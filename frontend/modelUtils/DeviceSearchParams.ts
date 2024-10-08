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
import { DeviceType } from '@/models/DeviceType'
import { PermissionGroup } from '@/models/PermissionGroup'
import { Status } from '@/models/Status'

export interface IDeviceSearchParams {
  searchText: string | null
  manufacturer: Manufacturer[]
  states: Status[]
  types: DeviceType[]
  permissionGroups: PermissionGroup[]
  onlyOwnDevices: boolean
  includeArchivedDevices: boolean
  manufacturerName: string | null
  model: string | null
}

/**
 * defines methods to convert from ISearchParameters to QueryParams and vice
 * versa
 */
export class DeviceSearchParamsSerializer {
  public states: Status[] = []
  public deviceTypes: DeviceType[] = []
  public manufacturer: Manufacturer[] = []
  public permissionGroups: PermissionGroup[] = []
  public skipManufacturerName: boolean = false
  public skipModel: boolean = false

  constructor ({ states, deviceTypes, manufacturer, permissionGroups, skipManufacturerName, skipModel }: {states?: Status[], deviceTypes?: DeviceType[], manufacturer?: Manufacturer[], permissionGroups?: PermissionGroup[], skipManufacturerName?: boolean, skipModel?: boolean} = {}) {
    if (states) {
      this.states = states
    }
    if (deviceTypes) {
      this.deviceTypes = deviceTypes
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
   * @param {IDeviceSearchParams} params - the params used in the search
   * @returns {QueryParams} Vue route query params
   */
  toQueryParams (params: IDeviceSearchParams): QueryParams {
    const result: QueryParams = {}
    if (params.searchText) {
      result.searchText = params.searchText
    }
    if (params.onlyOwnDevices) {
      result.onlyOwnDevices = String(params.onlyOwnDevices)
    }
    if (params.includeArchivedDevices) {
      result.includeArchivedDevices = String(params.includeArchivedDevices)
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
   * @returns {IDeviceSearchParams} the params used in the search
   */
  toSearchParams (params: QueryParams): IDeviceSearchParams {
    const isNotUndefined = (value: any) => typeof value !== 'undefined'

    let manufacturer: Manufacturer[] = []
    if (params.manufacturer) {
      if (!Array.isArray(params.manufacturer)) {
        params.manufacturer = [params.manufacturer]
      }
      manufacturer = params.manufacturer.map(paramId => this.manufacturer.find(manufacturer => manufacturer.id === paramId)).filter(isNotUndefined) as Manufacturer[]
    }

    let types: DeviceType[] = []
    if (params.types) {
      if (!Array.isArray(params.types)) {
        params.types = [params.types]
      }
      types = params.types.map(paramId => this.deviceTypes.find(deviceType => deviceType.id === paramId)).filter(isNotUndefined) as DeviceType[]
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
      onlyOwnDevices: typeof params.onlyOwnDevices !== 'undefined' && params.onlyOwnDevices === 'true',
      includeArchivedDevices: typeof params.includeArchivedDevices !== 'undefined' && params.includeArchivedDevices === 'true',
      manufacturerName: typeof params.manufacturerName === 'string' && !this.skipManufacturerName ? params.manufacturerName : '',
      model: typeof params.model === 'string' && !this.skipModel ? params.model : ''
    }
  }
}
