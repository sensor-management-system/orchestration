/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
 * - Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 * (UFZ, https://www.ufz.de)
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
        label: attachment.label
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
