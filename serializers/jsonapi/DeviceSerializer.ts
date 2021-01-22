/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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
import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'

import { IJsonApiObjectList, IJsonApiObject, IJsonApiDataWithId, IJsonApiDataWithOptionalId, IJsonApiTypeIdAttributes, IJsonApiTypeIdAttributesWithOptionalRelationships } from '@/serializers/jsonapi/JsonApiTypes'

import { AttachmentSerializer } from '@/serializers/jsonapi/AttachmentSerializer'
import { ContactSerializer, IMissingContactData } from '@/serializers/jsonapi/ContactSerializer'
import { CustomTextFieldSerializer } from '@/serializers/jsonapi/CustomTextFieldSerializer'
import { DevicePropertySerializer } from '@/serializers/jsonapi/DevicePropertySerializer'

export interface IDeviceMissingData {
  contacts: IMissingContactData
}

export interface IDeviceWithMeta {
  device: Device
  missing: IDeviceMissingData
}

export class DeviceSerializer {
  private attachmentSerializer: AttachmentSerializer = new AttachmentSerializer()
  private contactSerializer: ContactSerializer = new ContactSerializer()
  private customTextFieldSerializer: CustomTextFieldSerializer = new CustomTextFieldSerializer()
  private devicePropertySerializer: DevicePropertySerializer = new DevicePropertySerializer()

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiObject): IDeviceWithMeta {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiDataWithId | IJsonApiTypeIdAttributesWithOptionalRelationships, included: IJsonApiTypeIdAttributes[]): IDeviceWithMeta {
    const result: Device = new Device()

    const attributes = jsonApiData.attributes
    const relationships = jsonApiData.relationships || {}

    result.id = jsonApiData.id

    result.description = attributes.description || ''
    result.shortName = attributes.short_name || ''
    result.longName = attributes.long_name || ''
    result.serialNumber = attributes.serial_number || ''
    result.manufacturerUri = attributes.manufacturer_uri || ''
    result.manufacturerName = attributes.manufacturer_name || ''
    result.deviceTypeUri = attributes.device_type_uri || ''
    result.deviceTypeName = attributes.device_type_name || ''
    result.statusUri = attributes.status_uri || ''
    result.statusName = attributes.status_name || ''
    result.model = attributes.model || ''
    result.dualUse = attributes.dual_use || false
    result.inventoryNumber = attributes.inventory_number || ''
    result.persistentIdentifier = attributes.persistent_identifier || ''
    result.website = attributes.website || ''
    result.createdAt = attributes.created_at != null ? DateTime.fromISO(attributes.created_at, { zone: 'UTC' }) : null
    result.updatedAt = attributes.updated_at != null ? DateTime.fromISO(attributes.updated_at, { zone: 'UTC' }) : null
    // TODO
    // result.createdBy = attributes.created_by
    // result.updatedBy = attributes.updated_by
    // result.events = []

    result.attachments = this.attachmentSerializer.convertNestedJsonApiToModelList(attributes.attachments)
    result.customFields = this.customTextFieldSerializer.convertNestedJsonApiToModelList(attributes.customfields)
    result.properties = this.devicePropertySerializer.convertNestedJsonApiToModelList(attributes.properties)

    const contactsWithMissing = this.contactSerializer.convertJsonApiRelationshipsModelList(relationships, included)
    result.contacts = contactsWithMissing.contacts
    const missingDataForContactIds = contactsWithMissing.missing.ids

    return {
      device: result,
      missing: {
        contacts: {
          ids: missingDataForContactIds
        }
      }
    }
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiObjectList): IDeviceWithMeta[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((model: IJsonApiDataWithId) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }

  convertJsonApiRelationshipsModelList (included: IJsonApiTypeIdAttributes[]): Device[] {
    // it takes all the devices, as those are the only ones included in the query per configuration.
    // if you want to use it in a broader scope, you may have to change several things
    const result = []
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === 'device') {
          const device = this.convertJsonApiDataToModel(includedEntry, []).device
          result.push(device)
        }
      }
    }
    return result
  }

  convertModelToJsonApiData (device: Device): IJsonApiDataWithOptionalId {
    const properties = this.devicePropertySerializer.convertModelListToNestedJsonApiArray(device.properties)
    const customfields = this.customTextFieldSerializer.convertModelListToNestedJsonApiArray(device.customFields)
    const attachments = this.attachmentSerializer.convertModelListToNestedJsonApiArray(device.attachments)
    const contacts = this.contactSerializer.convertModelListToJsonApiRelationshipObject(device.contacts)

    const data: IJsonApiDataWithOptionalId = {
      type: 'device',
      attributes: {
        description: device.description,
        short_name: device.shortName,
        long_name: device.longName,
        serial_number: device.serialNumber,
        inventory_number: device.inventoryNumber,
        manufacturer_uri: device.manufacturerUri,
        manufacturer_name: device.manufacturerName,
        device_type_uri: device.deviceTypeUri,
        device_type_name: device.deviceTypeName,
        status_uri: device.statusUri,
        status_name: device.statusName,
        model: device.model,
        persistent_identifier: device.persistentIdentifier === '' ? null : device.persistentIdentifier,
        website: device.website,
        dual_use: device.dualUse,
        // those two time slots are set by the db, no matter what we deliver here
        created_at: device.createdAt != null ? device.createdAt.setZone('UTC').toISO() : null,
        updated_at: device.updatedAt != null ? device.updatedAt.setZone('UTC').toISO() : null,
        // TODO
        // created_by: device.createdBy,
        // updated_by: device.updatedBy,

        customfields,
        properties,
        attachments
      },
      relationships: {
        ...contacts
        // TODO: events
      }
    }

    if (device.id !== null) {
      data.id = device.id
    }

    return data
  }
}

export const deviceWithMetaToDeviceByThrowingErrorOnMissing = (deviceWithMeta: IDeviceWithMeta) : Device => {
  const device = deviceWithMeta.device

  if (deviceWithMeta.missing.contacts.ids.length > 0) {
    throw new Error('Contacts are missing')
  }

  return device
}

export const deviceWithMetaToDeviceByAddingDummyObjects = (deviceWithMeta: IDeviceWithMeta) : Device => {
  const device = deviceWithMeta.device

  for (const missingContactId of deviceWithMeta.missing.contacts.ids) {
    const contact = new Contact()
    contact.id = missingContactId
    device.contacts.push(contact)
  }

  return device
}
