/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'

import { Attachment, IAttachment } from '@/models/Attachment'

import
{
  IJsonApiEntityEnvelope,
  IJsonApiEntityListEnvelope,
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiEntityWithoutDetails,
  IJsonApiTypedEntityWithoutDetailsDataDictList,
  IJsonApiRelationships
}
  from
  '@/serializers/jsonapi/JsonApiTypes'

export interface IMissingAttachmentData {
  ids: string[]
}

export interface IAttachmentsAndMissing {
  attachments: Attachment[]
  missing: IMissingAttachmentData
}

export interface IAttachmentSerializer {
  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): Attachment
  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes): Attachment
  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): Attachment[]
  convertJsonApiRelationshipsSingleModel (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): Attachment | null
}

export class AttachmentSerializer implements IAttachmentSerializer {
  private _type: string
  private _relation: string

  constructor (type: string, relation: string) {
    this._type = type
    this._relation = relation
  }

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): Attachment {
    const data = jsonApiObject.data
    return this.convertJsonApiDataToModel(data)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes): Attachment {
    const attributes = jsonApiData.attributes
    const newEntry = Attachment.createEmpty()

    newEntry.id = jsonApiData.id.toString()

    if (attributes) {
      newEntry.url = attributes.url || ''
      newEntry.label = attributes.label || ''
      newEntry.description = attributes.description || ''
      newEntry.isUpload = attributes.is_upload || false
      newEntry.createdAt = attributes.created_at != null ? DateTime.fromISO(attributes.created_at, { zone: 'UTC' }) : null
    }

    return newEntry
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): Attachment[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel)
  }

  convertModelToJsonApiData (attachment: IAttachment, relationId: string): IJsonApiEntityWithOptionalId {
    const data: any = {
      type: this._type,
      attributes: {
        url: attachment.url,
        label: attachment.label,
        description: attachment.description
        // no need to set 'is_upload' - it is a read only field
        // Also the field for the created_at entry is set automatically
      },
      relationships: {
        [this._relation]: {
          data: {
            type: this._relation,
            id: relationId
          }
        }
      }
    }
    if (attachment.id) {
      data.id = attachment.id
    }
    return data
  }

  convertJsonApiRelationshipsSingleModel (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): Attachment | null {
    let requiredAttachmentId = null
    if (relationships[this._type]) {
      const attachmentObject = relationships[this._type]
      if (attachmentObject.data) {
        requiredAttachmentId = (attachmentObject.data as IJsonApiEntityWithoutDetails).id
      }
    }

    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === this._type) {
          const attachmentId = includedEntry.id
          if (requiredAttachmentId === attachmentId) {
            return this.convertJsonApiDataToModel(includedEntry)
          }
        }
      }
    }

    return null
  }

  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): IAttachmentsAndMissing {
    const attachmentIds = []
    const typePlural = this._type + 's'
    if (relationships[typePlural]) {
      const attachmentObject = relationships[typePlural]
      if (attachmentObject.data && (attachmentObject.data as IJsonApiEntityWithoutDetails[]).length > 0) {
        for (const relationShipAttachmentData of (attachmentObject.data as IJsonApiEntityWithoutDetails[])) {
          const attachmentId = relationShipAttachmentData.id
          attachmentIds.push(attachmentId)
        }
      }
    }

    const possibleAttachments: { [key: string]: Attachment } = {}
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === this._type) {
          const attachmentId = includedEntry.id
          if (attachmentIds.includes(attachmentId)) {
            const attachment = this.convertJsonApiDataToModel(includedEntry)
            possibleAttachments[attachmentId] = attachment
          }
        }
      }
    }

    const attachments = []
    const missingDataForAttachmentIds = []

    for (const attachmentId of attachmentIds) {
      if (possibleAttachments[attachmentId]) {
        attachments.push(possibleAttachments[attachmentId])
      } else {
        missingDataForAttachmentIds.push(attachmentId)
      }
    }

    return {
      attachments,
      missing: {
        ids: missingDataForAttachmentIds
      }
    }
  }

  convertModelListToJsonApiRelationshipObject (attachments: IAttachment[]): IJsonApiTypedEntityWithoutDetailsDataDictList {
    const typePlural = this._type + 's'
    return {
      [typePlural]: {
        data: this.convertModelListToTupleListWithIdAndType(attachments)
      }
    }
  }

  convertModelListToTupleListWithIdAndType (attachments: IAttachment[]): IJsonApiEntityWithoutDetails[] {
    const result: IJsonApiEntityWithoutDetails[] = []
    for (const attachment of attachments) {
      if (attachment.id !== null) {
        result.push({
          id: attachment.id,
          type: this._type
        })
      }
    }
    return result
  }
}
