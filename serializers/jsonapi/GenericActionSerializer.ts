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
  genericDeviceActionAttachmentId: string
  attachmentId: string
}

export class GenericActionSerializer {
  private attachmentSerializer: GenericActionAttachmentSerializer = new GenericActionAttachmentSerializer()
  private contactSerializer: ContactSerializer = new ContactSerializer()

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

  convertModelToJsonApiData (action: GenericAction, deviceId: string): IJsonApiEntityWithOptionalId {
    const data: IJsonApiEntityWithOptionalId = {
      type: 'generic_device_action',
      attributes: {
        description: action.description,
        action_type_name: action.actionTypeName,
        action_type_uri: action.actionTypeUrl,
        begin_date: action.beginDate != null ? action.beginDate.setZone('UTC').toISO() : null,
        end_date: action.endDate != null ? action.endDate.setZone('UTC').toISO() : null
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
    // Note: Attachments are not included and must be send to the backend with
    // a relation to the action after this action was saved
    return data
  }

  convertModelToJsonApiRelationshipObject (action: IGenericAction): IJsonApiTypedEntityWithoutDetailsDataDict {
    return {
      generic_device_action: {
        data: this.convertModelToTupleWithIdAndType(action)
      }
    }
  }

  convertModelToTupleWithIdAndType (action: IGenericAction): IJsonApiEntityWithoutDetails {
    return {
      id: action.id || '',
      type: 'generic_device_action'
    }
  }

  /**
   * convert GenericActions that come as a relationship
   *
   * do we still need this one?
   *
   * @param {IJsonApiTypeIdDataListDict} relationships - a JSONAPI relationships object
   * @param {IJsonApiTypeIdAttributes[]} included - a JSONAPI object with included GenericActions
   * @return {IGenericActionsAndMissing} serialized GenericActions and an array of ids, that could not be resolved
   */
  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntity[]): IGenericActionsAndMissing {
    const actionIds = []
    if (relationships.generic_device_actions) {
      const actionObject = relationships.generic_device_actions as IJsonApiEntityWithoutDetailsDataDictList
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
        if (includedEntry.type === 'generic_device_action') {
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
    included.forEach((i) => {
      if (!i.id) {
        return
      }
      if (i.type !== 'generic_device_action_attachment') {
        return
      }
      if (!i.relationships?.attachment || !i.relationships?.attachment.data || !(i.relationships?.attachment.data as IJsonApiEntityWithoutDetails).id) {
        return
      }
      const attachmentId: string = (i.relationships.attachment.data as IJsonApiEntityWithoutDetails).id
      linkedAttachments.push({
        genericDeviceActionAttachmentId: i.id,
        attachmentId
      })
    })
    return linkedAttachments
  }
}
