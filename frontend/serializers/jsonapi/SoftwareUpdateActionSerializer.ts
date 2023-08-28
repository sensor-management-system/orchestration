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
import { SoftwareUpdateAction, ISoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { Attachment } from '@/models/Attachment'
import {
  IJsonApiEntityEnvelope,
  IJsonApiEntityListEnvelope,
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiEntityWithoutDetails,
  IJsonApiEntityWithoutDetailsDataDictList,
  IJsonApiRelationships
} from '@/serializers/jsonapi/JsonApiTypes'

import {
  ContactSerializer,
  IContactAndMissing
} from '@/serializers/jsonapi/ContactSerializer'

import { IActionAttachmentSerializer } from '@/serializers/jsonapi/ActionAttachmentSerializer'

import {
  DeviceSoftwareUpdateActionAttachmentSerializer,
  PlatformSoftwareUpdateActionAttachmentSerializer
} from '@/serializers/jsonapi/SoftwareUpdateActionAttachmentSerializer'

export interface IMissingSoftwareUpdateActionData {
  ids: string[]
}

export interface ISoftwareUpdateActionsAndMissing {
  softwareUpdateActions: SoftwareUpdateAction[]
  missing: IMissingSoftwareUpdateActionData
}

export interface ISoftwareUpdateActionAttachmentRelation {
  softwareUpdateActionAttachmentId: string
  attachmentId: string
}

export interface ISoftwareUpdateActionSerializer {
  targetType: string
  attachmentSerializer: IActionAttachmentSerializer
  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): SoftwareUpdateAction
  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes, included: IJsonApiEntityWithOptionalAttributes[]): SoftwareUpdateAction
  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): SoftwareUpdateAction[]
  convertModelToJsonApiData (action: SoftwareUpdateAction, deviceOrPlatformId: string): IJsonApiEntityWithOptionalId
  convertModelToJsonApiRelationshipObject (action: ISoftwareUpdateAction): IJsonApiRelationships
  convertModelToTupleWithIdAndType (action: ISoftwareUpdateAction): IJsonApiEntityWithoutDetails
  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): ISoftwareUpdateActionsAndMissing
  convertJsonApiIncludedActionAttachmentsToIdList (included: IJsonApiEntityWithOptionalAttributes[]): ISoftwareUpdateActionAttachmentRelation[]
  getActionTypeName (): string
  getActionTypeNamePlural (): string
  getActionAttachmentTypeName (): string
}

export abstract class AbstractSoftwareUpdateActionSerializer implements ISoftwareUpdateActionSerializer {
  private contactSerializer: ContactSerializer = new ContactSerializer()

  abstract get targetType (): string
  abstract get attachmentSerializer (): IActionAttachmentSerializer

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): SoftwareUpdateAction {
    const data = jsonApiObject.data
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(data, included)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes, included: IJsonApiEntityWithOptionalAttributes[]): SoftwareUpdateAction {
    const attributes = jsonApiData.attributes
    const newEntry = SoftwareUpdateAction.createEmpty()

    newEntry.id = jsonApiData.id.toString()
    if (attributes) {
      newEntry.description = attributes.description || ''
      newEntry.softwareTypeName = attributes.software_type_name || ''
      newEntry.softwareTypeUrl = attributes.software_type_uri || ''
      newEntry.updateDate = attributes.update_date ? DateTime.fromISO(attributes.update_date, { zone: 'UTC' }) : null
      newEntry.version = attributes.version || ''
      newEntry.repositoryUrl = attributes.repository_url || ''
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

    return newEntry
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): SoftwareUpdateAction[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((model) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }

  convertModelToJsonApiData (action: SoftwareUpdateAction, deviceOrPlatformId: string): IJsonApiEntityWithOptionalId {
    const data: IJsonApiEntityWithOptionalId = {
      type: this.getActionTypeName(),
      attributes: {
        description: action.description,
        software_type_name: action.softwareTypeName,
        software_type_uri: action.softwareTypeUrl,
        update_date: action.updateDate != null ? action.updateDate.setZone('UTC').toISO() : null,
        version: action.version,
        repository_url: action.repositoryUrl
      },
      relationships: {
        [this.targetType]: {
          data: {
            type: this.targetType,
            id: deviceOrPlatformId
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

  convertModelToJsonApiRelationshipObject (action: ISoftwareUpdateAction): IJsonApiRelationships {
    return {
      [this.getActionTypeName()]: {
        data: this.convertModelToTupleWithIdAndType(action)
      }
    }
  }

  convertModelToTupleWithIdAndType (action: ISoftwareUpdateAction): IJsonApiEntityWithoutDetails {
    return {
      id: action.id || '',
      type: this.getActionTypeName()
    }
  }

  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): ISoftwareUpdateActionsAndMissing {
    const actionIds = []
    const type = this.getActionTypeName()
    const typePlural = this.getActionTypeNamePlural()
    if (relationships[typePlural]) {
      const actionObject = relationships[typePlural] as IJsonApiEntityWithoutDetailsDataDictList
      if (actionObject.data && (actionObject.data as IJsonApiEntityWithoutDetails[]).length > 0) {
        for (const relationShipActionData of actionObject.data) {
          const actionId = relationShipActionData.id
          actionIds.push(actionId)
        }
      }
    }

    const possibleActions: { [key: string]: SoftwareUpdateAction } = {}
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
      softwareUpdateActions: actions,
      missing: {
        ids: missingDataForActionIds
      }
    }
  }

  convertJsonApiIncludedActionAttachmentsToIdList (included: IJsonApiEntityWithOptionalAttributes[]): ISoftwareUpdateActionAttachmentRelation[] {
    const linkedAttachments: ISoftwareUpdateActionAttachmentRelation[] = []
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
        softwareUpdateActionAttachmentId: i.id,
        attachmentId
      })
    })
    return linkedAttachments
  }

  getActionTypeName (): string {
    return this.targetType + '_software_update_action'
  }

  getActionTypeNamePlural (): string {
    return this.getActionTypeName() + 's'
  }

  getActionAttachmentTypeName (): string {
    return this.targetType + '_software_update_action_attachment'
  }
}

export class DeviceSoftwareUpdateActionSerializer extends AbstractSoftwareUpdateActionSerializer {
  private _attachmentSerializer: IActionAttachmentSerializer

  constructor () {
    super()
    this._attachmentSerializer = new DeviceSoftwareUpdateActionAttachmentSerializer()
  }

  get targetType (): string {
    return 'device'
  }

  get attachmentSerializer (): IActionAttachmentSerializer {
    return this._attachmentSerializer
  }
}

export class PlatformSoftwareUpdateActionSerializer extends AbstractSoftwareUpdateActionSerializer {
  private _attachmentSerializer: IActionAttachmentSerializer

  constructor () {
    super()
    this._attachmentSerializer = new PlatformSoftwareUpdateActionAttachmentSerializer()
  }

  get targetType (): string {
    return 'platform'
  }

  get attachmentSerializer (): IActionAttachmentSerializer {
    return this._attachmentSerializer
  }
}
