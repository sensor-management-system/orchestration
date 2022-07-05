/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
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
import { Configuration } from '@/models/Configuration'
import { Contact } from '@/models/Contact'
import { Project } from '@/models/Project'
import { PermissionGroup } from '@/models/PermissionGroup'

import {
  ConfigurationSerializer,
  configurationWithMetaToConfigurationByAddingDummyObjects,
  configurationWithMetaToConfigurationByThrowingNoErrorOnMissing
} from '@/serializers/jsonapi/ConfigurationSerializer'

import { ContactSerializer } from '@/serializers/jsonapi/ContactSerializer'
import { DeviceMountActionApi } from '@/services/sms/DeviceMountActionApi'
import { DeviceUnmountActionApi } from '@/services/sms/DeviceUnmountActionApi'
import { PlatformMountActionApi } from '@/services/sms/PlatformMountActionApi'
import { PlatformUnmountActionApi } from '@/services/sms/PlatformUnmountActionApi'
import { StaticLocationBeginActionApi } from '@/services/sms/StaticLocationBeginActionApi'
import { StaticLocationEndActionApi } from '@/services/sms/StaticLocationEndActionApi'
import { DynamicLocationBeginActionApi } from '@/services/sms/DynamicLocationBeginActionApi'
import { DynamicLocationEndActionApi } from '@/services/sms/DynamicLocationEndActionApi'
import { StaticLocationBeginAction } from '@/models/StaticLocationBeginAction'
import { StaticLocationEndAction } from '@/models/StaticLocationEndAction'
import { DynamicLocationBeginAction } from '@/models/DynamicLocationBeginAction'
import { DynamicLocationEndAction } from '@/models/DynamicLocationEndAction'

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

export type ConfigurationPermissionFetchFunction = () => Promise<PermissionGroup[]>

export class ConfigurationApi {
  private axiosApi: AxiosInstance
  readonly basePath: string

  private _deviceMountActionApi: DeviceMountActionApi
  private _deviceUnmountActionApi: DeviceUnmountActionApi
  private _platformMountActionApi: PlatformMountActionApi
  private _platformUnmountActionApi: PlatformUnmountActionApi

  private _staticLocationBeginActionApi: StaticLocationBeginActionApi
  private _staticLocationEndActionApi: StaticLocationEndActionApi
  private _dynamicLocationBeginActionApi: DynamicLocationBeginActionApi
  private _dynamicLocationEndActionApi: DynamicLocationEndActionApi

  private _searchedProjects: Project[] = []
  private _searchedStates: string[] = []
  private _searchPermissionGroups: PermissionGroup[] = []
  private _searchText: string | null = null
  private _searchedUserMail: string | null = null
  private filterSettings: any[] = []

  private serializer: ConfigurationSerializer
  private permissionFetcher: ConfigurationPermissionFetchFunction | undefined

  constructor (
    axiosInstance: AxiosInstance,
    basePath: string,
    deviceMountActionApi: DeviceMountActionApi,
    deviceUnmountActionApi: DeviceUnmountActionApi,
    platformMountActionApi: PlatformMountActionApi,
    platformUnmountActionApi: PlatformUnmountActionApi,
    staticLocationBeginActionApi: StaticLocationBeginActionApi,
    staticLocationEndActionApi: StaticLocationEndActionApi,
    dynamicLocationBeginActionApi: DynamicLocationBeginActionApi,
    dynamicLocationEndActionApi: DynamicLocationEndActionApi,
    permissionFetcher?: ConfigurationPermissionFetchFunction
  ) {
    this.axiosApi = axiosInstance
    this.basePath = basePath

    this._deviceMountActionApi = deviceMountActionApi
    this._deviceUnmountActionApi = deviceUnmountActionApi
    this._platformMountActionApi = platformMountActionApi
    this._platformUnmountActionApi = platformUnmountActionApi

    this._staticLocationBeginActionApi = staticLocationBeginActionApi
    this._staticLocationEndActionApi = staticLocationEndActionApi
    this._dynamicLocationBeginActionApi = dynamicLocationBeginActionApi
    this._dynamicLocationEndActionApi = dynamicLocationEndActionApi

    this.serializer = new ConfigurationSerializer()

    if (permissionFetcher) {
      this.permissionFetcher = permissionFetcher
    }
  }

