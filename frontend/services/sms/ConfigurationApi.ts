/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
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

// eslint-disable-next-line
import { AxiosInstance, Method } from 'axios'

import { DateTime } from 'luxon'

import { Attachment } from '@/models/Attachment'
import { Configuration } from '@/models/Configuration'
import { ConfigurationMountingAction } from '@/models/ConfigurationMountingAction'
import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { Contact } from '@/models/Contact'
import { ContactRole } from '@/models/ContactRole'
import { CustomTextField } from '@/models/CustomTextField'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import { GenericAction } from '@/models/GenericAction'
import { Parameter } from '@/models/Parameter'
import { ParameterChangeAction } from '@/models/ParameterChangeAction'
import { PermissionGroup } from '@/models/PermissionGroup'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { Site } from '@/models/Site'
import { StaticLocationAction } from '@/models/StaticLocationAction'
import { TsmLinking } from '@/models/TsmLinking'

import { DeviceMountActionApi } from '@/services/sms/DeviceMountActionApi'
import { DynamicLocationActionApi } from '@/services/sms/DynamicLocationActionApi'
import { LocationActionTimepointControllerApi } from '@/services/sms/LocationActionTimepointControllerApi'
import { MountingActionsControllerApi } from '@/services/sms/MountingActionsControllerApi'
import { PlatformMountActionApi } from '@/services/sms/PlatformMountActionApi'
import { StaticLocationActionApi } from '@/services/sms/StaticLocationActionApi'
import { TsmLinkingApi } from '@/services/sms/TsmLinkingApi'

import {
  ConfigurationSerializer,
  configurationWithMetaToConfigurationByAddingDummyObjects,
  configurationWithMetaToConfigurationByThrowingNoErrorOnMissing
} from '@/serializers/jsonapi/ConfigurationSerializer'
import { ConfigurationAttachmentSerializer } from '@/serializers/jsonapi/ConfigurationAttachmentSerializer'
import { ContactRoleSerializer } from '@/serializers/jsonapi/ContactRoleSerializer'
import { CustomTextFieldSerializer, CustomTextFieldEntityType } from '@/serializers/jsonapi/CustomTextFieldSerializer'
import { GenericConfigurationActionSerializer } from '@/serializers/jsonapi/GenericActionSerializer'
import { ILocationTimepoint } from '@/serializers/controller/LocationActionTimepointSerializer'
import { ParameterChangeActionSerializer, ParameterChangeActionEntityType } from '@/serializers/jsonapi/ParameterChangeActionSerializer'
import { ParameterSerializer, ParameterEntityType } from '@/serializers/jsonapi/ParameterSerializer'

export interface IncludedRelationships {
  includeContacts?: boolean
  includeConfigurationParameters?: boolean
  includeCreatedBy?: boolean
  includeUpdatedBy?: boolean
}

function getIncludeParams (includes: IncludedRelationships): string {
  const listIncludedRelationships: string[] = []
  if (includes.includeContacts) {
    listIncludedRelationships.push('contacts')
  }
  if (includes.includeConfigurationParameters) {
    listIncludedRelationships.push('configuration_parameters')
  }
  if (includes.includeCreatedBy) {
    listIncludedRelationships.push('created_by.contact')
  }
  if (includes.includeUpdatedBy) {
    listIncludedRelationships.push('updated_by.contact')
  }
  return listIncludedRelationships.join(',')
}

export type ConfigurationPermissionFetchFunction = () => Promise<PermissionGroup[]>

export class ConfigurationApi {
  private axiosApi: AxiosInstance
  readonly basePath: string

  private _deviceMountActionApi: DeviceMountActionApi
  private _platformMountActionApi: PlatformMountActionApi

  private _staticLocationActionApi: StaticLocationActionApi
  private _dynamicLocationActionApi: DynamicLocationActionApi
  private _locationActionTimepointControllerApi: LocationActionTimepointControllerApi
  private _mountingActionsControllerApi: MountingActionsControllerApi

  private _tsmLinkingApi: TsmLinkingApi

  private _searchedStates: string[] = []
  private _searchedProjects: string[] = []
  private _searchedSites: Site[] = []
  private _searchPermissionGroups: PermissionGroup[] = []
  private _searchText: string | null = null
  private _searchedUserMail: string | null = null
  private _searchedIncludeArchivedConfigurations: boolean = false
  private filterSettings: any[] = []

