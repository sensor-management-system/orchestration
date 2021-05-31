/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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
}
