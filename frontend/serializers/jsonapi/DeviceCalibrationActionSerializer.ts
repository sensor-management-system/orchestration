/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
 */

import { DateTime } from 'luxon'

import { Attachment } from '@/models/Attachment'
import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'
import { DeviceProperty } from '@/models/DeviceProperty'

import { IJsonApiEntityEnvelope, IJsonApiEntityListEnvelope, IJsonApiEntityWithOptionalAttributes, IJsonApiEntityWithOptionalId, IJsonApiEntityWithoutDetails } from '@/serializers/jsonapi/JsonApiTypes'

import {
  ContactSerializer,
  IContactAndMissing
} from '@/serializers/jsonapi/ContactSerializer'

import { DeviceCalibrationActionAttachmentSerializer } from '@/serializers/jsonapi/DeviceCalibrationActionAttachmentSerializer'
import { DeviceCalibrationDevicePropertySerializer } from '@/serializers/jsonapi/DeviceCalibrationDevicePropertySerializer'

export interface IDeviceCalibrationActionAttachmentRelation {
  deviceCalibrationActionAttachmentId: string
  attachmentId: string
}

export interface IDeviceCalibrationPropertyRelation {
  devicePropertyCalibrationId: string
  devicePropertyId: string
}

export class DeviceCalibrationActionSerializer {
  private contactSerializer: ContactSerializer
  private attachmentSerializer: DeviceCalibrationActionAttachmentSerializer
  private devicePropertySerializer: DeviceCalibrationDevicePropertySerializer

  constructor () {
    this.contactSerializer = new ContactSerializer()
    this.attachmentSerializer = new DeviceCalibrationActionAttachmentSerializer()
    this.devicePropertySerializer = new DeviceCalibrationDevicePropertySerializer()
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): DeviceCalibrationAction[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((model) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): DeviceCalibrationAction {
    const data = jsonApiObject.data
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(data, included)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes, included: IJsonApiEntityWithOptionalAttributes[]): DeviceCalibrationAction {
    const attributes = jsonApiData.attributes
    const newEntry = DeviceCalibrationAction.createEmpty()

    newEntry.id = jsonApiData.id.toString()
    if (attributes) {
      newEntry.description = attributes.description || ''
      newEntry.formula = attributes.formula || ''
      newEntry.value = attributes.value || attributes.value === 0 || attributes.value === 0.0 ? attributes.value : null
      newEntry.currentCalibrationDate = attributes.current_calibration_date ? DateTime.fromISO(attributes.current_calibration_date, { zone: 'UTC' }) : null
      newEntry.nextCalibrationDate = attributes.next_calibration_date ? DateTime.fromISO(attributes.next_calibration_date, { zone: 'UTC' }) : null
    }

    const relationships = jsonApiData.relationships || {}

    const contactWithMissing: IContactAndMissing = this.contactSerializer.convertJsonApiRelationshipsSingleModel(relationships, included)
    if (contactWithMissing.contact) {
      newEntry.contact = contactWithMissing.contact
    }

    const attachments: Attachment[] = this.attachmentSerializer.convertJsonApiRelationshipsModelList(relationships, included)
    if (attachments.length) {
      newEntry.attachments = attachments
    }

    const measuredQuantities: DeviceProperty[] = this.devicePropertySerializer.convertJsonApiRelationshipsModelList(relationships, included)
    if (measuredQuantities.length) {
      newEntry.measuredQuantities = measuredQuantities
    }

    return newEntry
  }

  convertModelToJsonApiData (action: DeviceCalibrationAction, deviceId: string): IJsonApiEntityWithOptionalId {
    const data: IJsonApiEntityWithOptionalId = {
      type: 'device_calibration_action',
      attributes: {
        description: action.description,
        formula: action.formula,
        value: action.value === null ? null : action.value,
        current_calibration_date: action.currentCalibrationDate === null ? null : action.currentCalibrationDate.setZone('UTC').toISO(),
        next_calibration_date: action.nextCalibrationDate === null ? null : action.nextCalibrationDate.setZone('UTC').toISO()
      },
      relationships: {
        device: {
          data: {
            type: 'device',
            id: deviceId
          }
        }
      }
    }

    if (action.id) {
      data.id = action.id
    }

    if (action.contact && action.contact.id) {
      const contactRelationship = this.contactSerializer.convertModelToJsonApiRelationshipObject(action.contact)
      data.relationships = {
        ...data.relationships,
        ...contactRelationship
      }
    }

    // Note: Neither attachments nor device properties are included here as they must be saved separately

    return data
  }

  convertJsonApiIncludedActionAttachmentsToIdList (included: IJsonApiEntityWithOptionalAttributes[]): IDeviceCalibrationActionAttachmentRelation[] {
    const linkedAttachments: IDeviceCalibrationActionAttachmentRelation[] = []
    const type = 'device_calibration_attachment'
    included.forEach((i) => {
      if (!i.id) {
        return
      }
      if (i.type !== type) {
        return
      }
      if (!i.relationships?.attachment || !i.relationships?.attachment.data || !(i.relationships?.attachment.data as IJsonApiEntityWithoutDetails).id) {
        return
      }
      const attachmentId: string = (i.relationships.attachment.data as IJsonApiEntityWithoutDetails).id
      linkedAttachments.push({
        deviceCalibrationActionAttachmentId: i.id,
        attachmentId
      })
    })
    return linkedAttachments
  }

  convertJsonApiIncludedDevicePropertioesToIdList (included: IJsonApiEntityWithOptionalAttributes[]): IDeviceCalibrationPropertyRelation[] {
    const linkedProperties: IDeviceCalibrationPropertyRelation[] = []
    const type = 'device_property_calibration'
    included.forEach((i) => {
      if (!i.id) {
        return
      }
      if (i.type !== type) {
        return
      }
      if (!i.relationships?.device_property || !i.relationships?.device_property.data || !(i.relationships?.device_property.data as IJsonApiEntityWithoutDetails).id) {
        return
      }
      const devicePropertyId: string = (i.relationships.device_property.data as IJsonApiEntityWithoutDetails).id
      linkedProperties.push({
        devicePropertyCalibrationId: i.id,
        devicePropertyId
      })
    })
    return linkedProperties
  }
}