  private serializer: ConfigurationSerializer
  private permissionFetcher: ConfigurationPermissionFetchFunction | undefined

  constructor (
    axiosInstance: AxiosInstance,
    basePath: string,
    deviceMountActionApi: DeviceMountActionApi,
    platformMountActionApi: PlatformMountActionApi,
    staticLocationActionApi: StaticLocationActionApi,
    dynamicLocationActionApi: DynamicLocationActionApi,
    locationActionTimepointControllerApi: LocationActionTimepointControllerApi,
    mountingActionsControllerApi: MountingActionsControllerApi,
    tsmLinkingApi: TsmLinkingApi,
    permissionFetcher?: ConfigurationPermissionFetchFunction
  ) {
    this.axiosApi = axiosInstance
    this.basePath = basePath

    this._deviceMountActionApi = deviceMountActionApi
    this._platformMountActionApi = platformMountActionApi

    this._staticLocationActionApi = staticLocationActionApi
    this._dynamicLocationActionApi = dynamicLocationActionApi
    this._locationActionTimepointControllerApi = locationActionTimepointControllerApi
    this._mountingActionsControllerApi = mountingActionsControllerApi

    this._tsmLinkingApi = tsmLinkingApi

    this.serializer = new ConfigurationSerializer()

    if (permissionFetcher) {
      this.permissionFetcher = permissionFetcher
    }
  }

  get deviceMountActionApi (): DeviceMountActionApi {
    return this._deviceMountActionApi
  }

  get platformMountActionApi (): PlatformMountActionApi {
    return this._platformMountActionApi
  }

  get staticLocationActionApi (): StaticLocationActionApi {
    return this._staticLocationActionApi
  }

  get dynamicLocationActionApi (): DynamicLocationActionApi {
    return this._dynamicLocationActionApi
  }

  get locationActionTimepointControllerApi (): LocationActionTimepointControllerApi {
    return this._locationActionTimepointControllerApi
  }

  get mountingActionsControllerApi (): MountingActionsControllerApi {
    return this._mountingActionsControllerApi
  }

  get searchedStates (): string[] {
    return this._searchedStates
  }

  get tsmLinkingApi (): TsmLinkingApi {
    return this._tsmLinkingApi
  }

  setSearchedStates (value: string[]) {
    this._searchedStates = value
    return this
  }

  get searchedProjects (): string[] {
    return this._searchedProjects
  }

  setSearchedProjects (value: string[]) {
    this._searchedProjects = value
    return this
  }

  get searchedSites (): Site[] {
    return this._searchedSites
  }

  setSearchedSites (value: Site[]) {
    this._searchedSites = value
    return this
  }

  get searchedPermissionGroups (): PermissionGroup[] {
    return this._searchPermissionGroups
  }

