/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { ManufacturerModel } from '@/models/ManufacturerModel'
import {
  IJsonApiEntityEnvelope,
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiEntityWithoutDetails,
  IJsonApiEntity,
  IJsonApiEntityListEnvelope
} from '@/serializers/jsonapi/JsonApiTypes'
import { ExportControlSerializer } from '@/serializers/jsonapi/ExportControlSerializer'

export class ManufacturerModelSerializer {
  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): ManufacturerModel {
    const result = new ManufacturerModel()

    const data = jsonApiObject.data
    result.id = data.id || ''

    const attributes = data.attributes
    result.manufacturerName = attributes.manufacturer_name || ''
    result.model = attributes.model || ''
    result.externalSystemName = attributes.external_system_name || ''
    result.externalSystemUrl = attributes.external_system_url || ''

    if (data.relationships?.export_control.data) {
      const exportControlSerializer = new ExportControlSerializer()

      const exportControlById: {[key: string]: IJsonApiEntityWithOptionalAttributes} = {}
      const included: IJsonApiEntityWithOptionalAttributes[] = jsonApiObject.included || []
      for (const includedDataset of included) {
        if (includedDataset.type === 'export_control') {
          exportControlById[includedDataset.id] = includedDataset
        }
      }

      const exportControlRelationshipData = data.relationships.export_control.data as IJsonApiEntityWithoutDetails
      if (exportControlRelationshipData.id) {
        const exportControlData = exportControlById[exportControlRelationshipData.id]
        if (exportControlData) {
          const exportControlToTransfom = {
            data: exportControlData
          } as IJsonApiEntityEnvelope
          result.exportControl = exportControlSerializer.convertJsonApiObjectToModel(exportControlToTransfom)
        }
      }
    }

    return result
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): ManufacturerModel[] {
    return jsonApiObjectList.data.map((model: IJsonApiEntity) => {
      return this.convertJsonApiObjectToModel({ data: model, included: jsonApiObjectList.included || [] })
    })
  }
}
