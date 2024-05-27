/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