  setSearchPermissionGroups (value: PermissionGroup[]) {
    this._searchPermissionGroups = value
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

  get searchIncludeArchivedConfigurations (): boolean {
    return this._searchedIncludeArchivedConfigurations
  }

  setSearchIncludeArchivedConfigurations (value: boolean) {
    this._searchedIncludeArchivedConfigurations = value
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
    if (this.searchIncludeArchivedConfigurations) {
      result.hide_archived = false
    }
    return result
  }

  async searchPaginated (pageNumber: number, pageSize: number, includes: IncludedRelationships = {}) {
    this.prepareSearch()

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
      // And - again - we don't ask the api here to load the contact data as well
      // so we will add the dummy objects to stay with the relationships
      const elements: Configuration[] = this.serializer.convertJsonApiObjectListToModelList(
        rawData
      ).map(configurationWithMetaToConfigurationByAddingDummyObjects)

      const totalCount = rawData.meta.count

      return {
        elements,
        totalCount
      }
    })
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
          hide_archived: false,
          filter: JSON.stringify([{ name: 'updated_at', op: 'ne', val: null }])
        }
      }

    ).then((rawResponse: any) => {
      const rawData = rawResponse.data
      // We don't ask the api to load the contacts, so we just add dummy objects
      // to stay with the relationships
      return this.serializer
        .convertJsonApiObjectListToModelList(rawData)
        .map(configurationWithMetaToConfigurationByAddingDummyObjects)
    })
  }

  prepareSearch () {
    this.resetFilterSetting()
    this.prepareStates()
    this.prepareProjects()
    this.prepareSites()
    this.preparePermissionGroups()
    this.prepareMail()
  }

  async getSensorML (configurationId: string): Promise<Blob> {
    const url = this.basePath + '/' + configurationId + '/sensorml'
    const response = await this.axiosApi.get(url)
    return new Blob([response.data], { type: 'text/xml' })
  }

  getSensorMLUrl (configurationId: string): string {
    return this.axiosApi.defaults.baseURL + this.basePath + '/' + configurationId + '/sensorml'
  }

  resetFilterSetting () {
    this.filterSettings = []
  }

  prepareStates () {
    if (this.searchedStates.length > 0) {
      this.filterSettings.push({
        name: 'status',
        op: 'in_',
        val: this.searchedStates
      })
    }
  }

  prepareProjects () {
    if (this.searchedProjects.length > 0) {
      this.filterSettings.push({
        name: 'project',
        op: 'in_',
        val: this.searchedProjects
      })
    }
  }

  preparePermissionGroups () {
    if (this.searchedPermissionGroups.length > 0) {
      this.filterSettings.push({
        or: this.searchedPermissionGroups.map((permissionGroup) => {
          return {
            name: 'cfg_permission_group',
            op: 'eq',
            val: permissionGroup.id
          }
        })
      })
    }
  }

  prepareSites () {
    if (this.searchedSites.length > 0) {
      this.filterSettings.push({
        name: 'site_id',
        op: 'in_',
        val: this.searchedSites.map(s => s.id)
      })
    }
  }

  prepareMail () {
    if (this.searchedUserMail) {
      this.filterSettings.push({
        name: 'contacts.email',
        op: 'eq',
        val: this.searchedUserMail
      })
    }
  }

  async findById (id: string, includes: IncludedRelationships = {}): Promise<Configuration> {
    if (this.permissionFetcher) {
      this.serializer.permissionGroups = await this.permissionFetcher()
    }

    const include = getIncludeParams(includes)
    return this.axiosApi.get(this.basePath + '/' + id, {
      params: {
        include
      }
    }).then((rawResponse) => {
      const rawData = rawResponse.data
      // return configurationWithMetaToConfigurationByThrowingErrorOnMissing(this.serializer.convertJsonApiObjectToModel(rawData))
      return configurationWithMetaToConfigurationByThrowingNoErrorOnMissing(this.serializer.convertJsonApiObjectToModel(rawData))
    })
  }

  // eslint-disable-next-line
  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }

  archiveById (id: string): Promise<void> {
    return this.axiosApi.post(this.basePath + '/' + id + '/archive')
  }

  restoreById (id: string): Promise<void> {
    return this.axiosApi.post(this.basePath + '/' + id + '/restore')
  }

  async save (configuration: Configuration): Promise<Configuration> {
    const data: any = this.serializer.convertModelToJsonApiData(configuration)
    let method: Method = 'patch'
    let url = this.basePath

    if (!configuration.id) {
      method = 'post'
    } else {
      url += '/' + configuration.id
    }
    const serverAnswer = await this.axiosApi.request({
      url,
      method,
      data: {
        data
      }
    })

    return this.findById(serverAnswer.data.data.id)
  }

  private async tryToDeleteRelationship (relationshipToDelete: string, id: string) {
    const url = this.basePath + '/' + id + '/relationships/' + relationshipToDelete

    let relationshipTypeToDelete: string | null = null
    let relationshipIdToDelete: string | null = null

    try {
      const getResponse = await this.axiosApi.get(url)
      relationshipTypeToDelete = getResponse.data.data.type
      relationshipIdToDelete = getResponse.data.data.id
      // if there is no element, the id may still be null
    } catch (_errorFromGet) {
      // We can ignore the error here
      // as we will not try to delete relationships
      // that don't exist
      //
      // the if check will make sure we only go on
      // with deleting for those relationships that exist
    }

    if (relationshipTypeToDelete != null && relationshipIdToDelete != null) {
      // Please note: We don't have a try/catch block here
      // as we want the exception - in case we can't delete
      // an existing relationship.
      await this.axiosApi.request({
        url,
        method: 'delete',
        data: {
          data: {
            type: relationshipTypeToDelete,
            id: relationshipIdToDelete
          }
        }
      })
    }
  }

  findRelatedContactRoles (configurationId: string): Promise<ContactRole[]> {
    const url = this.basePath + '/' + configurationId + '/configuration-contact-roles'
    const params = {
      'page[size]': 10000,
      include: 'contact'
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new ContactRoleSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  async findRelatedLocationActions (configurationId: string): Promise<ILocationTimepoint[]> {
    return await this.locationActionTimepointControllerApi.findLocationActions(configurationId)
  }

  async findRelatedMountingActions (configurationId: string): Promise<ConfigurationMountingAction[]> {
    const response = await this.mountingActionsControllerApi.findMountingActions(configurationId)
    return response
  }

  async findRelatedMountingActionsByDate (configurationId: string, timepoint: DateTime, contacts: Contact[]): Promise<ConfigurationsTree> {
    return await this.mountingActionsControllerApi.findMountingActionsByDate(configurationId, timepoint, contacts)
  }

  async findRelatedDeviceMountActions (configurationId: string): Promise<DeviceMountAction[]> {
    return await this.deviceMountActionApi.getRelatedActions(configurationId)
  }

  async findRelatedDeviceMountActionsIncludingDeviceInformation (configurationId: string): Promise<DeviceMountAction[]> {
    return await this.deviceMountActionApi.getRelatedActionsIncludingDeviceInformation(configurationId)
  }

  async findRelatedPlatformMountActions (configurationId: string): Promise<PlatformMountAction[]> {
    return await this.platformMountActionApi.getRelatedActions(configurationId)
  }

  async findRelatedDynamicLocationActions (configurationId: string): Promise<DynamicLocationAction[]> {
    return await this.dynamicLocationActionApi.getRelatedActions(configurationId)
  }

  async findRelatedStaticLocationActions (configurationId: string): Promise<StaticLocationAction[]> {
    return await this.staticLocationActionApi.getRelatedActions(configurationId)
  }

  async findRelatedConfigurationAttachments (configurationId: string): Promise<Attachment[]> {
    const url = this.basePath + '/' + configurationId + '/configuration-attachments'
    const params = {
      'page[size]': 10000
    }
    return await this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new ConfigurationAttachmentSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  findRelatedConfigurationCustomFields (configurationId: string): Promise<CustomTextField[]> {
    const url = this.basePath + '/' + configurationId + '/configuration-customfields'
    const params = {
      'page[size]': 10000
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new CustomTextFieldSerializer(CustomTextFieldEntityType.CONFIGURATION).convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  async findRelatedGenericActions (configurationId: string): Promise<GenericAction[]> {
    const url = this.basePath + '/' + configurationId + '/generic-configuration-actions'
    const params = {
      'page[size]': 10000,
      include: [
        'contact',
        'generic_configuration_action_attachments.attachment'
      ].join(',')
    }
    const result = await this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new GenericConfigurationActionSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
    return result
  }

  async findRelatedTsmLinkings (configurationId: string): Promise<TsmLinking[]> {
    return await this._tsmLinkingApi.getRelatedTsmLinkings(configurationId)
  }

  removeContact (configurationContactRoleId: string): Promise<void> {
    const url = 'configuration-contact-roles/' + configurationContactRoleId
    return this.axiosApi.delete(url)
  }

  addContact (configurationId: string, contactRole: ContactRole): Promise<string> {
    const url = 'configuration-contact-roles'
    const data = new ContactRoleSerializer().convertModelToJsonApiData(contactRole, 'configuration_contact_role', 'configuration', configurationId)
    return this.axiosApi.post(url, { data }).then(response => response.data.data.id)
  }

  async findRelatedConfigurationParameters (configurationId: string): Promise<Parameter[]> {
    const url = this.basePath + '/' + configurationId + '/configuration-parameters'
    const params = {
      'page[size]': 10000,
      // The one that was created first, should be first. All others behind.
      sort: 'created_at'
    }
    const response = await this.axiosApi.get(url, { params })
    return new ParameterSerializer(ParameterEntityType.CONFIGURATION).convertJsonApiObjectListToModelList(response.data)
  }

  async findRelatedParameterChangeActions (configurationId: string): Promise<ParameterChangeAction[]> {
    const url = this.basePath + '/' + configurationId + '/configuration-parameter-value-change-actions'
    const params = {
      'page[size]': 10000,
      include: [
        'contact',
        'configuration_parameter'
      ].join(','),
      // The one with the smallest date first. All others behind.
      sort: 'date'
    }
    const response = await this.axiosApi.get(url, { params })
    return new ParameterChangeActionSerializer(ParameterChangeActionEntityType.CONFIGURATION_PARAMETER_VALUE_CHANGE).convertJsonApiObjectListToModelList(response.data)
  }
}
