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

  constructor ({ states, deviceTypes, manufacturer, permissionGroups }: {states?: Status[], deviceTypes?: DeviceType[], manufacturer?: Manufacturer[], permissionGroups?: PermissionGroup[]} = {}) {
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
      includeArchivedDevices: typeof params.includeArchivedDevices !== 'undefined' && params.includeArchivedDevices === 'true'
    }
  }
}
