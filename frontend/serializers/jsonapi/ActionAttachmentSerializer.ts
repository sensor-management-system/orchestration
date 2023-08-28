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
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiRelationships,
  IJsonApiEntityWithoutDetails,
  IJsonApiEntityWithoutDetailsDataDictList
} from '@/serializers/jsonapi/JsonApiTypes'

import { IAttachmentSerializer } from '@/serializers/jsonapi/AttachmentSerializer'
import { DeviceAttachmentSerializer } from '@/serializers/jsonapi/DeviceAttachmentSerializer'
import { PlatformAttachmentSerializer } from '@/serializers/jsonapi/PlatformAttachmentSerializer'

export interface IActionAttachmentSerializer {
  attachmentSerializer: IAttachmentSerializer
  getActionTypeName (): string
  getActionAttachmentTypeName (): string
  getActionAttachmentTypeNamePlural (): string
  getAttachmentTypeName (): string
  convertModelToJsonApiData (attachment: Attachment, actionId: string): IJsonApiEntityWithOptionalId
  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): Attachment[]
}

export abstract class AbstractActionAttachmentSerializer implements IActionAttachmentSerializer {
  abstract get attachmentSerializer (): IAttachmentSerializer
  abstract getActionTypeName (): string
  abstract getActionAttachmentTypeName (): string
  abstract getActionAttachmentTypeNamePlural (): string
  abstract getAttachmentTypeName (): string

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
    const entityType = this.getActionAttachmentTypeName()
    const actionType = this.getActionTypeName()
    const attachmentType = this.getAttachmentTypeName()
    const data: IJsonApiEntityWithOptionalId = {
      type: entityType,
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

  convertJsonApiRelationshipsModelList (relationships: IJsonApiRelationships, included: IJsonApiEntityWithOptionalAttributes[]): Attachment[] {
    const actionAttachmentIds = []
    const entityType = this.getActionAttachmentTypeName()
    const typePlural = this.getActionAttachmentTypeNamePlural()
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
        if (includedEntry.type === entityType) {
          const actionAttachmentId = includedEntry.id
          if (actionAttachmentIds.includes(actionAttachmentId)) {
            if ((includedEntry.relationships?.attachment?.data as IJsonApiEntityWithoutDetails | undefined)?.id) {
              attachmentIds.push((includedEntry.relationships?.attachment?.data as IJsonApiEntityWithoutDetails).id)
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
}

export class GenericDeviceActionAttachmentSerializer extends AbstractActionAttachmentSerializer {
  private _attachmentSerializer: IAttachmentSerializer

  constructor () {
    super()
    this._attachmentSerializer = new DeviceAttachmentSerializer()
  }

  getActionTypeName (): string {
    return 'generic_device_action'
  }

  getActionAttachmentTypeName (): string {
    return 'generic_device_action_attachment'
  }

  getActionAttachmentTypeNamePlural (): string {
    return this.getActionAttachmentTypeName() + 's'
  }

  getAttachmentTypeName (): string {
    return 'device_attachment'
  }

  get attachmentSerializer (): IAttachmentSerializer {
    return this._attachmentSerializer
  }
}

export class GenericPlatformActionAttachmentSerializer extends AbstractActionAttachmentSerializer {
  private _attachmentSerializer: IAttachmentSerializer

  constructor () {
    super()
    this._attachmentSerializer = new PlatformAttachmentSerializer()
  }

  getActionTypeName (): string {
    return 'generic_platform_action'
  }

  getActionAttachmentTypeName (): string {
    return 'generic_platform_action_attachment'
  }

  getActionAttachmentTypeNamePlural (): string {
    return this.getActionAttachmentTypeName() + 's'
  }

  getAttachmentTypeName (): string {
    return 'platform_attachment'
  }

  get attachmentSerializer (): IAttachmentSerializer {
    return this._attachmentSerializer
  }
}
