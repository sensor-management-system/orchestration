/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2023
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tim Eder (UFZ, tim.eder@ufz.de)
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
import { SiteUsage } from '@/models/SiteUsage'
import { SiteType } from '@/models/SiteType'

export interface ISiteSearchParams {
  searchText: string | null
  permissionGroups: PermissionGroup[]
  onlyOwnSites: boolean
  includeArchivedSites: boolean
  siteUsages: SiteUsage[]
  siteTypes: SiteType[]
}

/**
 * defines methods to convert from ISearchParameters to QueryParams and vice
 * versa
 */
export class SiteSearchParamsSerializer {
  public permissionGroups: PermissionGroup[] = []
  public siteUsages: SiteUsage[] = []
  public siteTypes: SiteType[] = []

  constructor ({ permissionGroups, siteUsages, siteTypes }: {permissionGroups?: PermissionGroup[], siteUsages?: SiteUsage[], siteTypes?: SiteType[]} = {}) {
    if (permissionGroups) {
      this.permissionGroups = permissionGroups
    }
    if (siteUsages) {
      this.siteUsages = siteUsages
    }
    if (siteTypes) {
      this.siteTypes = siteTypes
    }
  }

  /**
   * converts search parameters to Vue route query params
   *
   * @param {ISiteSearchParams} params - the params used in the search
   * @returns {QueryParams} Vue route query params
   */
  toQueryParams (params: ISiteSearchParams): QueryParams {
    const result: QueryParams = {}
    if (params.searchText) {
      result.searchText = params.searchText
    }
    if (params.onlyOwnSites) {
      result.onlyOwnSites = String(params.onlyOwnSites)
    }
    if (params.includeArchivedSites) {
      result.includeArchivedSites = String(params.includeArchivedSites)
    }
    if (params.permissionGroups) {
      result.permissionGroups = params.permissionGroups.map(p => p.id)
    }
    if (params.siteUsages) {
      result.siteUsages = params.siteUsages.map(s => s.id)
    }
    if (params.siteTypes) {
      result.siteTypes = params.siteTypes.map(s => s.id)
    }
    return result
  }

  /**
   * converts Vue route query params to search parameters
   *
   * @param {QueryParams} params - the Vue route query params
   * @returns {ISiteSearchParams} the params used in the search
   */
  toSearchParams (params: QueryParams): ISiteSearchParams {
    const isNotUndefined = (value: any) => typeof value !== 'undefined'

    let permissionGroups: PermissionGroup[] = []
    if (params.permissionGroups) {
      if (!Array.isArray(params.permissionGroups)) {
        params.permissionGroups = [params.permissionGroups]
      }
      permissionGroups = params.permissionGroups.map(paramId => this.permissionGroups.find(permissionGroup => permissionGroup.id === paramId)).filter(isNotUndefined) as PermissionGroup[]
    }

    let siteUsages: SiteUsage[] = []
    if (params.siteUsages) {
      if (!Array.isArray(params.siteUsages)) {
        params.siteUsages = [params.siteUsages]
      }
      siteUsages = params.siteUsages.map(paramId => this.siteUsages.find(siteUsage => siteUsage.id === paramId)).filter(isNotUndefined) as SiteUsage[]
    }

    let siteTypes: SiteType[] = []
    if (params.siteType) {
      if (!Array.isArray(params.siteTypes)) {
        params.siteTypes = [params.siteTypes]
      }
      siteTypes = params.siteTypes.map(paramId => this.siteTypes.find(siteType => siteType.id === paramId)).filter(isNotUndefined) as SiteType[]
    }

    return {
      searchText: typeof params.searchText === 'string' ? params.searchText : '',
      permissionGroups,
      siteUsages,
      siteTypes,
      onlyOwnSites: typeof params.onlyOwnSites !== 'undefined' && params.onlyOwnSites === 'true',
      includeArchivedSites: typeof params.includeArchivedSites !== 'undefined' && params.includeArchivedSites === 'true'
    }
  }
}
