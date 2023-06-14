/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2022
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
import { AxiosInstance, Method } from 'axios'

import { DateTime } from 'luxon'
import { Attachment } from '@/models/Attachment'
import { ContactRole } from '@/models/ContactRole'
import { Platform } from '@/models/Platform'
import { PlatformType } from '@/models/PlatformType'
import { Manufacturer } from '@/models/Manufacturer'
import { Status } from '@/models/Status'
import { PermissionGroup } from '@/models/PermissionGroup'

import { GenericAction } from '@/models/GenericAction'
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'
import { PlatformMountAction } from '@/models/views/platforms/actions/PlatformMountAction'

import { ContactRoleSerializer } from '@/serializers/jsonapi/ContactRoleSerializer'

import {
  PlatformSerializer,
  platformWithMetaToPlatformThrowingNoErrorOnMissing,
  platformWithMetaToPlatformByAddingDummyObjects
} from '@/serializers/jsonapi/PlatformSerializer'

import { PlatformAttachmentSerializer } from '@/serializers/jsonapi/PlatformAttachmentSerializer'

import { GenericPlatformActionSerializer } from '@/serializers/jsonapi/GenericActionSerializer'
import { PlatformSoftwareUpdateActionSerializer } from '@/serializers/jsonapi/SoftwareUpdateActionSerializer'
import { PlatformMountActionSerializer } from '@/serializers/jsonapi/composed/platforms/actions/PlatformMountActionSerializer'
import { Availability } from '@/models/Availability'
import { AvailabilitySerializer } from '@/serializers/controller/AvailabilitySerializer'

export interface IncludedRelationships {
  includeContacts?: boolean
  includePlatformAttachments?: boolean
  includeCreatedBy?: boolean
  includeUpdatedBy?: boolean
}

function getIncludeParams (includes: IncludedRelationships): string {
  const listIncludedRelationships: string[] = []
  if (includes.includeContacts) {
    listIncludedRelationships.push('contacts')
  }
  if (includes.includePlatformAttachments) {
    listIncludedRelationships.push('platform_attachments')
  }
  if (includes.includeCreatedBy) {
    listIncludedRelationships.push('created_by.contact')
  }
  if (includes.includeUpdatedBy) {
    listIncludedRelationships.push('updated_by.contact')
  }
  return listIncludedRelationships.join(',')
}

export type PlatformPermissionFetchFunction = () => Promise<PermissionGroup[]>

