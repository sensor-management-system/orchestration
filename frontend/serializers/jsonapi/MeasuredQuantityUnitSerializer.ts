/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { MeasuredQuantityUnit } from '@/models/MeasuredQuantityUnit'

import {
  IJsonApiEntityListEnvelope,
  IJsonApiEntity,
  IJsonApiEntityWithoutDetailsDataDict
} from '@/serializers/jsonapi/JsonApiTypes'

export class MeasuredQuantityUnitSerializer {
  private _included: IJsonApiEntity[] = []

  get included (): IJsonApiEntity[] {
    return this._included
  }

  set included (includedList: IJsonApiEntity[]) {
    this._included = includedList.filter(i => i.type === 'Unit')
  }

  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): MeasuredQuantityUnit[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel.bind(this))
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiEntity): MeasuredQuantityUnit {
    const id = jsonApiData.id.toString()
    const url = jsonApiData.links?.self || ''
    const defaultLimitMin = jsonApiData.attributes.default_limit_min
    const defaultLimitMax = jsonApiData.attributes.default_limit_max
    const unitId = (jsonApiData.relationships && jsonApiData.relationships.unit && jsonApiData.relationships.unit.data && (jsonApiData.relationships.unit as IJsonApiEntityWithoutDetailsDataDict).data.id) || ''
    const measuredQuantityId = (jsonApiData.relationships && jsonApiData.relationships.measured_quantity && jsonApiData.relationships.measured_quantity.data && (jsonApiData.relationships.measured_quantity as IJsonApiEntityWithoutDetailsDataDict).data.id) || ''

    // find the corresponding Unit and take the name and the definition from there
    let name = ''
    let definition = ''
    const relatedUnit = this.included.find(i => i.id === unitId)
    if (relatedUnit) {
      name = relatedUnit.attributes.term
      definition = relatedUnit.attributes.definition
    }

    return MeasuredQuantityUnit.createWithData(id, name, url, definition, defaultLimitMin, defaultLimitMax, unitId, measuredQuantityId)
  }

  convertModelToJsonApiData (measuredQuantityUnit: MeasuredQuantityUnit) {
    const attributes = {
      default_limit_min: measuredQuantityUnit.defaultLimitMin,
      default_limit_max: measuredQuantityUnit.defaultLimitMax
    }

    const relationships = {
      unit: {
        data: {
          id: measuredQuantityUnit.unitId,
          type: 'Unit'
        }
      },
      measured_quantity: {
        data: {
          id: measuredQuantityUnit.measuredQuantityId,
          type: 'MeasuredQuantity'
        }
      }
    }

    const wrapper: any = {
      type: 'MeasuredQuantityUnit',
      attributes,
      relationships
    }

    if (measuredQuantityUnit.id) {
      wrapper.id = measuredQuantityUnit.id
    }

    return wrapper
  }
}
