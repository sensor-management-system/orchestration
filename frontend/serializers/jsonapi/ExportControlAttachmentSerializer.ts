/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'

import { ExportControlAttachment } from '@/models/ExportControlAttachment'
import { IJsonApiEntityEnvelope, IJsonApiEntityListEnvelope, IJsonApiEntityWithOptionalAttributes, IJsonApiEntityWithOptionalId } from '@/serializers/jsonapi/JsonApiTypes'

export class ExportControlAttachmentSerializer {
  convertModelToJsonApiData (attachment: ExportControlAttachment, manufacturerModelId: string): IJsonApiEntityWithOptionalId {
    const data: any = {
      type: 'export_control_attachment',
      attributes: {
        url: attachment.url,
        label: attachment.label,
        description: attachment.description,
        is_export_control_only: attachment.isExportControlOnly
        // is_upload will be set automatically
      },
      relationships: {
        manufacturer_model: {
          data: {
            type: 'manufacturer_model',
            id: manufacturerModelId
          }
        }
      }
    }

    if (attachment.id) {
      data.id = attachment.id
    }

    return data
  }

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): ExportControlAttachment {
    const jsonApiData = jsonApiObject.data
    return this.convertJsonApiDataToModel(jsonApiData)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntityWithOptionalAttributes): ExportControlAttachment {
    const newEntry = new ExportControlAttachment()

    newEntry.id = jsonApiData.id.toString()

    const attributes = jsonApiData.attributes
    if (attributes) {
      newEntry.url = attributes.url || ''
      newEntry.label = attributes.label || ''
      newEntry.description = attributes.description || ''
      newEntry.isUpload = attributes.is_upload || false
      newEntry.isExportControlOnly = attributes.is_export_control_only || false
      newEntry.createdAt = attributes.created_at != null ? DateTime.fromISO(attributes.created_at, { zone: 'UTC' }) : null
    }
    return newEntry
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): ExportControlAttachment[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel)
  }
}
