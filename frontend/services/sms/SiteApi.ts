/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
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
import { AxiosInstance, Method } from 'axios'

import { Site } from '@/models/Site'

import { PermissionGroup } from '@/models/PermissionGroup'

import {
  SiteSerializer,
  siteWithMetaToSiteByAddingDummyObjects,
  siteWithMetaToSiteThrowingNoErrorOnMissing
} from '@/serializers/jsonapi/SiteSerializer'
import { ContactRole } from '@/models/ContactRole'
import { ContactRoleSerializer } from '@/serializers/jsonapi/ContactRoleSerializer'
import { SiteConfigurationsApi } from '@/services/sms/SiteConfigurationsApi'
import { SiteUsage } from '@/models/SiteUsage'
import { SiteType } from '@/models/SiteType'
import { SiteAttachmentSerializer } from '@/serializers/jsonapi/SiteAttachmentSerializer'
import { Attachment } from '@/models/Attachment'

export interface IncludedRelationships {
  includeContacts?: boolean
  includeCreatedBy?: boolean
  includeUpdatedBy?: boolean
}

function getIncludeParams (includes: IncludedRelationships): string {
  const listIncludedRelationships: string[] = []
  if (includes.includeContacts) {
    listIncludedRelationships.push('contacts')
  }
  if (includes.includeCreatedBy) {
    listIncludedRelationships.push('created_by.contact')
  }
  if (includes.includeUpdatedBy) {
    listIncludedRelationships.push('updated_by.contact')
  }
  return listIncludedRelationships.join(',')
}

export type SitePermissionFetchFunction = () => Promise<PermissionGroup[]>

