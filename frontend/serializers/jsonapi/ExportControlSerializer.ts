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
import { ExportControl } from '@/models/ExportControl'
import { IJsonApiEntityWithOptionalId, IJsonApiEntityEnvelope, IJsonApiEntityWithoutDetails, IJsonApiEntityListEnvelope, IJsonApiEntity } from '@/serializers/jsonapi/JsonApiTypes'

export class ExportControlSerializer {
  convertModelToJsonApiData (exportControl: ExportControl): IJsonApiEntityWithOptionalId {
    const data: IJsonApiEntityWithOptionalId = {
      type: 'export_control',
      attributes: {
        dual_use: exportControl.dualUse,
        export_control_classification_number: exportControl.exportControlClassificationNumber,
        customs_tariff_number: exportControl.customsTariffNumber,
        additional_information: exportControl.additionalInformation,
        internal_note: exportControl.internalNote
      },
      relationships: {
        manufacturer_model: {
          data: null
        }
      }
    }
    if (exportControl.id) {
      data.id = exportControl.id
    }
    if (exportControl.manufacturerModelId) {
      data.relationships!.manufacturer_model.data = {
        type: 'manufacturer_model',
        id: exportControl.manufacturerModelId
      }
    }
    return data
  }

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiEntityEnvelope): ExportControl {
    const data = jsonApiObject.data

    const result = new ExportControl()
    result.id = data.id || ''

    const attributes = data.attributes

    if (attributes.dual_use === true || attributes.dual_use === false) {
      result.dualUse = attributes.dual_use
    } else {
      result.dualUse = null
    }
    result.exportControlClassificationNumber = attributes.export_control_classification_number || ''
    result.customsTariffNumber = attributes.customs_tariff_number || ''
    result.additionalInformation = attributes.additional_information || ''
    result.internalNote = attributes.internal_note || ''

    result.createdAt = attributes.created_at != null ? DateTime.fromISO(attributes.created_at, { zone: 'UTC' }) : null
    result.updatedAt = attributes.updated_at != null ? DateTime.fromISO(attributes.updated_at, { zone: 'UTC' }) : null

    const relationships = data.relationships
    if (relationships?.manufacturer_model?.data) {
      const manufacturerModelData = relationships?.manufacturer_model?.data as IJsonApiEntityWithoutDetails
      if (data.id) {
        result.manufacturerModelId = manufacturerModelData.id
      }
    }
    if (relationships?.created_by?.data) {
      const createdByIdData = relationships.created_by.data as IJsonApiEntityWithoutDetails
      if (data.id) {
        result.createdByUserId = createdByIdData.id
      }
    }
    if (relationships?.updated_by?.data) {
      const updatedByIdData = relationships.updated_by.data as IJsonApiEntityWithoutDetails
      if (data.id) {
        result.updatedByUserId = updatedByIdData.id
      }
    }

    return result
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): ExportControl[] {
    return jsonApiObjectList.data.map((model: IJsonApiEntity) => {
      return this.convertJsonApiObjectToModel({ data: model, included: jsonApiObjectList.included || [] })
    })
  }
}
