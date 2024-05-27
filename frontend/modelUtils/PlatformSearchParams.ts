/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { QueryParams } from '@/modelUtils/QueryParams'

import { Manufacturer } from '@/models/Manufacturer'
import { PermissionGroup } from '@/models/PermissionGroup'
import { PlatformType } from '@/models/PlatformType'
import { Status } from '@/models/Status'

export interface IPlatformSearchParams {
  searchText: string | null
  manufacturer: Manufacturer[]
  states: Status[]
  types: PlatformType[]
  permissionGroups: PermissionGroup[]
  onlyOwnPlatforms: boolean
  includeArchivedPlatforms: boolean
  manufacturerName: string | null
  model: string | null
}

/**
 * defines methods to convert from ISearchParameters to QueryParams and vice
 * versa
 */
export class PlatformSearchParamsSerializer {
  public states: Status[] = []
  public platformTypes: PlatformType[] = []
  public manufacturer: Manufacturer[] = []
  public permissionGroups: PermissionGroup[] = []
  public skipManufacturerName: boolean = false
  public skipModel: boolean = false

  constructor ({ states, platformTypes, manufacturer, permissionGroups, skipManufacturerName, skipModel }: {states?: Status[], platformTypes?: PlatformType[], manufacturer?: Manufacturer[], permissionGroups?: PermissionGroup[], skipManufacturerName?: boolean, skipModel?: boolean} = {}) {
    if (states) {
      this.states = states
    }
    if (platformTypes) {
      this.platformTypes = platformTypes
    }
    if (manufacturer) {
      this.manufacturer = manufacturer
    }
    if (permissionGroups) {
      this.permissionGroups = permissionGroups
    }
    this.skipManufacturerName = !!skipManufacturerName
    this.skipModel = !!skipModel
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
    if (params.includeArchivedPlatforms) {
      result.includeArchivedPlatforms = String(params.includeArchivedPlatforms)
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
    if (params.permissionGroups) {
      result.permissionGroups = params.permissionGroups.map(p => p.id)
    }
    if (params.manufacturerName && !this.skipManufacturerName) {
      result.manufacturerName = params.manufacturerName
    }
    if (params.model && !this.skipModel) {
      result.model = params.model
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

    let permissionGroups: PermissionGroup[] = []
    if (params.permissionGroups) {
      if (!Array.isArray(params.permissionGroups)) {
        params.permissionGroups = [params.permissionGroups]
      }
      permissionGroups = params.permissionGroups.map(paramId => this.permissionGroups.find(permissionGroup => permissionGroup.id === paramId)).filter(isNotUndefined) as PermissionGroup[]
    }

    return {
      searchText: typeof params.searchText === 'string' ? params.searchText : '',
      manufacturer,
      states,
      types,
      permissionGroups,
      onlyOwnPlatforms: typeof params.onlyOwnPlatforms !== 'undefined' && params.onlyOwnPlatforms === 'true',
      includeArchivedPlatforms: typeof params.includeArchivedPlatforms !== 'undefined' && params.includeArchivedPlatforms === 'true',
      manufacturerName: typeof params.manufacturerName === 'string' && !this.skipManufacturerName ? params.manufacturerName : '',
      model: typeof params.model === 'string' && !this.skipModel ? params.model : ''
    }
  }
}
