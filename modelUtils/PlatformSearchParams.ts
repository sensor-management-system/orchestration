/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2022
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

import { QueryParams } from '@/modelUtils/QueryParams'

import { Manufacturer } from '@/models/Manufacturer'
import { PlatformType } from '@/models/PlatformType'
import { Status } from '@/models/Status'

export interface IPlatformBasicSearchParams {
  searchText: string | null
}

export interface IPlatformSearchParams extends IPlatformBasicSearchParams {
  manufacturer: Manufacturer[]
  states: Status[]
  types: PlatformType[]
  onlyOwnPlatforms: boolean
}

/**
 * defines methods to convert from ISearchParameters to QueryParams and vice
 * versa
 */
export class PlatformSearchParamsSerializer {
  public states: Status[] = []
  public platformTypes: PlatformType[] = []
  public manufacturer: Manufacturer[] = []

  constructor ({ states, platformTypes, manufacturer }: {states?: Status[], platformTypes?: PlatformType[], manufacturer?: Manufacturer[]} = {}) {
    if (states) {
      this.states = states
    }
    if (platformTypes) {
      this.platformTypes = platformTypes
    }
    if (manufacturer) {
      this.manufacturer = manufacturer
    }
  }

  /**
   * converts search parameters to Vue route query params
   *
   * @param {IPlatformSearchParams} params - the params used in the search
   * @returns {QueryParams} Vue route query params
   */
  toQueryParams (params: IPlatformSearchParams): QueryParams {
    const result: QueryParams = {}
    if (params.searchText) {
      result.searchText = params.searchText
    }
    if (params.onlyOwnPlatforms) {
      result.onlyOwnPlatforms = String(params.onlyOwnPlatforms)
    }
    if (params.manufacturer) {
      result.manufacturer = params.manufacturer.map(m => m.id)
    }
    if (params.types) {
      result.types = params.types.map(t => t.id)
    }
    if (params.states) {
      result.states = params.states.map(s => s.id)
    }
    return result
  }

  /**
   * converts Vue route query params to search parameters
   *
   * @param {QueryParams} params - the Vue route query params
   * @returns {IPlatformSearchParams} the params used in the search
   */
  toSearchParams (params: QueryParams): IPlatformSearchParams {
    const isNotUndefined = (value: any) => typeof value !== 'undefined'

    let manufacturer: Manufacturer[] = []
    if (params.manufacturer) {
      if (!Array.isArray(params.manufacturer)) {
        params.manufacturer = [params.manufacturer]
      }
      manufacturer = params.manufacturer.map(paramId => this.manufacturer.find(manufacturer => manufacturer.id === paramId)).filter(isNotUndefined) as Manufacturer[]
    }

    let types: PlatformType[] = []
    if (params.types) {
      if (!Array.isArray(params.types)) {
        params.types = [params.types]
      }
      types = params.types.map(paramId => this.platformTypes.find(platformType => platformType.id === paramId)).filter(isNotUndefined) as PlatformType[]
    }

    let states: Status[] = []
    if (params.states) {
      if (!Array.isArray(params.states)) {
        params.states = [params.states]
      }
      states = params.states.map(paramId => this.states.find(state => state.id === paramId)).filter(isNotUndefined) as Status[]
    }

    return {
      searchText: typeof params.searchText === 'string' ? params.searchText : '',
      manufacturer,
      states,
      types,
      onlyOwnPlatforms: typeof params.onlyOwnPlatforms !== 'undefined' && params.onlyOwnPlatforms === 'true'
    }
  }
}
