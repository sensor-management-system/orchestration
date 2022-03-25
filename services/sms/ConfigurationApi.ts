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

import { Configuration } from '@/models/Configuration'
import { Contact } from '@/models/Contact'
import { DynamicLocation } from '@/models/Location'
import { Project } from '@/models/Project'

// eslint-disable-next-line
import { IFlaskJSONAPIFilter } from '@/utils/JSONApiInterfaces'

import {
  IPaginationLoader
} from '@/utils/PaginatedLoader'

import {
  ConfigurationSerializer,
  configurationWithMetaToConfigurationByAddingDummyObjects,
  configurationWithMetaToConfigurationByThrowingErrorOnMissing
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

export class ConfigurationApi {
  private axiosApi: AxiosInstance
  readonly basePath: string

  private deviceMountActionApi: DeviceMountActionApi
  private deviceUnmountActionApi: DeviceUnmountActionApi
  private platformMountActionApi: PlatformMountActionApi
  private platformUnmountActionApi: PlatformUnmountActionApi

  private staticLocationBeginActionApi: StaticLocationBeginActionApi
  private staticLocationEndActionApi: StaticLocationEndActionApi
  private dynamicLocationBeginActionApi: DynamicLocationBeginActionApi
  private dynamicLocationEndActionApi: DynamicLocationEndActionApi

  private serializer: ConfigurationSerializer

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
    dynamicLocationEndActionApi: DynamicLocationEndActionApi
  ) {
    this.axiosApi = axiosInstance
    this.basePath = basePath

    this.deviceMountActionApi = deviceMountActionApi
    this.deviceUnmountActionApi = deviceUnmountActionApi
    this.platformMountActionApi = platformMountActionApi
    this.platformUnmountActionApi = platformUnmountActionApi

    this.staticLocationBeginActionApi = staticLocationBeginActionApi
    this.staticLocationEndActionApi = staticLocationEndActionApi
    this.dynamicLocationBeginActionApi = dynamicLocationBeginActionApi
    this.dynamicLocationEndActionApi = dynamicLocationEndActionApi

    this.serializer = new ConfigurationSerializer()
  }

  findById (id: string): Promise<Configuration> {
    return this.axiosApi.get(this.basePath + '/' + id, {
      params: {
        include: [
          'contacts',
          'src_longitude',
          'src_latitude',
          'src_elevation',
          'device_mount_actions',
          'device_unmount_actions',
          'platform_mount_actions',
          'platform_unmount_actions',
          'configuration_static_location_begin_actions',
          'configuration_static_location_end_actions',
          'configuration_dynamic_location_begin_actions',
          'configuration_dynamic_location_end_actions',
          'platform_mount_actions.platform',
          'device_mount_actions.device',
          'device_mount_actions.device.device_properties',
          'device_mount_actions.contact',
          'platform_mount_actions.contact',
          'platform_unmount_actions.contact',
          'device_unmount_actions.contact',
          'configuration_static_location_begin_actions.contact',
          'configuration_static_location_end_actions.contact',
          'configuration_dynamic_location_begin_actions.contact',
          'configuration_dynamic_location_end_actions.contact',
          'configuration_dynamic_location_begin_actions.x_property',
          'configuration_dynamic_location_begin_actions.y_property',
          'configuration_dynamic_location_begin_actions.z_property'
          // devices of the dynamic location properties must be
          // part of mounted devices
        ].join(',')
      }
    }).then((rawResponse) => {
      const rawData = rawResponse.data
      return configurationWithMetaToConfigurationByThrowingErrorOnMissing(this.serializer.convertJsonApiObjectToModel(rawData))
    })
  }

  // eslint-disable-next-line
  deleteById (id: string) : Promise<void> {
    return this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }

  async save (configuration: Configuration): Promise<Configuration> {
    const data: any = this.serializer.convertModelToJsonApiData(configuration)
    let method: Method = 'patch'
    let url = this.basePath
    const relationshipsToDelete: string[] = []
    let platformMountActionIdsToDelete: Set<string> = new Set()
    let platformMountActionIdsToUpdate: Set<string> = new Set()
    let platformUnmountActionIdsToDelete: Set<string> = new Set()
    let platformUnmountActionIdsToUpdate: Set<string> = new Set()
    let deviceMountActionIdsToDelete: Set<string> = new Set()
    let deviceMountActionIdsToUpdate: Set<string> = new Set()
    let deviceUnmountActionIdsToDelete: Set<string> = new Set()
    let deviceUnmountActionIdsToUpdate: Set<string> = new Set()
    let staticLocationBeginActionIdsToDelete: Set<string> = new Set()
    let staticLocationBeginActionIdsToUpdate: Set<string> = new Set()
    let staticLocationEndActionIdsToDelete: Set<string> = new Set()
    let staticLocationEndActionIdsToUpdate: Set<string> = new Set()
    let dynamicLocationBeginActionIdsToDelete: Set<string> = new Set()
    let dynamicLocationBeginActionIdsToUpdate: Set<string> = new Set()
    let dynamicLocationEndActionIdsToDelete: Set<string> = new Set()
    let dynamicLocationEndActionIdsToUpdate: Set<string> = new Set()

    // step 1
    // load existing config to check current setting of the configuration

    if (configuration.id) {
      const existingConfig = await this.findById(configuration.id)
      if (existingConfig.location instanceof DynamicLocation) {
        if (configuration.location instanceof DynamicLocation) {
          if (configuration.location.elevation == null && existingConfig.location.elevation !== null) {
            relationshipsToDelete.push('src-elevation')
          }
          if (configuration.location.latitude == null && existingConfig.location.latitude !== null) {
            relationshipsToDelete.push('src-latitude')
          }
          if (configuration.location.longitude == null && existingConfig.location.longitude !== null) {
            relationshipsToDelete.push('src-longitude')
          }
        } else {
          relationshipsToDelete.push('src-elevation')
          relationshipsToDelete.push('src-latitude')
          relationshipsToDelete.push('src-longitude')
        }
      }
      const newPlatformMountActionIds = new Set(configuration.platformMountActions.map(x => x.id))
      platformMountActionIdsToDelete = new Set(existingConfig.platformMountActions.map(x => x.id).filter(x => !newPlatformMountActionIds.has(x)))
      platformMountActionIdsToUpdate = new Set(existingConfig.platformMountActions.map(x => x.id).filter(x => newPlatformMountActionIds.has(x)))
      const newPlatformUnmountActionIds = new Set(configuration.platformUnmountActions.map(x => x.id))
      platformUnmountActionIdsToDelete = new Set(existingConfig.platformUnmountActions.map(x => x.id).filter(x => !newPlatformUnmountActionIds.has(x)))
      platformUnmountActionIdsToUpdate = new Set(existingConfig.platformUnmountActions.map(x => x.id).filter(x => newPlatformUnmountActionIds.has(x)))

      const newDeviceMountActionIds = new Set(configuration.deviceMountActions.map(x => x.id))
      deviceMountActionIdsToDelete = new Set(existingConfig.deviceMountActions.map(x => x.id).filter(x => !newDeviceMountActionIds.has(x)))
      deviceMountActionIdsToUpdate = new Set(existingConfig.deviceMountActions.map(x => x.id).filter(x => newDeviceMountActionIds.has(x)))
      const newDeviceUnmountActionIds = new Set(configuration.deviceUnmountActions.map(x => x.id))
      deviceUnmountActionIdsToDelete = new Set(existingConfig.deviceUnmountActions.map(x => x.id).filter(x => !newDeviceUnmountActionIds.has(x)))
      deviceUnmountActionIdsToUpdate = new Set(existingConfig.deviceUnmountActions.map(x => x.id).filter(x => newDeviceUnmountActionIds.has(x)))

      const newStaticLocationBeginActionIds = new Set(configuration.staticLocationBeginActions.map(x => x.id))
      staticLocationBeginActionIdsToDelete = new Set(existingConfig.staticLocationBeginActions.map(x => x.id).filter(x => !newStaticLocationBeginActionIds.has(x)))
      staticLocationBeginActionIdsToUpdate = new Set(existingConfig.staticLocationBeginActions.map(x => x.id).filter(x => newStaticLocationBeginActionIds.has(x)))

      const newStaticLocationEndActionIds = new Set(configuration.staticLocationEndActions.map(x => x.id))
      staticLocationEndActionIdsToDelete = new Set(existingConfig.staticLocationEndActions.map(x => x.id).filter(x => !newStaticLocationEndActionIds.has(x)))
      staticLocationEndActionIdsToUpdate = new Set(existingConfig.staticLocationEndActions.map(x => x.id).filter(x => newStaticLocationEndActionIds.has(x)))

      const newDynamicLocationBeginActionIds = new Set(configuration.dynamicLocationBeginActions.map(x => x.id))
      dynamicLocationBeginActionIdsToDelete = new Set(existingConfig.dynamicLocationBeginActions.map(x => x.id).filter(x => !newDynamicLocationBeginActionIds.has(x)))
      dynamicLocationBeginActionIdsToUpdate = new Set(existingConfig.dynamicLocationBeginActions.map(x => x.id).filter(x => newDynamicLocationBeginActionIds.has(x)))

      const newDynamicLocationEndActionIds = new Set(configuration.dynamicLocationEndActions.map(x => x.id))
      dynamicLocationEndActionIdsToDelete = new Set(existingConfig.dynamicLocationEndActions.map(x => x.id).filter(x => !newDynamicLocationEndActionIds.has(x)))
      dynamicLocationEndActionIdsToUpdate = new Set(existingConfig.dynamicLocationEndActions.map(x => x.id).filter(x => newDynamicLocationEndActionIds.has(x)))
    }

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
    const configurationId = serverAnswer.data.data.id
    const promisesDelete = []
    for (const deviceMountActionId of deviceMountActionIdsToDelete) {
      promisesDelete.push(this.deviceMountActionApi.deleteById(deviceMountActionId))
    }
    for (const deviceUnmontActionId of deviceUnmountActionIdsToDelete) {
      promisesDelete.push(this.deviceUnmountActionApi.deleteById(deviceUnmontActionId))
    }
    for (const platformMountActionId of platformMountActionIdsToDelete) {
      promisesDelete.push(this.platformMountActionApi.deleteById(platformMountActionId))
    }
    for (const platformUnmountActionId of platformUnmountActionIdsToDelete) {
      promisesDelete.push(this.platformUnmountActionApi.deleteById(platformUnmountActionId))
    }
    for (const staticLocationBeginActionId of staticLocationBeginActionIdsToDelete) {
      promisesDelete.push(this.staticLocationBeginActionApi.deleteById(staticLocationBeginActionId))
    }
    for (const staticLocationEndActionId of staticLocationEndActionIdsToDelete) {
      promisesDelete.push(this.staticLocationEndActionApi.deleteById(staticLocationEndActionId))
    }
    for (const dynamicLocationBeginActionId of dynamicLocationBeginActionIdsToDelete) {
      promisesDelete.push(this.dynamicLocationBeginActionApi.deleteById(dynamicLocationBeginActionId))
    }
    for (const dynamicLocationEndActionId of dynamicLocationEndActionIdsToDelete) {
      promisesDelete.push(this.dynamicLocationEndActionApi.deleteById(dynamicLocationEndActionId))
    }
    relationshipsToDelete.forEach(relationship => promisesDelete.push(this.tryToDeleteRelationship(relationship, configurationId)))

    await Promise.all(promisesDelete)

    // now we need to add the new ones
    const promisesSave = []
    for (const platformMountAction of configuration.platformMountActions) {
      if (!platformMountAction.id) {
        promisesSave.push(this.platformMountActionApi.add(configurationId, platformMountAction))
      } else if (platformMountActionIdsToUpdate.has(platformMountAction.id)) {
        promisesSave.push(this.platformMountActionApi.update(configurationId, platformMountAction))
      }
    }
    for (const platformUnmountAction of configuration.platformUnmountActions) {
      if (!platformUnmountAction.id) {
        promisesSave.push(this.platformUnmountActionApi.add(configurationId, platformUnmountAction))
      } else if (platformUnmountActionIdsToUpdate.has(platformUnmountAction.id)) {
        promisesSave.push(this.platformUnmountActionApi.update(configurationId, platformUnmountAction))
      }
    }
    for (const deviceMountAction of configuration.deviceMountActions) {
      if (!deviceMountAction.id) {
        promisesSave.push(this.deviceMountActionApi.add(configurationId, deviceMountAction))
      } else if (deviceMountActionIdsToUpdate.has(deviceMountAction.id)) {
        promisesSave.push(this.deviceMountActionApi.update(configurationId, deviceMountAction))
      }
    }
    for (const deviceUnmountAction of configuration.deviceUnmountActions) {
      if (!deviceUnmountAction.id) {
        promisesSave.push(this.deviceUnmountActionApi.add(configurationId, deviceUnmountAction))
      } else if (deviceUnmountActionIdsToUpdate.has(deviceUnmountAction.id)) {
        promisesSave.push(this.deviceUnmountActionApi.update(configurationId, deviceUnmountAction))
      }
    }
    for (const staticLocationBeginAction of configuration.staticLocationBeginActions) {
      if (!staticLocationBeginAction.id) {
        promisesSave.push(this.staticLocationBeginActionApi.add(configurationId, staticLocationBeginAction))
      } else if (staticLocationBeginActionIdsToUpdate.has(staticLocationBeginAction.id)) {
        promisesSave.push(this.staticLocationBeginActionApi.update(configurationId, staticLocationBeginAction))
      }
    }
    for (const staticLocationEndAction of configuration.staticLocationEndActions) {
      if (!staticLocationEndAction.id) {
        promisesSave.push(this.staticLocationEndActionApi.add(configurationId, staticLocationEndAction))
      } else if (staticLocationEndActionIdsToUpdate.has(staticLocationEndAction.id)) {
        promisesSave.push(this.staticLocationEndActionApi.update(configurationId, staticLocationEndAction))
      }
    }
    for (const dynamicLocationBeginAction of configuration.dynamicLocationBeginActions) {
      if (!dynamicLocationBeginAction.id) {
        promisesSave.push(this.dynamicLocationBeginActionApi.add(configurationId, dynamicLocationBeginAction))
      } else if (dynamicLocationBeginActionIdsToUpdate.has(dynamicLocationBeginAction.id)) {
        promisesSave.push(this.dynamicLocationBeginActionApi.update(configurationId, dynamicLocationBeginAction))
      }
    }
    for (const dynamicLocationEndAction of configuration.dynamicLocationEndActions) {
      if (!dynamicLocationEndAction.id) {
        promisesSave.push(this.dynamicLocationEndActionApi.add(configurationId, dynamicLocationEndAction))
      } else if (dynamicLocationEndActionIdsToUpdate.has(dynamicLocationEndAction.id)) {
        promisesSave.push(this.dynamicLocationEndActionApi.update(configurationId, dynamicLocationEndAction))
      }
    }
    await Promise.all(promisesSave)

    return this.findById(configurationId)
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

  newSearchBuilder (): ConfigurationSearchBuilder {
    return new ConfigurationSearchBuilder(this.axiosApi, this.basePath, this.serializer)
  }

  findRelatedContacts (configurationId: string): Promise<Contact[]> {
    const url = this.basePath + '/' + configurationId + '/contacts'
    const params = {
      'page[size]': 10000
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new ContactSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

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

export class ConfigurationSearchBuilder {
  private axiosApi: AxiosInstance
  readonly basePath: string

  private clientSideFilterFunc: (configuration: Configuration) => boolean
  private serverSideFilterSettings: IFlaskJSONAPIFilter[] = []
  private esTextFilter: string | null = null
  private serializer: ConfigurationSerializer

  constructor (axiosApi: AxiosInstance, basePath: string, serializer: ConfigurationSerializer) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.clientSideFilterFunc = (_c: Configuration) => true
    this.serializer = serializer
  }

  withText (text: string | null) {
    if (text) {
      this.esTextFilter = text
    }
    return this
  }

  withOneMatchingProjectOf (projects: Project[]) {
    if (projects.length > 0) {
      this.serverSideFilterSettings.push({
        or: [
          {
            name: 'project_name',
            op: 'in_',
            val: projects.map((p: Project) => p.name)
          },
          {
            name: 'project_uri',
            op: 'in_',
            val: projects.map((p: Project) => p.uri)
          }
        ]
      })
    }
    return this
  }

  withOneLocationTypeOf (locationTypes: string[]) {
    if (locationTypes.length > 0) {
      this.serverSideFilterSettings.push({
        name: 'location_type',
        op: 'in_',
        val: locationTypes
      })
    }
    return this
  }

  withOneStatusOf (states: string[]) {
    if (states.length > 0) {
      this.serverSideFilterSettings.push({
        name: 'status',
        op: 'in_',
        val: states
      })
    }
    return this
  }

  withContactEmail (email: string) {
    this.serverSideFilterSettings.push({
      name: 'contacts.email',
      op: 'eq',
      val: email
    })
    return this
  }

  build (): ConfigurationSearcher {
    return new ConfigurationSearcher(
      this.axiosApi,
      this.basePath,
      this.clientSideFilterFunc,
      this.serverSideFilterSettings,
      this.esTextFilter,
      this.serializer
    )
  }
}

export class ConfigurationSearcher {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private clientSideFilterFunc: (configuration: Configuration) => boolean
  private serverSideFilterSettings: IFlaskJSONAPIFilter[]
  private esTextFilter: string | null
  private serializer: ConfigurationSerializer

  constructor (
    axiosApi: AxiosInstance,
    basePath: string,
    clientSideFilterFunc: (configuration: Configuration) => boolean,
    serverSideFilterSettings: IFlaskJSONAPIFilter[],
    esTextFilter: string | null,
    serializer: ConfigurationSerializer
  ) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.clientSideFilterFunc = clientSideFilterFunc
    this.serverSideFilterSettings = serverSideFilterSettings
    this.esTextFilter = esTextFilter
    this.serializer = serializer
  }

  private get commonParams (): any {
    const result: any = {
      filter: JSON.stringify(this.serverSideFilterSettings)
    }
    if (this.esTextFilter != null) {
      // In case we have a search string, then we want to
      // sort by relevance (which is the default)
      result.q = this.esTextFilter
    } else {
      // otherwise we want to search alphabetically
      result.sort = 'label'
    }
    return result
  }

  findMatchingAsCsvBlob (): Promise<Blob> {
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
      return new Blob([response.data], { type: 'text/csv;charset=utf-8' })
    })
  }

  findMatchingAsList (): Promise<Configuration[]> {
    return this.axiosApi.get(
      this.basePath,
      {
        params: {
          'page[size]': 100000,
          ...this.commonParams
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

  findMatchingAsPaginationLoaderOnPage (page: number, pageSize: number): Promise<IPaginationLoader<Configuration>> {
    return this.findAllOnPage(page, pageSize)
  }

  private findAllOnPage (page: number, pageSize: number): Promise<IPaginationLoader<Configuration>> {
    return this.axiosApi.get(
      this.basePath,
      {
        params: {
          'page[size]': pageSize,
          'page[number]': page,
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

      // check if the provided page param is valid
      if (totalCount > 0 && elements.length === 0) {
        throw new RangeError('page is out of bounds')
      }

      let funToLoadNext = null
      if (elements.length > 0) {
        funToLoadNext = () => this.findAllOnPage(page + 1, pageSize)
      }

      let funToLoadPage = null
      if (elements.length > 0) {
        funToLoadPage = (pageNr: number) => this.findAllOnPage(pageNr, pageSize)
      }

      return {
        elements,
        totalCount,
        page,
        funToLoadNext,
        funToLoadPage
      }
    })
  }
}
