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

import { PermissionGroup } from '@/models/PermissionGroup'

export interface IConfigurationBasicSearchParams {
  searchText: string | null
}

export interface IConfigurationSearchParams extends IConfigurationBasicSearchParams {
  states: string[]
  permissionGroups: PermissionGroup[]
  includeArchivedConfigurations: boolean
}

/**
 * defines methods to convert from ISearchParameters to QueryParams and vice
 * versa
 */
export class ConfigurationSearchParamsSerializer {
  public states: string[] = []
  public permissionGroups: PermissionGroup[] = []

  constructor ({ states, permissionGroups }: {states?: string[], permissionGroups?: PermissionGroup[]} = {}) {
    if (states) {
      this.states = states
    }
    if (permissionGroups) {
      this.permissionGroups = permissionGroups
    }
  }

  /**
   * converts search parameters to Vue route query params
   *
   * @param {IConfigurationSearchParams} params - the params used in the search
   * @returns {QueryParams} Vue route query params
   */
  toQueryParams (params: IConfigurationSearchParams): QueryParams {
    const result: QueryParams = {}
    if (params.searchText) {
      result.searchText = params.searchText
    }
    if (params.states) {
      result.states = params.states
    }
    if (params.permissionGroups) {
      result.permissionGroups = params.permissionGroups.map(p => p.id)
    }
    if (params.includeArchivedConfigurations) {
      result.includeArchivedConfigurations = String(params.includeArchivedConfigurations)
    }
    return result
  }

  /**
   * converts Vue route query params to search parameters
   *
   * @param {QueryParams} params - the Vue route query params
   * @returns {IConfigurationSearchParams} the params used in the search
   */
  toSearchParams (params: QueryParams): IConfigurationSearchParams {
    const isNotUndefined = (value: any) => typeof value !== 'undefined'

    let states: string[] = []
    if (params.states) {
      if (!Array.isArray(params.states)) {
        params.states = [params.states]
      }
      states = params.states.filter(state => typeof state === 'string') as string[]
    }

    let permissionGroups: PermissionGroup[] = []
    if (params.permissionGroups) {
      if (!Array.isArray(params.permissionGroups)) {
        params.permissionGroups = [params.permissionGroups]
      }
      permissionGroups = params.permissionGroups.map(paramId => this.permissionGroups.find(permissionGroup => permissionGroup.id === paramId)).filter(isNotUndefined) as PermissionGroup[]
    }

    return {
      searchText: typeof params.searchText === 'string' ? params.searchText : '',
      states,
      permissionGroups,
      includeArchivedConfigurations: typeof params.includeArchivedConfigurations !== 'undefined' && params.includeArchivedConfigurations === 'true'
    }
  }
}