export class PlatformApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: PlatformSerializer
  private permissionFetcher: PlatformPermissionFetchFunction | undefined

  private _searchedManufacturers: Manufacturer[] = []
  private _searchedStates: Status[] = []
  private _searchedPlatformTypes: PlatformType[] = []
  private _searchedPermissionGroups: PermissionGroup[] = []
  private _searchedUserMail: string | null = null
  private _searchedCreatorId: string | null = null
  private _searchedIncludeArchivedPlatforms = false
  private _searchText: string | null = null
  private filterSettings: any[] = []

  constructor (axiosInstance: AxiosInstance, basePath: string, permissionFetcher?: PlatformPermissionFetchFunction) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
    this.serializer = new PlatformSerializer()
    if (permissionFetcher) {
      this.permissionFetcher = permissionFetcher
    }
  }

  get searchedManufacturers (): Manufacturer[] {
    return this._searchedManufacturers
  }

  setSearchedManufacturers (value: Manufacturer[]) {
    this._searchedManufacturers = value
    return this
  }

  get searchedStates (): Status[] {
    return this._searchedStates
  }

  setSearchedStates (value: Status[]) {
    this._searchedStates = value
    return this
  }

  get searchedPlatformTypes (): PlatformType[] {
    return this._searchedPlatformTypes
  }

  setSearchedPlatformTypes (value: PlatformType[]) {
    this._searchedPlatformTypes = value
    return this
  }

  get searchedPermissionGroups (): PermissionGroup[] {
    return this._searchedPermissionGroups
  }

  setSearchedPermissionGroups (value: PermissionGroup[]) {
    this._searchedPermissionGroups = value
    return this
  }

  get searchText (): string | null {
    return this._searchText
  }

  setSearchText (value: string | null) {
    this._searchText = value
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

  get searchIncludeArchivedPlatforms (): boolean {
    return this._searchedIncludeArchivedPlatforms
  }

  setSearchIncludeArchivedPlatforms (value: boolean) {
    this._searchedIncludeArchivedPlatforms = value
    return this
  }

  private get commonParams (): any {
    const result: any = {
      filter: JSON.stringify(this.filterSettings)
    }
    if (this.searchText) {
      result.q = this.searchText
    }
    result.sort = 'short_name'
    if (this.searchIncludeArchivedPlatforms) {
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
      // And - again - as we don't ask the api to include the contacts, we just handle
      // the missing contact data by adding dummy objects for those.
      const elements: Platform[] = this.serializer.convertJsonApiObjectListToModelList(
        rawData
      ).map(platformWithMetaToPlatformByAddingDummyObjects)

      // This is given by the json api. Regardless of the pagination it
      // represents the total amount of entries found.
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
          ...this.commonParams
        }
      }
    ).then((rawResponse: any) => {
      const rawData = rawResponse.data
      // We don't ask the api to load the contacts, so we just add dummy objects
      // to stay with the relationships
      return this.serializer
        .convertJsonApiObjectListToModelList(rawData)
        .map(platformWithMetaToPlatformByAddingDummyObjects)
    })
  }

  async getSensorML (platformId: string): Promise<Blob> {
    const url = this.basePath + '/' + platformId + '/sensorml'
    const response = await this.axiosApi.get(url)
    return new Blob([response.data], { type: 'text/xml' })
  }

  getSensorMLUrl (platformId: string): string {
    return this.axiosApi.defaults.baseURL + this.basePath + '/' + platformId + '/sensorml'
  }

  async searchRecentlyUpdated (amount: number) {
    this.prepareSearch()
    return await this.axiosApi.get(
      this.basePath,
      {
        params: {
          'page[size]': amount,
          'page[number]': 1,
          sort: '-updated_at',
          include: 'updated_by.contact',
          hide_archived: false
        }
      }

    ).then((rawResponse: any) => {
      const rawData = rawResponse.data
      // We don't ask the api to load the contacts, so we just add dummy objects
      // to stay with the relationships
      return this.serializer
        .convertJsonApiObjectListToModelList(rawData)
        .map(platformWithMetaToPlatformByAddingDummyObjects)
    })
  }

  searchMatchingAsCsvBlob (): Promise<Blob> {
    this.prepareSearch()

    const url = this.basePath
    return this.axiosApi.request({
      url,
      method: 'get',
      headers: {
        accept: 'text/csv'
      },
      params: {
        'page[size]': 10000,
        ...this.commonParams
      }
    }).then((response) => {
      // we use text/plain here to allow the easier display in the browser
      return new Blob([response.data], { type: 'text/plain;charset=utf-8' })
    })
  }

  prepareSearch () {
    this.resetFilterSetting()
    this.prepareManufacturers()
    this.prepareStates()
    this.prepareTypes()
    this.preparePermissionGroups()
    this.prepareMail()
    this.prepareCreator()
  }

  prepareMail () {
    if (this.searchedUserMail) {
      this.filterSettings.push({
        name: 'platform_contact_roles.contact.email',
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

  prepareManufacturers () {
    if (this.searchedManufacturers.length > 0) {
      this.filterSettings.push({
        or: [
          {
            name: 'manufacturer_name',
            op: 'in_',
            val: this.searchedManufacturers.map((m: Manufacturer) => m.name)
          },
          {
            name: 'manufacturer_uri',
            op: 'in_',
            val: this.searchedManufacturers.map((m: Manufacturer) => m.uri)
          }
        ]
      })
    }
  }

  prepareStates () {
    if (this.searchedStates.length > 0) {
      this.filterSettings.push({
        or: [
          {
            name: 'status_name',
            op: 'in_',
            val: this.searchedStates.map((s: Status) => s.name)
          },
          {
            name: 'status_uri',
            op: 'in_',
            val: this.searchedStates.map((s: Status) => s.uri)
          }
        ]
      })
    }
  }

  prepareTypes () {
    if (this.searchedPlatformTypes.length > 0) {
      this.filterSettings.push({
        or: [
          {
            name: 'platform_type_name',
            op: 'in_',
            val: this.searchedPlatformTypes.map((t: PlatformType) => t.name)
          },
          {
            name: 'platform_type_uri',
            op: 'in_',
            val: this.searchedPlatformTypes.map((t: PlatformType) => t.uri)
          }
        ]
      })
    }
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

  async findById (id: string, includes: IncludedRelationships): Promise<Platform> {
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
    // As we ask the api to include all the contacts, we want to have them here
    // if they are missing => throw an error
    return platformWithMetaToPlatformThrowingNoErrorOnMissing(this.serializer.convertJsonApiObjectToModel(rawData))
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

  save (platform: Platform): Promise<Platform> {
    // The relationships themselves will be added, updated & deleted in their
    // own tabs and in their own services.
    // If we would include them here (without fetching them before), we would
    // delete them. So we will skip them in order to keep them in the backend.
    const includeRelationships = false
    const data:
      any = this.serializer.convertModelToJsonApiData(platform, includeRelationships)
    let method: Method = 'patch'
    let url = this.basePath

    if (platform.id === null) {
      // new -> post
      method = 'post'
    } else {
      // old -> patch
      url += '/' + String(platform.id)
    }

    // TODO: links for contacts
    return this.axiosApi.request({
      url,
      method,
      data: {
        data
      }
    }).then((serverAnswer) => {
      const answerData = serverAnswer.data
      return platformWithMetaToPlatformThrowingNoErrorOnMissing(
        this.serializer.convertJsonApiObjectToModel(answerData))
    })
  }

  findRelatedContactRoles (platformId: string):
    Promise<ContactRole[]> {
    const url = this.basePath + '/' + platformId + '/platform-contact-roles'
    const params = {
      'page[size]': 10000,
      include: 'contact'
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new ContactRoleSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  findRelatedPlatformAttachments (platformId: string): Promise<Attachment[]> {
    const url = this.basePath + '/' + platformId + '/platform-attachments'
    const params = {
      'page[size]': 10000
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new PlatformAttachmentSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  findRelatedGenericActions (platformId: string): Promise<GenericAction[]> {
    const url = this.basePath + '/' + platformId + '/generic-platform-actions'
    const params = {
      'page[size]': 10000,
      include: [
        'contact',
        'generic_platform_action_attachments.attachment'
      ].join(',')
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new GenericPlatformActionSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  findRelatedSoftwareUpdateActions (platformId: string): Promise<SoftwareUpdateAction[]> {
    const url = this.basePath + '/' + platformId + '/platform-software-update-actions'
    const params = {
      'page[size]': 10000,
      include: [
        'contact',
        'platform_software_update_action_attachments.attachment'
      ].join(',')
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new PlatformSoftwareUpdateActionSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  findRelatedMountActions (platformId: string): Promise<PlatformMountAction[]> {
    const url = this.basePath + '/' + platformId + '/platform-mount-actions'
    const params = {
      'page[size]': 10000,
      include: [
        'begin_contact',
        'end_contact',
        'parent_platform',
        'configuration'
      ].join(',')
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new PlatformMountActionSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  removeContact (platformContactRoleId: string): Promise<void> {
    const url = 'platform-contact-roles/' + platformContactRoleId
    return this.axiosApi.delete(url)
  }

  addContact (platformId: string, contactRole: ContactRole): Promise<string> {
    const url = 'platform-contact-roles'
    const data = new ContactRoleSerializer().convertModelToJsonApiData(contactRole, 'platform_contact_role', 'platform', platformId)
    return this.axiosApi.post(url, { data }).then(response => response.data.data.id)
  }

  checkAvailability (ids: (string | null)[], from: DateTime, to: DateTime | null): Promise<Availability[]> {
    const url = '/controller/platform-availabilities'
    const params = {
      ids: ids ? ids.join(',') : '',
      from: from.toISO(),
      to: to ? to.toISO() : ''
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new AvailabilitySerializer().convertJsonApiObjectListToModelList(rawServerResponse)
    })
  }
}