export class SiteApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: SiteSerializer
  private permissionFetcher: SitePermissionFetchFunction | undefined

  private _siteConfigurationsApi: SiteConfigurationsApi

  private _searchedPermissionGroups: PermissionGroup[] = []
  private _searchedSiteUsages: SiteUsage[] = []
  private _searchedSiteTypes: SiteType[] = []
  private _searchedUserMail: string | null = null
  private _searchedCreatorId: string | null = null
  private _searchedIncludeArchivedSites: boolean = false
  private _searchText: string | null = null
  private filterSettings: any[] = []

  constructor (
    axiosInstance: AxiosInstance,
    basePath: string,
    siteConfigurationsApi: SiteConfigurationsApi,
    permissionFetcher?: SitePermissionFetchFunction
  ) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
    this.serializer = new SiteSerializer()
    this._siteConfigurationsApi = siteConfigurationsApi
    if (permissionFetcher) {
      this.permissionFetcher = permissionFetcher
    }
  }

  get siteConfigurationsApi (): SiteConfigurationsApi {
    return this._siteConfigurationsApi
  }

  get searchedPermissionGroups (): PermissionGroup[] {
    return this._searchedPermissionGroups
  }

  async getSensorML (siteId: string): Promise<Blob> {
    const url = this.basePath + '/' + siteId + '/sensorml'
    const response = await this.axiosApi.get(url)
    return new Blob([response.data], { type: 'text/xml' })
  }

  getSensorMLUrl (siteId: string): string {
    return this.axiosApi.defaults.baseURL + this.basePath + '/' + siteId + '/sensorml'
  }

  setSearchedPermissionGroups (value: PermissionGroup[]) {
    this._searchedPermissionGroups = value
    return this
  }

  get searchedSiteUsages (): SiteUsage[] {
    return this._searchedSiteUsages
  }

  setSearchedSiteUsages (value: SiteUsage[]) {
    this._searchedSiteUsages = value
    return this
  }

  get searchedSiteTypes (): SiteType[] {
    return this._searchedSiteTypes
  }

  setSearchedSiteTypes (value: SiteType[]) {
    this._searchedSiteTypes = value
    return this
  }

  get searchedUserMail (): string | null {
    return this._searchedUserMail
  }

  setSearchedUserMail (value: string | null) {
    this._searchedUserMail = value
    return this
  }

  get searchedCreatorId (): string | null {
    return this._searchedCreatorId
  }

  setSearchedCreatorId (value: string | null) {
    this._searchedCreatorId = value
    return this
  }

  get searchText (): string | null {
    return this._searchText
  }

  setSearchText (value: string | null) {
    this._searchText = value
    return this
  }

  get searchIncludeArchivedSites (): boolean {
    return this._searchedIncludeArchivedSites
  }

  setSearchIncludeArchivedSites (value: boolean) {
    this._searchedIncludeArchivedSites = value
    return this
  }

  private get commonParams (): any {
    const result: any = {
      filter: JSON.stringify(this.filterSettings)
    }
    if (this.searchText) {
      result.q = this.searchText
    }
    result.sort = 'label'
    if (this.searchIncludeArchivedSites) {
      result.hide_archived = false
    }
    return result
  }

  async searchPaginated (pageNumber: number, pageSize: number, includes: IncludedRelationships = {}) {
    this.prepareSearch()
    // set the permission groups for the serializer
    if (this.permissionFetcher) {
      this.serializer.permissionGroups = await this.permissionFetcher()
    }

    const include = getIncludeParams(includes)

    return this.axiosApi.get(
      this.basePath,
      {
        params: {
          'page[size]': pageSize,
          'page[number]': pageNumber,
          include,
          ...this.commonParams
        }
      }
    ).then((rawResponse) => {
      const rawData = rawResponse.data
      const elements: Site[] = this.serializer.convertJsonApiObjectListToModelList(
        rawData
      ).map(siteWithMetaToSiteByAddingDummyObjects)

      const totalCount = rawData.meta.count

      return {
        elements,
        totalCount
      }
    })
  }

  async searchAll () {
    this.prepareSearch()
    // set the permission groups for the serializer
    if (this.permissionFetcher) {
      this.serializer.permissionGroups = await this.permissionFetcher()
    }

    return this.axiosApi.get(
      this.basePath,
      {
        params: {
          ...this.commonParams,
          'page[size]': 10000
        }
      }
    ).then((rawResponse: any) => {
      const rawData = rawResponse.data
      return this.serializer
        .convertJsonApiObjectListToModelList(rawData)
        .map(siteWithMetaToSiteByAddingDummyObjects)
    })
  }

  async findRelatedConfigurations (siteId: string) {
    return await this.siteConfigurationsApi.findRelatedConfigurations(siteId)
  }

  async findRelatedSiteAttachments (siteId: string): Promise<Attachment[]> {
    const url = this.basePath + '/' + siteId + '/site-attachments'
    const params = {
      'page[size]': 10000
    }
    return await this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new SiteAttachmentSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  async searchRecentlyUpdated (amount: number) {
    this.prepareSearch()
    const response = await this.axiosApi.get(
      this.basePath,
      {
        params: {
          'page[size]': amount,
          'page[number]': 1,
          sort: '-updated_at',
          include: 'updated_by.contact',
          hide_archived: false,
          filter: JSON.stringify([{ name: 'updated_at', op: 'ne', val: null }])
        }
      }
    )
    // We don't ask the api to load the contacts, so we just add dummy objects
    // to stay with the relationships
    return this.serializer
      .convertJsonApiObjectListToModelList(response.data)
      .map(siteWithMetaToSiteByAddingDummyObjects)
  }

  prepareSearch () {
    this.resetFilterSetting()
    this.preparePermissionGroups()
    this.prepareSiteUsages()
    this.prepareSiteTypes()
    this.prepareMail()
    this.prepareCreator()
  }

  prepareMail () {
    if (this.searchedUserMail) {
      this.filterSettings.push({
        name: 'site_contact_roles.contact.email',
        op: 'eq',
        val: this.searchedUserMail
      })
    }
  }

  prepareCreator () {
    if (this.searchedCreatorId) {
      this.filterSettings.push({
        name: 'created_by_id',
        op: 'eq',
        val: this.searchedCreatorId
      })
    }
  }

  resetFilterSetting () {
    this.filterSettings = []
  }

  preparePermissionGroups () {
    if (this.searchedPermissionGroups.length > 0) {
      this.filterSettings.push({
        or: this.searchedPermissionGroups.map((permissionGroup) => {
          return {
            name: 'group_ids',
            op: 'any',
            val: permissionGroup.id
          }
        })
      })
    }
  }

  prepareSiteUsages () {
    if (this.searchedSiteUsages.length > 0) {
      this.filterSettings.push({
        or: [
          {
            name: 'site_usage_name',
            op: 'in_',
            val: this.searchedSiteUsages.map((s: SiteUsage) => s.name)
          },
          {
            name: 'site_usage_uri',
            op: 'in_',
            val: this.searchedSiteUsages.map((s: SiteUsage) => s.uri)
          }
        ]
      })
    }
  }

  prepareSiteTypes () {
    if (this.searchedSiteTypes.length > 0) {
      this.filterSettings.push({
        or: [
          {
            name: 'site_type_name',
            op: 'in_',
            val: this.searchedSiteTypes.map((s: SiteType) => s.name)
          },
          {
            name: 'site_type_uri',
            op: 'in_',
            val: this.searchedSiteTypes.map((s: SiteType) => s.uri)
          }
        ]
      })
    }
  }

  async findById (id: string, includes: IncludedRelationships = {}): Promise<Site> {
    const include = getIncludeParams(includes)
    // set the permission groups for the serializer
    if (this.permissionFetcher) {
      this.serializer.permissionGroups = await this.permissionFetcher()
    }

    const rawResponse = await this.axiosApi.get(
      this.basePath + '/' + id,
      {
        params: {
          include
        }
      }
    )
    const rawData = rawResponse.data

    return siteWithMetaToSiteThrowingNoErrorOnMissing(
      this.serializer.convertJsonApiObjectToModel(rawData)
    )
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }

  archiveById (id: string): Promise<void> {
    return this.axiosApi.post(this.basePath + '/' + id + '/archive')
  }

  restoreById (id: string): Promise<void> {
    return this.axiosApi.post(this.basePath + '/' + id + '/restore')
  }

  save (site: Site) {
    const includeRelationships = false
    const data: any = this.serializer.convertModelToJsonApiData(site, includeRelationships)
    let method: Method = 'patch'
    let url = this.basePath

    if (site.id === '') {
      // new -> post
      method = 'post'
    } else {
      // old -> patch
      url += '/' + String(site.id)
    }

    return this.axiosApi.request({
      url,
      method,
      data: {
        data
      }
    }).then((serverAnswer) => {
      const answerData = serverAnswer.data

      return siteWithMetaToSiteThrowingNoErrorOnMissing(
        this.serializer.convertJsonApiObjectToModel(answerData))
    })
  }

  findRelatedContactRoles (siteId: string): Promise<ContactRole[]> {
    const url = this.basePath + '/' + siteId + '/site-contact-roles'
    const params = {
      'page[size]': 10000,
      include: 'contact'
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new ContactRoleSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  removeContact (siteContactRoleId: string): Promise<void> {
    const url = 'site-contact-roles/' + siteContactRoleId
    return this.axiosApi.delete(url)
  }

  addContact (siteId: string, contactRole: ContactRole): Promise<string> {
    const url = 'site-contact-roles'
    const data = new ContactRoleSerializer().convertModelToJsonApiData(contactRole, 'site_contact_role', 'site', siteId)
    return this.axiosApi.post(url, { data }).then(response => response.data.data.id)
  }
}
