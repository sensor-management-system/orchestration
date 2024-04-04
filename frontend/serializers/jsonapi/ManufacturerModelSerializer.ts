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
