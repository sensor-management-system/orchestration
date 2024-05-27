/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'
import { GenericAction, IGenericAction } from '@/models/GenericAction'
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
  GenericDeviceActionAttachmentSerializer,
  GenericPlatformActionAttachmentSerializer,
  GenericConfigurationActionAttachmentSerializer
} from '@/serializers/jsonapi/GenericActionAttachmentSerializer'

export interface IMissingGenericActionData {
  ids: string[]
}

export interface IGenericActionsAndMissing {
  genericActions: GenericAction[]
  missing: IMissingGenericActionData
}

export interface IGenericActionAttachmentRelation {
  genericActionAttachmentId: string
  attachmentId: string
}

export interface IGenericActionSerializer {
  targetType: string
  attachmentSerializer: IActionAttachmentSerializer
  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): GenericAction
  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes, included: IJsonApiEntityWithOptionalAttributes[]): GenericAction
  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): GenericAction[]
  convertModelToJsonApiData (action: GenericAction, deviceOrPlatformId: string): IJsonApiEntityWithOptionalId
  convertModelToJsonApiRelationshipObject (action: IGenericAction): IJsonApiRelationships
  convertModelToTupleWithIdAndType (action: IGenericAction): IJsonApiEntityWithoutDetails
  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): IGenericActionsAndMissing
  convertJsonApiIncludedActionAttachmentsToIdList (included: IJsonApiEntityWithOptionalAttributes[]): IGenericActionAttachmentRelation[]
  getActionTypeName (): string
  getActionTypeNamePlural (): string
  getActionAttachmentTypeName (): string
}

export abstract class AbstractGenericActionSerializer implements IGenericActionSerializer {
  private contactSerializer: ContactSerializer = new ContactSerializer()

  abstract get targetType (): string
  abstract get attachmentSerializer (): IActionAttachmentSerializer

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): GenericAction {
    const data = jsonApiObject.data
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(data, included)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes, included: IJsonApiEntityWithOptionalAttributes[]): GenericAction {
    const attributes = jsonApiData.attributes
    const newEntry = GenericAction.createEmpty()

    newEntry.id = jsonApiData.id.toString()
    if (attributes) {
      newEntry.description = attributes.description || ''
      newEntry.actionTypeName = attributes.action_type_name || ''
      newEntry.actionTypeUrl = attributes.action_type_uri || ''
      newEntry.beginDate = attributes.begin_date ? DateTime.fromISO(attributes.begin_date, { zone: 'UTC' }) : null
      newEntry.endDate = attributes.end_date ? DateTime.fromISO(attributes.end_date, { zone: 'UTC' }) : null
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

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): GenericAction[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((model) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }

  convertModelToJsonApiData (action: GenericAction, deviceOrPlatformId: string): IJsonApiEntityWithOptionalId {
    const data: IJsonApiEntityWithOptionalId = {
      type: this.getActionTypeName(),
      attributes: {
        description: action.description,
        action_type_name: action.actionTypeName,
        action_type_uri: action.actionTypeUrl,
        begin_date: action.beginDate != null ? action.beginDate.setZone('UTC').toISO() : null,
        end_date: action.endDate != null ? action.endDate.setZone('UTC').toISO() : null
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

  convertModelToJsonApiRelationshipObject (action: IGenericAction): IJsonApiRelationships {
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

  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): IGenericActionsAndMissing {
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
      genericActions: actions,
      missing: {
        ids: missingDataForActionIds
      }
    }
  }

  convertJsonApiIncludedActionAttachmentsToIdList (included: IJsonApiEntityWithOptionalAttributes[]): IGenericActionAttachmentRelation[] {
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
    return 'generic_' + this.targetType + '_action'
  }

  getActionTypeNamePlural (): string {
    return this.getActionTypeName() + 's'
  }

  getActionAttachmentTypeName (): string {
    return 'generic_' + this.targetType + '_action_attachment'
  }
}

export class GenericDeviceActionSerializer extends AbstractGenericActionSerializer {
  private _attachmentSerializer: IActionAttachmentSerializer

  constructor () {
    super()
    this._attachmentSerializer = new GenericDeviceActionAttachmentSerializer()
  }

  get targetType (): string {
    return 'device'
  }

  get attachmentSerializer (): IActionAttachmentSerializer {
    return this._attachmentSerializer
  }
}

export class GenericPlatformActionSerializer extends AbstractGenericActionSerializer {
  private _attachmentSerializer: IActionAttachmentSerializer

  constructor () {
    super()
    this._attachmentSerializer = new GenericPlatformActionAttachmentSerializer()
  }

  get targetType (): string {
    return 'platform'
  }

  get attachmentSerializer (): IActionAttachmentSerializer {
    return this._attachmentSerializer
  }
}

export class GenericConfigurationActionSerializer extends AbstractGenericActionSerializer {
  private _attachmentSerializer: IActionAttachmentSerializer

  constructor () {
    super()
    this._attachmentSerializer = new GenericConfigurationActionAttachmentSerializer()
  }

  get targetType (): string {
    return 'configuration'
  }

  get attachmentSerializer (): IActionAttachmentSerializer {
    return this._attachmentSerializer
  }
}
