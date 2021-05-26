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
import { GenericAction, IGenericAction } from '@/models/GenericAction'
import { Attachment } from '@/models/Attachment'
import {
  IJsonApiEntityEnvelope,
  IJsonApiEntityListEnvelope,
  IJsonApiEntity,
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityWithoutDetails,
  IJsonApiTypedEntityWithoutDetailsDataDict,
  IJsonApiEntityWithoutDetailsDataDictList,
  IJsonApiRelationships
} from '@/serializers/jsonapi/JsonApiTypes'

import { ContactSerializer, IContactAndMissing } from '@/serializers/jsonapi/ContactSerializer'
import { GenericActionAttachmentSerializer } from '@/serializers/jsonapi/GenericActionAttachmentSerializer'

export interface IMissingGenericActionData {
  ids: string[]
}

export interface IGenericActionsAndMissing {
  genericDeviceActions: GenericAction[]
  missing: IMissingGenericActionData
}

export interface IGenericActionAttachmentRelation {
  genericActionAttachmentId: string
  attachmentId: string
}

export const GENERIC_ACTION_SERIALIZER_TYPE_DEVICE = 'device'
export const GENERIC_ACTION_SERIALIZER_TYPE_PLATFORM = 'platform'
export type GenericActionSerializerType = typeof GENERIC_ACTION_SERIALIZER_TYPE_DEVICE | typeof GENERIC_ACTION_SERIALIZER_TYPE_PLATFORM

export class GenericActionSerializer {
  private attachmentSerializer: GenericActionAttachmentSerializer
  private contactSerializer: ContactSerializer = new ContactSerializer()
  private type: GenericActionSerializerType

  constructor (type: GenericActionSerializerType) {
    if (![GENERIC_ACTION_SERIALIZER_TYPE_DEVICE, GENERIC_ACTION_SERIALIZER_TYPE_PLATFORM].includes(type)) {
      throw new TypeError('type ' + type + ' is unknown')
    }
    this.type = type
    this.attachmentSerializer = new GenericActionAttachmentSerializer(this.type)
  }

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): GenericAction {
    const data = jsonApiObject.data
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(data, included)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntity, included: IJsonApiEntity[]): GenericAction {
    const attributes = jsonApiData.attributes
    const newEntry = GenericAction.createEmpty()

    newEntry.id = jsonApiData.id.toString()
    newEntry.description = attributes.description || ''
    newEntry.actionTypeName = attributes.action_type_name || ''
    newEntry.actionTypeUrl = attributes.action_type_uri || ''
    newEntry.beginDate = attributes.begin_date ? DateTime.fromISO(attributes.begin_date, { zone: 'UTC' }) : null
    newEntry.endDate = attributes.end_date ? DateTime.fromISO(attributes.end_date, { zone: 'UTC' }) : null

    const relationships = jsonApiData.relationships || {}

    const contactWithMissing: IContactAndMissing = this.contactSerializer.convertJsonApiRelationshipsSingleModel(relationships, included)
    if (contactWithMissing.contact) {
      newEntry.contact = contactWithMissing.contact
    }

    const attachments: Attachment[] = this.attachmentSerializer.convertJsonApiRelationshipsModelList(relationships, included)
    if (attachments.length) {
      newEntry.attachments = attachments
    }

    return newEntry
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): GenericAction[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((model: IJsonApiEntity) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }

  convertModelToJsonApiData (action: GenericAction, deviceOrPlatformId: string): IJsonApiEntityWithOptionalId {
    const type = this.getActionTypeName()
    let relationships: IJsonApiRelationships
    switch (this.type) {
      case GENERIC_ACTION_SERIALIZER_TYPE_DEVICE:
        relationships = {
          device: {
            data: {
              type: 'device',
              id: deviceOrPlatformId
            }
          }
        }
        break
      case GENERIC_ACTION_SERIALIZER_TYPE_PLATFORM:
        relationships = {
          platform: {
            data: {
              type: 'platform',
              id: deviceOrPlatformId
            }
          }
        }
        break
    }
    const data: IJsonApiEntityWithOptionalId = {
      type,
      attributes: {
        description: action.description,
        action_type_name: action.actionTypeName,
        action_type_uri: action.actionTypeUrl,
        begin_date: action.beginDate != null ? action.beginDate.setZone('UTC').toISO() : null,
        end_date: action.endDate != null ? action.endDate.setZone('UTC').toISO() : null
      },
      relationships
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
    // Note: Attachments are not included and must be send to the backend with
    // a relation to the action after this action was saved
    return data
  }

  convertModelToJsonApiRelationshipObject (action: IGenericAction): IJsonApiTypedEntityWithoutDetailsDataDict {
    return {
      [this.getActionTypeName()]: {
        data: this.convertModelToTupleWithIdAndType(action)
      }
    }
  }

  convertModelToTupleWithIdAndType (action: IGenericAction): IJsonApiEntityWithoutDetails {
    return {
      id: action.id || '',
      type: this.getActionTypeName()
    }
  }

  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntity[]): IGenericActionsAndMissing {
    const actionIds = []
    const type = this.getActionTypeName()
    const typePlural = type + 's'
    if (relationships[typePlural]) {
      const actionObject = relationships[typePlural] as IJsonApiEntityWithoutDetailsDataDictList
      if (actionObject.data && (actionObject.data as IJsonApiEntityWithoutDetails[]).length > 0) {
        for (const relationShipActionData of actionObject.data) {
          const actionId = relationShipActionData.id
          actionIds.push(actionId)
        }
      }
    }

    const possibleActions: { [key: string]: GenericAction } = {}
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === type) {
          const actionId = includedEntry.id
          if (actionIds.includes(actionId)) {
            const action = this.convertJsonApiDataToModel(includedEntry, [])
            possibleActions[actionId] = action
          }
        }
      }
    }

    const actions = []
    const missingDataForActionIds = []

    for (const actionId of actionIds) {
      if (possibleActions[actionId]) {
        actions.push(possibleActions[actionId])
      } else {
        missingDataForActionIds.push(actionId)
      }
    }

    return {
      genericDeviceActions: actions,
      missing: {
        ids: missingDataForActionIds
      }
    }
  }

  convertJsonApiIncludedGenericActionAttachmentsToIdList (included: IJsonApiEntity[]): IGenericActionAttachmentRelation[] {
    const linkedAttachments: IGenericActionAttachmentRelation[] = []
    const type = this.getActionAttachmentTypeName()
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
        genericActionAttachmentId: i.id,
        attachmentId
      })
    })
    return linkedAttachments
  }

  getActionTypeName (): string {
    switch (this.type) {
      case GENERIC_ACTION_SERIALIZER_TYPE_DEVICE:
        return 'generic_device_action'
      case GENERIC_ACTION_SERIALIZER_TYPE_PLATFORM:
        return 'generic_platform_action'
      default:
        throw new TypeError('action type name not defined')
    }
  }

  getActionAttachmentTypeName (): string {
    switch (this.type) {
      case GENERIC_ACTION_SERIALIZER_TYPE_DEVICE:
        return 'generic_device_action_attachment'
      case GENERIC_ACTION_SERIALIZER_TYPE_PLATFORM:
        return 'generic_platform_action_attachment'
      default:
        throw new TypeError('action attachment type name not defined')
    }
  }
}