  get deviceMountActionApi (): DeviceMountActionApi {
    return this._deviceMountActionApi
  }

  get deviceUnmountActionApi (): DeviceUnmountActionApi {
    return this._deviceUnmountActionApi
  }

  get platformMountActionApi (): PlatformMountActionApi {
    return this._platformMountActionApi
  }

  get platformUnmountActionApi (): PlatformUnmountActionApi {
    return this._platformUnmountActionApi
  }

  get staticLocationBeginActionApi (): StaticLocationBeginActionApi {
    return this._staticLocationBeginActionApi
  }

  get staticLocationEndActionApi (): StaticLocationEndActionApi {
    return this._staticLocationEndActionApi
  }

  get dynamicLocationBeginActionApi (): DynamicLocationBeginActionApi {
    return this._dynamicLocationBeginActionApi
  }

  get dynamicLocationEndActionApi (): DynamicLocationEndActionApi {
    return this._dynamicLocationEndActionApi
  }

  get searchedProjects (): Project[] {
    return this._searchedProjects
  }

  setSearchedProjects (value: Project[]) {
    this._searchedProjects = value
    return this
  }

  get searchedStates (): string[] {
    return this._searchedStates
  }

  setSearchedStates (value: string[]) {
    this._searchedStates = value
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

  private get commonParams (): any {
    const result: any = {
      filter: JSON.stringify(this.filterSettings)
    }
    if (this.searchText) {
      result.q = this.searchText
    }
    result.sort = 'label'
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

  prepareSearch () {
    this.resetFilterSetting()
    this.prepareProjects()
    this.prepareStates()
    this.preparePermissionGroups()
    this.prepareMail()
  }

  resetFilterSetting () {
    this.filterSettings = []
  }

  prepareProjects () {
    if (this.searchedProjects.length > 0) {
      this.filterSettings.push({
        or: [
          {
            name: 'project_name',
            op: 'in_',
            val: this.searchedProjects.map((p: Project) => p.name)
          },
          {
            name: 'project_uri',
            op: 'in_',
            val: this.searchedProjects.map((p: Project) => p.uri)
          }
        ]
      })
    }
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

  async save (configuration: Configuration): Promise<Configuration> {
    const data: any = this.serializer.convertModelToJsonApiData(configuration)
    let method: Method = 'patch'
    let url = this.basePath
    // const relationshipsToDelete: string[] = []
    // let platformMountActionIdsToDelete: Set<string> = new Set()
    // let platformMountActionIdsToUpdate: Set<string> = new Set()
    // let platformUnmountActionIdsToDelete: Set<string> = new Set()
    // let platformUnmountActionIdsToUpdate: Set<string> = new Set()
    // let deviceMountActionIdsToDelete: Set<string> = new Set()
    // let deviceMountActionIdsToUpdate: Set<string> = new Set()
    // let deviceUnmountActionIdsToDelete: Set<string> = new Set()
    // let deviceUnmountActionIdsToUpdate: Set<string> = new Set()
    // let staticLocationBeginActionIdsToDelete: Set<string> = new Set()
    // let staticLocationBeginActionIdsToUpdate: Set<string> = new Set()
    // let staticLocationEndActionIdsToDelete: Set<string> = new Set()
    // let staticLocationEndActionIdsToUpdate: Set<string> = new Set()
    // let dynamicLocationBeginActionIdsToDelete: Set<string> = new Set()
    // let dynamicLocationBeginActionIdsToUpdate: Set<string> = new Set()
    // let dynamicLocationEndActionIdsToDelete: Set<string> = new Set()
    // let dynamicLocationEndActionIdsToUpdate: Set<string> = new Set()

    // step 1
    // load existing config to check current setting of the configuration

    // if (configuration.id) {
    //   const existingConfig = await this.findById(configuration.id)
    //   if (existingConfig.location instanceof DynamicLocation) {
    //     if (configuration.location instanceof DynamicLocation) {
    //       if (configuration.location.elevation == null && existingConfig.location.elevation !== null) {
    //         relationshipsToDelete.push('src-elevation')
    //       }
    //       if (configuration.location.latitude == null && existingConfig.location.latitude !== null) {
    //         relationshipsToDelete.push('src-latitude')
    //       }
    //       if (configuration.location.longitude == null && existingConfig.location.longitude !== null) {
    //         relationshipsToDelete.push('src-longitude')
    //       }
    //     } else {
    //       relationshipsToDelete.push('src-elevation')
    //       relationshipsToDelete.push('src-latitude')
    //       relationshipsToDelete.push('src-longitude')
    //     }
    //   }
    //   const newPlatformMountActionIds = new Set(configuration.platformMountActions.map(x => x.id))
    //   platformMountActionIdsToDelete = new Set(existingConfig.platformMountActions.map(x => x.id).filter(x => !newPlatformMountActionIds.has(x)))
    //   platformMountActionIdsToUpdate = new Set(existingConfig.platformMountActions.map(x => x.id).filter(x => newPlatformMountActionIds.has(x)))
    //   const newPlatformUnmountActionIds = new Set(configuration.platformUnmountActions.map(x => x.id))
    //   platformUnmountActionIdsToDelete = new Set(existingConfig.platformUnmountActions.map(x => x.id).filter(x => !newPlatformUnmountActionIds.has(x)))
    //   platformUnmountActionIdsToUpdate = new Set(existingConfig.platformUnmountActions.map(x => x.id).filter(x => newPlatformUnmountActionIds.has(x)))
    //
    //   const newDeviceMountActionIds = new Set(configuration.deviceMountActions.map(x => x.id))
    //   deviceMountActionIdsToDelete = new Set(existingConfig.deviceMountActions.map(x => x.id).filter(x => !newDeviceMountActionIds.has(x)))
    //   deviceMountActionIdsToUpdate = new Set(existingConfig.deviceMountActions.map(x => x.id).filter(x => newDeviceMountActionIds.has(x)))
    //   const newDeviceUnmountActionIds = new Set(configuration.deviceUnmountActions.map(x => x.id))
    //   deviceUnmountActionIdsToDelete = new Set(existingConfig.deviceUnmountActions.map(x => x.id).filter(x => !newDeviceUnmountActionIds.has(x)))
    //   deviceUnmountActionIdsToUpdate = new Set(existingConfig.deviceUnmountActions.map(x => x.id).filter(x => newDeviceUnmountActionIds.has(x)))
    //
    //   const newStaticLocationBeginActionIds = new Set(configuration.staticLocationBeginActions.map(x => x.id))
    //   staticLocationBeginActionIdsToDelete = new Set(existingConfig.staticLocationBeginActions.map(x => x.id).filter(x => !newStaticLocationBeginActionIds.has(x)))
    //   staticLocationBeginActionIdsToUpdate = new Set(existingConfig.staticLocationBeginActions.map(x => x.id).filter(x => newStaticLocationBeginActionIds.has(x)))
    //
    //   const newStaticLocationEndActionIds = new Set(configuration.staticLocationEndActions.map(x => x.id))
    //   staticLocationEndActionIdsToDelete = new Set(existingConfig.staticLocationEndActions.map(x => x.id).filter(x => !newStaticLocationEndActionIds.has(x)))
    //   staticLocationEndActionIdsToUpdate = new Set(existingConfig.staticLocationEndActions.map(x => x.id).filter(x => newStaticLocationEndActionIds.has(x)))
    //
    //   const newDynamicLocationBeginActionIds = new Set(configuration.dynamicLocationBeginActions.map(x => x.id))
    //   dynamicLocationBeginActionIdsToDelete = new Set(existingConfig.dynamicLocationBeginActions.map(x => x.id).filter(x => !newDynamicLocationBeginActionIds.has(x)))
    //   dynamicLocationBeginActionIdsToUpdate = new Set(existingConfig.dynamicLocationBeginActions.map(x => x.id).filter(x => newDynamicLocationBeginActionIds.has(x)))
    //
    //   const newDynamicLocationEndActionIds = new Set(configuration.dynamicLocationEndActions.map(x => x.id))
    //   dynamicLocationEndActionIdsToDelete = new Set(existingConfig.dynamicLocationEndActions.map(x => x.id).filter(x => !newDynamicLocationEndActionIds.has(x)))
    //   dynamicLocationEndActionIdsToUpdate = new Set(existingConfig.dynamicLocationEndActions.map(x => x.id).filter(x => newDynamicLocationEndActionIds.has(x)))
    // }

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
    // const configurationId = serverAnswer.data.data.id
    // const promisesDelete = []
    // for (const deviceMountActionId of deviceMountActionIdsToDelete) {
    //   promisesDelete.push(this._deviceMountActionApi.deleteById(deviceMountActionId))
    // }
    // for (const deviceUnmontActionId of deviceUnmountActionIdsToDelete) {
    //   promisesDelete.push(this._deviceUnmountActionApi.deleteById(deviceUnmontActionId))
    // }
    // for (const platformMountActionId of platformMountActionIdsToDelete) {
    //   promisesDelete.push(this._platformMountActionApi.deleteById(platformMountActionId))
    // }
    // for (const platformUnmountActionId of platformUnmountActionIdsToDelete) {
    //   promisesDelete.push(this._platformUnmountActionApi.deleteById(platformUnmountActionId))
    // }
    // for (const staticLocationBeginActionId of staticLocationBeginActionIdsToDelete) {
    //   promisesDelete.push(this._staticLocationBeginActionApi.deleteById(staticLocationBeginActionId))
    // }
    // for (const staticLocationEndActionId of staticLocationEndActionIdsToDelete) {
    //   promisesDelete.push(this._staticLocationEndActionApi.deleteById(staticLocationEndActionId))
    // }
    // for (const dynamicLocationBeginActionId of dynamicLocationBeginActionIdsToDelete) {
    //   promisesDelete.push(this._dynamicLocationBeginActionApi.deleteById(dynamicLocationBeginActionId))
    // }
    // for (const dynamicLocationEndActionId of dynamicLocationEndActionIdsToDelete) {
    //   promisesDelete.push(this._dynamicLocationEndActionApi.deleteById(dynamicLocationEndActionId))
    // }
    // relationshipsToDelete.forEach(relationship => promisesDelete.push(this.tryToDeleteRelationship(relationship, configurationId)))
    //
    // await Promise.all(promisesDelete)
    //
    // // now we need to add the new ones
    // const promisesSave = []
    // for (const platformMountAction of configuration.platformMountActions) {
    //   if (!platformMountAction.id) {
    //     promisesSave.push(this._platformMountActionApi.add(configurationId, platformMountAction))
    //   } else if (platformMountActionIdsToUpdate.has(platformMountAction.id)) {
    //     promisesSave.push(this._platformMountActionApi.update(configurationId, platformMountAction))
    //   }
    // }
    // for (const platformUnmountAction of configuration.platformUnmountActions) {
    //   if (!platformUnmountAction.id) {
    //     promisesSave.push(this._platformUnmountActionApi.add(configurationId, platformUnmountAction))
    //   } else if (platformUnmountActionIdsToUpdate.has(platformUnmountAction.id)) {
    //     promisesSave.push(this._platformUnmountActionApi.update(configurationId, platformUnmountAction))
    //   }
    // }
    // for (const deviceMountAction of configuration.deviceMountActions) {
    //   if (!deviceMountAction.id) {
    //     promisesSave.push(this._deviceMountActionApi.add(configurationId, deviceMountAction))
    //   } else if (deviceMountActionIdsToUpdate.has(deviceMountAction.id)) {
    //     promisesSave.push(this._deviceMountActionApi.update(configurationId, deviceMountAction))
    //   }
    // }
    // for (const deviceUnmountAction of configuration.deviceUnmountActions) {
    //   if (!deviceUnmountAction.id) {
    //     promisesSave.push(this._deviceUnmountActionApi.add(configurationId, deviceUnmountAction))
    //   } else if (deviceUnmountActionIdsToUpdate.has(deviceUnmountAction.id)) {
    //     promisesSave.push(this._deviceUnmountActionApi.update(configurationId, deviceUnmountAction))
    //   }
    // }
    // for (const staticLocationBeginAction of configuration.staticLocationBeginActions) {
    //   if (!staticLocationBeginAction.id) {
    //     promisesSave.push(this._staticLocationBeginActionApi.add(configurationId, staticLocationBeginAction))
    //   } else if (staticLocationBeginActionIdsToUpdate.has(staticLocationBeginAction.id)) {
    //     promisesSave.push(this._staticLocationBeginActionApi.update(configurationId, staticLocationBeginAction))
    //   }
    // }
    // for (const staticLocationEndAction of configuration.staticLocationEndActions) {
    //   if (!staticLocationEndAction.id) {
    //     promisesSave.push(this._staticLocationEndActionApi.add(configurationId, staticLocationEndAction))
    //   } else if (staticLocationEndActionIdsToUpdate.has(staticLocationEndAction.id)) {
    //     promisesSave.push(this._staticLocationEndActionApi.update(configurationId, staticLocationEndAction))
    //   }
    // }
    // for (const dynamicLocationBeginAction of configuration.dynamicLocationBeginActions) {
    //   if (!dynamicLocationBeginAction.id) {
    //     promisesSave.push(this._dynamicLocationBeginActionApi.add(configurationId, dynamicLocationBeginAction))
    //   } else if (dynamicLocationBeginActionIdsToUpdate.has(dynamicLocationBeginAction.id)) {
    //     promisesSave.push(this._dynamicLocationBeginActionApi.update(configurationId, dynamicLocationBeginAction))
    //   }
    // }
    // for (const dynamicLocationEndAction of configuration.dynamicLocationEndActions) {
    //   if (!dynamicLocationEndAction.id) {
    //     promisesSave.push(this._dynamicLocationEndActionApi.add(configurationId, dynamicLocationEndAction))
    //   } else if (dynamicLocationEndActionIdsToUpdate.has(dynamicLocationEndAction.id)) {
    //     promisesSave.push(this._dynamicLocationEndActionApi.update(configurationId, dynamicLocationEndAction))
    //   }
    // }
    // await Promise.all(promisesSave)

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

  // newSearchBuilder ()
  //   :
  //   ConfigurationSearchBuilder {
  //   return new ConfigurationSearchBuilder(this.axiosApi, this.basePath, this.serializer)
  // }

  findRelatedContacts (configurationId: string): Promise<Contact[]> {
    const url = this.basePath + '/' + configurationId + '/contacts'
    const params = {
      'page[size]': 10000
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new ContactSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  findRelatedStaticLocationBeginActions (configurationId: string): Promise<StaticLocationBeginAction> {
    const url = this.basePath + '/' + configurationId + '/static-location-begin-actions'
    const params = {
      'page[size]': 10000
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return rawServerResponse.data.data.map((apiData: any) => {
        return {
          id: apiData.id,
          beginDate: DateTime.fromISO(apiData.attributes.begin_date, { zone: 'UTC' }),
          description: apiData.attributes.description,
          epsgCode: apiData.attributes.epsg_code ?? '4326',
          x: apiData.attributes.x,
          y: apiData.attributes.y,
          z: apiData.attributes.z,
          elevationDatumName: apiData.attributes.elevation_datum_name ?? 'MSL',
          elevationDatumUri: apiData.attributes.elevation_datum_uri ?? ''
        }
      })
    })
  }

  findRelatedStaticLocationEndActions (configurationId: string): Promise<StaticLocationEndAction> {
    const url = this.basePath + '/' + configurationId + '/static-location-end-actions'
    const params = {
      'page[size]': 10000
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return rawServerResponse.data.data.map((apiData: any) => {
        return {
          id: apiData.id,
          description: apiData.attributes.description,
          endDate: apiData.attributes.end_data
        }
      })
    })
  }

  findRelatedDynamicLocationBeginActions (configurationId: string): Promise<DynamicLocationBeginAction> {
    const url = this.basePath + '/' + configurationId + '/dynamic-location-begin-action'
    const params = {
      'page[size]': 10000
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return rawServerResponse.data.data.map((apiData: any) => {
        return {
          id: apiData.id,
          beginDate: DateTime.fromISO(apiData.attributes.begin_date, { zone: 'UTC' }),
          description: apiData.attributes.description,
          epsgCode: apiData.attributes.epsg_code ?? '4326',
          elevationDatumName: apiData.attributes.elevation_datum_name ?? 'MSL',
          elevationDatumUri: apiData.attributes.elevation_datum_uri ?? '',
          contactId: apiData.relationships.contact.data.id
        }
      })
    })
  }

  findRelatedDynamicLocationEndActions (configurationId: string): Promise<DynamicLocationEndAction> {
    const url = this.basePath + '/' + configurationId + '/dynamic-location-end-actions'
    const params = {
      'page[size]': 10000
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return rawServerResponse.data.data.map((apiData: any) => {
        return {
          id: apiData.id,
          description: apiData.attributes.description,
          endDate: apiData.attributes.end_data
        }
      })
    })
  }

  // findRelatedDeviceMountActions(configurationId: string): Promise<DeviceMountAction>{
  //   const url = this.basePath + '/' + configurationId + '/device-mount-actions'
  //
  //
  //   const params = {
  //     'page[size]': 10000,
  //     include:'device,contact,parent_platform'
  //   }
  //   return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
  //
  //     const included = rawServerResponse.data.included
  //
  //     let includedContacts = included.filter((element:any) => element.type==='contact')
  //     let includedDevices = included.filter((element:any) => element.type==='device')
  //     // let includedContacts = included.filter((element:any) => element.type==='')
  //
  //     console.log('includedContacts',includedContacts);
  //     console.log('includedDevices',includedDevices);
  //
  //     return rawServerResponse.data.data.map((apiData: any)=>{
  //       let contactId = apiData.relationships.contact.data?.id
  //       let deviceId = apiData.relationships.device.data?.id
  //       let parentPlatformId = apiData.relationships.parent_platform.data?.id
  //
  //       let deviceData = includedDevices.find((element:any)=> element.id === deviceId)
  //       let contactData = includedContacts.find((element:any)=> element.id === contactId)
  //       //Todo parent platform
  //       let deviceWithMeta= new DeviceSerializer().convertJsonApiDataToModel(deviceData,[])
  //
  //       return {
  //         id: apiData.id,
  //         offsetX: apiData.attributes.offset_x,
  //         offsetY: apiData.attributes.offset_y,
  //         offsetZ: apiData.attributes.offset_z,
  //         description: apiData.attributes.description,
  //         date: DateTime.fromISO(apiData.attributes.begin_date, { zone: 'UTC' }),
  //         device:deviceWithMeta.device
  //       }
  //     })
  //   })
  // }
  // findRelatedPlatformMountActions(configurationId: string): Promise<PlatformMountAction>{
  //   const url = this.basePath + '/' + configurationId + '/platform-mount-actions'
  //   const params = {
  //     'page[size]': 10000,
  //     include:'platform,contact,parent_platform'
  //   }
  //   return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
  //     const included = rawServerResponse.data.included
  //     let includedContacts = included.filter((element:any) => element.type==='contact')
  //     let includedPlatforms = included.filter((element:any) => element.type==='platform')
  //
  //     return rawServerResponse.data.data.map((apiData: any)=>{
  //
  //       let contactId = apiData.relationships.contact.data?.id
  //       let platformId = apiData.relationships.platform.data?.id
  //       let parentPlatformId = apiData.relationships.parent_platform.data?.id
  //
  //       let platformData = includedPlatforms.find((element:any)=> element.id === platformId)
  //       let contactData = includedContacts.find((element:any)=> element.id === contactId)
  //       //Todo parent platform
  //       let paltformWithMeta= new PlatformSerializer().convertJsonApiDataToModel(platformData,[])
  //
  //
  //       return {
  //         id: apiData.id,
  //         offsetX: apiData.attributes.offset_x,
  //         offsetY: apiData.attributes.offset_y,
  //         offsetZ: apiData.attributes.offset_z,
  //         description: apiData.attributes.description,
  //         date: DateTime.fromISO(apiData.attributes.begin_date, { zone: 'UTC' }),
  //         platform:paltformWithMeta.platform
  //       }
  //     })
  //   })
  // }
  // findRelatedDeviceUnmountActions(configurationId: string): Promise<PlatformMountAction>{
  //   const url = this.basePath + '/' + configurationId + '/device-unmount-actions'
  //   const params = {
  //     'page[size]': 10000
  //   }
  //   return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
  //     return rawServerResponse.data.data.map((apiData: any)=>{
  //       return {
  //         id: apiData.id,
  //         description: apiData.attributes.description,
  //         date: DateTime.fromISO(apiData.attributes.end_date, { zone: 'UTC' }),
  //       }
  //     })
  //   })
  // }
  // findRelatedPlatformUnmountActions(configurationId: string): Promise<PlatformMountAction>{
  //   const url = this.basePath + '/' + configurationId + '/platform-unmount-actions'
  //   const params = {
  //     'page[size]': 10000
  //   }
  //   return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
  //     return rawServerResponse.data.data.map((apiData: any)=>{
  //       return {
  //         id: apiData.id,
  //         description: apiData.attributes.description,
  //         date: DateTime.fromISO(apiData.attributes.end_date, { zone: 'UTC' }),
  //       }
  //     })
  //   })
  // }

  removeContact (configurationId: string, contactId: string): Promise<void> {
    const url = this.basePath + '/' + configurationId + '/relationships/contacts'
    const params = {
      data: [{
        type: 'contact',
        id: contactId
      }]
    }
    return this.axiosApi.delete(url, { data: params })
  }

  addContact (configurationId: string, contactId: string): Promise<void> {
    const url = this.basePath + '/' + configurationId + '/relationships/contacts'
    const data = [{
      type: 'contact',
      id: contactId
    }]
    return this.axiosApi.post(url, { data })
  }
}

//
// export class ConfigurationSearchBuilder {
//   private axiosApi: AxiosInstance
//   readonly basePath: string
//
//   private clientSideFilterFunc: (configuration: Configuration) => boolean
//   private serverSideFilterSettings: IFlaskJSONAPIFilter[] = []
//   private esTextFilter: string | null = null
//   private serializer: ConfigurationSerializer
//
//   constructor (axiosApi: AxiosInstance, basePath: string, serializer: ConfigurationSerializer) {
//     this.axiosApi = axiosApi
//     this.basePath = basePath
//     this.clientSideFilterFunc = (_c: Configuration) => true
//     this.serializer = serializer
//   }
//
//   withText (text: string | null) {
//     if (text) {
//       this.esTextFilter = text
//     }
//     return this
//   }
//
//   withOneMatchingProjectOf (projects: Project[]) {
//     if (projects.length > 0) {
//       this.serverSideFilterSettings.push({
//         or: [
//           {
//             name: 'project_name',
//             op: 'in_',
//             val: projects.map((p: Project) => p.name)
//           },
//           {
//             name: 'project_uri',
//             op: 'in_',
//             val: projects.map((p: Project) => p.uri)
//           }
//         ]
//       })
//     }
//     return this
//   }
//
//   withOneLocationTypeOf (locationTypes: string[]) {
//     if (locationTypes.length > 0) {
//       this.serverSideFilterSettings.push({
//         name: 'location_type',
//         op: 'in_',
//         val: locationTypes
//       })
//     }
//     return this
//   }
//
//   withOneStatusOf (states: string[]) {
//     if (states.length > 0) {
//       this.serverSideFilterSettings.push({
//         name: 'status',
//         op: 'in_',
//         val: states
//       })
//     }
//     return this
//   }
//
//   withContactEmail (email: string) {
//     this.serverSideFilterSettings.push({
//       name: 'contacts.email',
//       op: 'eq',
//       val: email
//     })
//     return this
//   }

// build (): ConfigurationSearcher {
//   return new ConfigurationSearcher(
//     this.axiosApi,
//     this.basePath,
//     this.clientSideFilterFunc,
//     this.serverSideFilterSettings,
//     this.esTextFilter,
//     this.serializer
//   )
// }
// }

// export class ConfigurationSearcher {
//   private axiosApi: AxiosInstance
//   readonly basePath: string
//   private clientSideFilterFunc: (configuration: Configuration) => boolean
//   private serverSideFilterSettings: IFlaskJSONAPIFilter[]
//   private esTextFilter: string | null
//   private serializer: ConfigurationSerializer
//
//   constructor (
//     axiosApi: AxiosInstance,
//     basePath: string,
//     clientSideFilterFunc: (configuration: Configuration) => boolean,
//     serverSideFilterSettings: IFlaskJSONAPIFilter[],
//     esTextFilter: string | null,
//     serializer: ConfigurationSerializer
//   ) {
//     this.axiosApi = axiosApi
//     this.basePath = basePath
//     this.clientSideFilterFunc = clientSideFilterFunc
//     this.serverSideFilterSettings = serverSideFilterSettings
//     this.esTextFilter = esTextFilter
//     this.serializer = serializer
//   }
//
//   private get commonParams (): any {
//     const result: any = {
//       filter: JSON.stringify(this.serverSideFilterSettings)
//     }
//     if (this.esTextFilter != null) {
//       // In case we have a search string, then we want to
//       // sort by relevance (which is the default)
//       result.q = this.esTextFilter
//     } else {
//       // otherwise we want to search alphabetically
//       result.sort = 'label'
//     }
//     return result
//   }
//
//   findMatchingAsCsvBlob (): Promise<Blob> {
//     const url = this.basePath
//     return this.axiosApi.request({
//       url,
//       method: 'get',
//       headers: {
//         accept: 'text/csv'
//       },
//       params: {
//         'page[size]': 10000,
//         ...this.commonParams
//       }
//     }).then((response) => {
//       return new Blob([response.data], { type: 'text/csv;charset=utf-8' })
//     })
//   }
//
//   findMatchingAsList (): Promise<Configuration[]> {
//     return this.axiosApi.get(
//       this.basePath,
//       {
//         params: {
//           'page[size]': 100000,
//           ...this.commonParams
//         }
//       }
//     ).then((rawResponse: any) => {
//       const rawData = rawResponse.data
//       // We don't ask the api to load the contacts, so we just add dummy objects
//       // to stay with the relationships
//       return this.serializer
//         .convertJsonApiObjectListToModelList(rawData)
//         .map(configurationWithMetaToConfigurationByAddingDummyObjects)
//     })
//   }
//
//   findMatchingAsPaginationLoaderOnPage (page: number, pageSize: number): Promise<IPaginationLoader<Configuration>> {
//     return this.findAllOnPage(page, pageSize)
//   }
//
//   private findAllOnPage (page: number, pageSize: number): Promise<IPaginationLoader<Configuration>> {
//     return this.axiosApi.get(
//       this.basePath,
//       {
//         params: {
//           'page[size]': pageSize,
//           'page[number]': page,
//           ...this.commonParams
//         }
//       }
//     ).then((rawResponse) => {
//       const rawData = rawResponse.data
//       // And - again - we don't ask the api here to load the contact data as well
//       // so we will add the dummy objects to stay with the relationships
//       const elements: Configuration[] = this.serializer.convertJsonApiObjectListToModelList(
//         rawData
//       ).map(configurationWithMetaToConfigurationByAddingDummyObjects)
//
//       const totalCount = rawData.meta.count
//
//       // check if the provided page param is valid
//       if (totalCount > 0 && elements.length === 0) {
//         throw new RangeError('page is out of bounds')
//       }
//
//       let funToLoadNext = null
//       if (elements.length > 0) {
//         funToLoadNext = () => this.findAllOnPage(page + 1, pageSize)
//       }
//
//       let funToLoadPage = null
//       if (elements.length > 0) {
//         funToLoadPage = (pageNr: number) => this.findAllOnPage(pageNr, pageSize)
//       }
//
//       return {
//         elements,
//         totalCount,
//         page,
//         funToLoadNext,
//         funToLoadPage
//       }
//     })
//   }
// }
