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
  IJsonApiDataWithId,
  IJsonApiDataWithOptionalId,
  IJsonApiTypeIdDataList,
  IJsonApiTypeIdDataListDict

} from '@/serializers/jsonapi/JsonApiTypes'
import { DeviceAttachmentSerializer } from '@/serializers/jsonapi/DeviceAttachmentSerializer'

export class GenericDeviceActionAttachmentSerializer {
  private attachmentSerializer: DeviceAttachmentSerializer = new DeviceAttachmentSerializer()

  convertModelToJsonApiData (attachment: Attachment, actionId: string): IJsonApiDataWithOptionalId {
    /**
     * 2021-05-07 mha:
     * We build the relation to the action by hand instead of using the
     * GenericDeviceActionSerializer, to avoid circular references.  We also
     * build the relation to the attachment by hand instead of using the
     * DeviceAttachmentSerializer, which uses 'device_attachment' as its
     * property whereas we need 'attachment' as the property and
     * 'device_attachment' as the type.
     */
    const data: any = {
      type: 'generic_device_action_attachment',
      attributes: {},
      relationships: {
        action: {
          data: {
            type: 'generic_device_action',
            id: actionId
          }
        },
        attachment: {
          data: {
            type: 'device_attachment',
            id: attachment.id
          }
        }
      }
    }
    return data
  }

  convertJsonApiRelationshipsModelList (relationships: IJsonApiTypeIdDataListDict, included: IJsonApiDataWithId[]): Attachment[] {
    const actionAttachmentIds = []
    if (relationships.generic_device_action_attachments) {
      const attachmentObject = relationships.generic_device_action_attachments as IJsonApiTypeIdDataList
      if (attachmentObject.data && attachmentObject.data.length > 0) {
        for (const relationShipAttachmentData of attachmentObject.data) {
          const actionAttachmentId = relationShipAttachmentData.id
          actionAttachmentIds.push(actionAttachmentId)
        }
      }
    }

    const attachmentIds = []
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === 'generic_device_action_attachment') {
          const actionAttachmentId = includedEntry.id
          if (actionAttachmentIds.includes(actionAttachmentId)) {
            if (includedEntry.relationships.attachment && includedEntry.relationships.attachment.data && 'id' in includedEntry.relationships.attachment.data) {
              attachmentIds.push(includedEntry.relationships.attachment.data.id)
            }
          }
        }
      }
    }

    const attachments: Attachment[] = []
    if (included && included.length > 0) {
      for (const includedEntry of included) {
        if (includedEntry.type === 'device_attachment') {
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
}
