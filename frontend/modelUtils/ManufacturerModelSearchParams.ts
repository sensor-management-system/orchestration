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

import { Manufacturer } from '@/models/Manufacturer'
import { QueryParams } from '@/modelUtils/QueryParams'

export type DualUseSearchOption = 'all' | 'yes' | 'no' | 'unspecified'

export interface IManufacturerModelSearchParams {
  searchText: string | null
  manufacturers: Manufacturer[]
  dualUseSearchOption: DualUseSearchOption
}

export class ManufacturerModelSearchParamsSerializer {
  public manufacturer: Manufacturer[] = []

  constructor ({ manufacturer }: { manufacturer?: Manufacturer[] } = {}) {
    if (manufacturer) {
      this.manufacturer = manufacturer
    }
  }

  toQueryParams (params: IManufacturerModelSearchParams): QueryParams {
    const result: QueryParams = {}
    if (params.searchText) {
      result.searchText = params.searchText
    }
    if (params.manufacturers) {
      result.manufacturer = params.manufacturers.map(m => m.id)
    }
    if (params.dualUseSearchOption) {
      result.dualUse = params.dualUseSearchOption
    }
    return result
  }

  toSearchParams (params: QueryParams): IManufacturerModelSearchParams {
    const isNotUndefined = (value: any) => typeof value !== 'undefined'

    let manufacturers: Manufacturer[] = []
    if (params.manufacturers) {
      if (!Array.isArray(params.manufacturers)) {
        params.manufacturers = [params.manufacturers]
      }
      manufacturers = params.manufacturers.map(
        paramId => this.manufacturer.find(
          manufacturer => manufacturer.id === paramId
        )
      ).filter(isNotUndefined) as Manufacturer[]
    }

    return {
      searchText: typeof params.searchText === 'string' ? params.searchText : '',
      manufacturers,
      dualUseSearchOption: typeof params.dualUse === 'string' ? params.dualUse as DualUseSearchOption : 'all'
    }
  }
}
