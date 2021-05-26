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
import { Attachment } from '@/models/Attachment'

import {
  IJsonApiEntityWithOptionalId,
  IJsonApiEntity,
  IJsonApiRelationships,
  IJsonApiEntityWithoutDetails,
  IJsonApiEntityWithoutDetailsDataDictList
} from '@/serializers/jsonapi/JsonApiTypes'

import { DeviceAttachmentSerializer } from '@/serializers/jsonapi/DeviceAttachmentSerializer'

export const GENERIC_ACTION_ATTACHMENT_SERIALIZER_TYPE_DEVICE = 'device'
export const GENERIC_ACTION_ATTACHMENT_SERIALIZER_TYPE_PLATFORM = 'platform'
export type GenericActionAttachmentSerializerType = typeof GENERIC_ACTION_ATTACHMENT_SERIALIZER_TYPE_DEVICE | typeof GENERIC_ACTION_ATTACHMENT_SERIALIZER_TYPE_PLATFORM

export class GenericActionAttachmentSerializer {
  private attachmentSerializer: DeviceAttachmentSerializer = new DeviceAttachmentSerializer()
  private type: GenericActionAttachmentSerializerType

  constructor (type: GenericActionAttachmentSerializerType) {
    if (![GENERIC_ACTION_ATTACHMENT_SERIALIZER_TYPE_DEVICE, GENERIC_ACTION_ATTACHMENT_SERIALIZER_TYPE_PLATFORM].includes(type)) {
      throw new TypeError('type ' + type + ' is unknown')
    }
    this.type = type
  }

  convertModelToJsonApiData (attachment: Attachment, actionId: string): IJsonApiEntityWithOptionalId {
    /**
     * 2021-05-07 mha:
     * We build the relation to the action by hand instead of using the
     * GenericActionSerializer, to avoid circular references.  We also
     * build the relation to the attachment by hand instead of using the
     * DeviceAttachmentSerializer, which uses 'device_attachment' as its
     * property whereas we need 'attachment' as the property and
     * 'device_attachment' as the type.
     */
    const type = this.getActionAttachmentTypeName()
    const actionType = this.getActionTypeName()
    const attachmentType = this.getAttachmentTypeName()
    const data: IJsonApiEntityWithOptionalId = {
      type,
      attributes: {},
      relationships: {
        action: {
          data: {
            type: actionType,
            id: actionId
          }
        },
        attachment: {
          data: {
            type: attachmentType,
            id: attachment.id || ''
          }
        }
      }
    }
    return data
  }

  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntity[]): Attachment[] {
    const actionAttachmentIds = []
    const type = this.getActionAttachmentTypeName()
    const typePlural = type + 's'
    if (relationships[typePlural]) {
      const attachmentObject = relationships[typePlural] as IJsonApiEntityWithoutDetailsDataDictList
      if (attachmentObject.data && (attachmentObject.data as IJsonApiEntityWithoutDetails[]).length > 0) {
        for (const relationShipAttachmentData of attachmentObject.data as IJsonApiEntityWithoutDetails[]) {
          const actionAttachmentId = relationShipAttachmentData.id
          actionAttachmentIds.push(actionAttachmentId)
        }
      }
    }

    const attachmentIds = []
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === type) {
          const actionAttachmentId = includedEntry.id
          if (actionAttachmentIds.includes(actionAttachmentId)) {
            if (includedEntry.relationships && includedEntry.relationships.attachment && includedEntry.relationships.attachment.data && 'id' in includedEntry.relationships.attachment.data) {
              attachmentIds.push(includedEntry.relationships.attachment.data.id)
            }
          }
        }
      }
    }

    const attachmentType = this.getAttachmentTypeName()
    const attachments: Attachment[] = []
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === attachmentType) {
          const attachmentId = includedEntry.id
          if (attachmentIds.includes(attachmentId)) {
            const attachment = this.attachmentSerializer.convertJsonApiDataToModel(includedEntry)
            attachments.push(attachment)
          }
        }
      }
    }

    return attachments
  }

  getActionTypeName (): string {
    switch (this.type) {
      case GENERIC_ACTION_ATTACHMENT_SERIALIZER_TYPE_DEVICE:
        return 'generic_device_action'
      case GENERIC_ACTION_ATTACHMENT_SERIALIZER_TYPE_PLATFORM:
        return 'generic_platform_action'
      default:
        throw new TypeError('action type name not defined')
    }
  }

  getActionAttachmentTypeName (): string {
    switch (this.type) {
      case GENERIC_ACTION_ATTACHMENT_SERIALIZER_TYPE_DEVICE:
        return 'generic_device_action_attachment'
      case GENERIC_ACTION_ATTACHMENT_SERIALIZER_TYPE_PLATFORM:
        return 'generic_platform_action_attachment'
      default:
        throw new TypeError('action attachment type name not defined')
    }
  }

  getAttachmentTypeName (): string {
    switch (this.type) {
      case GENERIC_ACTION_ATTACHMENT_SERIALIZER_TYPE_DEVICE:
        return 'device_attachment'
      case GENERIC_ACTION_ATTACHMENT_SERIALIZER_TYPE_PLATFORM:
        return 'platform_attachment'
      default:
        throw new TypeError('attachment type name not defined')
    }
  }
}
