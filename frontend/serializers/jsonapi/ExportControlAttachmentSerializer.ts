/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2024
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
