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

import { Site } from '@/models/Site'
import { PermissionGroup } from '@/models/PermissionGroup'

export interface IConfigurationBasicSearchParams {
  searchText: string | null
}

export interface IConfigurationSearchParams extends IConfigurationBasicSearchParams {
  states: string[]
  projects: string[]
  campaigns: string[]
  sites: Site[]
  permissionGroups: PermissionGroup[]
  onlyOwnConfigurations: boolean
  includeArchivedConfigurations: boolean
}

/**
 * defines methods to convert from ISearchParameters to QueryParams and vice
 * versa
 */
export class ConfigurationSearchParamsSerializer {
  public states: string[] = []
  public projects: string[] = []
  public campaigns: string[] = []
  public sites: Site[] = []
  public permissionGroups: PermissionGroup[] = []

  constructor ({ states, projects, sites, permissionGroups, campaigns }: {states?: string[], projects?: string[], sites?: Site[], permissionGroups?: PermissionGroup[], campaigns?: string[]} = {}) {
    if (states) {
      this.states = states
    }
    if (projects) {
      this.projects = projects
    }
    if (campaigns) {
      this.campaigns = campaigns
    }
    if (sites) {
      this.sites = sites
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
    if (params.projects) {
      result.projects = params.projects
    }
    if (params.campaigns) {
      result.campaigns = params.campaigns
    }
    if (params.sites) {
      result.sites = params.sites.map(s => s.id)
    }
    if (params.onlyOwnConfigurations) {
      result.onlyOwnConfigurations = String(params.onlyOwnConfigurations)
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
    let projects: string[] = []
    if (params.projects) {
      if (!Array.isArray(params.projects)) {
        params.projects = [params.projects]
      }
      projects = params.projects.filter(project => typeof project === 'string') as string[]
    }
    let campaigns: string[] = []
    if (params.campaigns) {
      if (!Array.isArray(params.campaigns)) {
        params.campaigns = [params.campaigns]
      }
      campaigns = params.campaigns.filter(campaign => typeof campaign === 'string') as string[]
    }

    let sites: Site[] = []
    if (params.sites) {
      if (!Array.isArray(params.sites)) {
        params.sites = [params.sites]
      }
      sites = params.sites.map(siteId => this.sites.find(site => site.id === siteId)).filter(isNotUndefined) as Site[]
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
      projects,
      campaigns,
      sites,
      permissionGroups,
      onlyOwnConfigurations: typeof params.onlyOwnConfigurations !== 'undefined' && params.onlyOwnConfigurations === 'true',
      includeArchivedConfigurations: typeof params.includeArchivedConfigurations !== 'undefined' && params.includeArchivedConfigurations === 'true'
    }
  }
}
