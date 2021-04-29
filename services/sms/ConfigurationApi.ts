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
  // eslint-disable-next-line
  IPaginationLoader, FilteredPaginationedLoader
} from '@/utils/PaginatedLoader'

import {
  ConfigurationSerializer,
  configurationWithMetaToConfigurationByAddingDummyObjects,
  configurationWithMetaToConfigurationByThrowingErrorOnMissing
} from '@/serializers/jsonapi/ConfigurationSerializer'

import { ContactSerializer } from '@/serializers/jsonapi/ContactSerializer'

export class ConfigurationApi {
  private axiosApi: AxiosInstance
  private serializer: ConfigurationSerializer

  constructor (axiosInstance: AxiosInstance) {
    this.axiosApi = axiosInstance
    this.serializer = new ConfigurationSerializer()
  }

  findById (id: string): Promise<Configuration> {
    return this.axiosApi.get(id, {
      params: {
        include: [
          'contacts',
          'configuration_platforms.platform',
          'configuration_devices.device',
          'src_longitude',
          'src_latitude',
          'src_elevation'
        ].join(',')
      }
    }).then((rawResponse) => {
      const rawData = rawResponse.data
      return configurationWithMetaToConfigurationByThrowingErrorOnMissing(this.serializer.convertJsonApiObjectToModel(rawData))
    })
  }

  // eslint-disable-next-line
  deleteById (id: string) : Promise<void> {
    return this.axiosApi.delete<string, void>(id)
  }

  save (configuration: Configuration): Promise<Configuration> {
    const data: any = this.serializer.convertModelToJsonApiData(configuration)
    let method: Method = 'patch'
    let url = ''
    const relationshipsToDelete : string[] = []

    if (!configuration.id) {
      method = 'post'
    } else {
      url = configuration.id

      if (configuration.location instanceof DynamicLocation) {
        if (configuration.location.elevation == null) {
          // it uses here the url views to send a delete request
          relationshipsToDelete.push('src-elevation')
        }
        if (configuration.location.latitude == null) {
          relationshipsToDelete.push('src-latitude')
        }
        if (configuration.location.longitude == null) {
          relationshipsToDelete.push('src-longitude')
        }
      } else {
        relationshipsToDelete.push('src-elevation')
        relationshipsToDelete.push('src-latitude')
        relationshipsToDelete.push('src-longitude')
      }
    }
    return this.axiosApi.request({
      url,
      method,
      data: {
        data
      }
    }).then((serverAnswer) => {
      return this.tryToDeleteRelationshipsAndFindById(relationshipsToDelete, serverAnswer.data.data.id)
    })
  }

  private async tryToDeleteRelationshipsAndFindById (relationshipsToDelete: string[], id: string) : Promise<Configuration> {
    await Promise.all(relationshipsToDelete.map(async (r: string) => {
      await this.tryToDeleteRelationship(r, id)
    }))
    return this.findById(id)
  }

  private async tryToDeleteRelationship (relationshipToDelete: string, id: string) {
    const url = id + '/relationships/' + relationshipToDelete

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
    return new ConfigurationSearchBuilder(this.axiosApi, this.serializer)
  }

  findRelatedContacts (configurationId: string): Promise<Contact[]> {
    const url = configurationId + '/contacts'
    const params = {
      'page[size]': 10000
    }
    return this.axiosApi.get(url, { params }).then((rawServerResponse) => {
      return new ContactSerializer().convertJsonApiObjectListToModelList(rawServerResponse.data)
    })
  }

  removeContact (configurationId: string, contactId: string): Promise<void> {
    const url = configurationId + '/relationships/contacts'
    const params = {
      data: [{
        type: 'contact',
        id: contactId
      }]
    }
    return this.axiosApi.delete(url, { data: params })
  }

  addContact (configurationId: string, contactId: string): Promise<void> {
    const url = configurationId + '/relationships/contacts'
    const data = [{
      type: 'contact',
      id: contactId
    }]
    return this.axiosApi.post(url, { data })
  }
}

export class ConfigurationSearchBuilder {
  private axiosApi: AxiosInstance
  private clientSideFilterFunc: (configuration: Configuration) => boolean
  private serverSideFilterSettings: IFlaskJSONAPIFilter[] = []
  private esTextFilter: string | null = null
  private serializer: ConfigurationSerializer

  constructor (axiosApi: AxiosInstance, serializer: ConfigurationSerializer) {
    this.axiosApi = axiosApi
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

  build (): ConfigurationSearcher {
    return new ConfigurationSearcher(
      this.axiosApi,
      this.clientSideFilterFunc,
      this.serverSideFilterSettings,
      this.esTextFilter,
      this.serializer
    )
  }
}

export class ConfigurationSearcher {
  private axiosApi: AxiosInstance
  private clientSideFilterFunc: (configuration: Configuration) => boolean
  private serverSideFilterSettings: IFlaskJSONAPIFilter[]
  private esTextFilter: string | null
  private serializer: ConfigurationSerializer

  constructor (
    axiosApi: AxiosInstance,
    clientSideFilterFunc: (configuration: Configuration) => boolean,
    serverSideFilterSettings: IFlaskJSONAPIFilter[],
    esTextFilter: string | null,
    serializer: ConfigurationSerializer
  ) {
    this.axiosApi = axiosApi
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
    const url = ''
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
      '',
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

  findMatchingAsPaginationLoader (pageSize: number): Promise<IPaginationLoader<Configuration>> {
    const loaderPromise: Promise<IPaginationLoader<Configuration>> = this.findAllOnPage(1, pageSize)
    return loaderPromise.then((loader) => {
      return new FilteredPaginationedLoader<Configuration>(loader, this.clientSideFilterFunc)
    })
  }

  private findAllOnPage (page: number, pageSize: number): Promise<IPaginationLoader<Configuration>> {
    return this.axiosApi.get(
      '',
      {
        params: {
          'page[size]': pageSize,
          'page[number]': page,
          ...this.commonParams
        }
      }
    ).then((rawResponse) => {
      const rawData = rawResponse.data
      // client side filtering will not be done here
      // (but in the FilteredPaginationedLoader)
      // so that we know if we still have elements here
      // there may be others to load as well

      // And - again - we don't ask the api here to load the contact data as well
      // so we will add the dummy objects to stay with the relationships
      const elements: Configuration[] = this.serializer.convertJsonApiObjectListToModelList(
        rawData
      ).map(configurationWithMetaToConfigurationByAddingDummyObjects)

      const totalCount = rawData.meta.count

      let funToLoadNext = null
      if (elements.length > 0) {
        funToLoadNext = () => this.findAllOnPage(page + 1, pageSize)
      }

      return {
        elements,
        totalCount,
        funToLoadNext
      }
    })
  }
}
