/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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
        include: 'contacts'
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

    if (configuration.id === null) {
      method = 'post'
    } else {
      url = configuration.id
    }
    return this.axiosApi.request({
      url,
      method,
      data: {
        data
      }
    }).then((serverAnswer) => {
      // no contacts here => reload completely
      return this.findById(serverAnswer.data.data.id)
    })
  }

  newSearchBuilder (): ConfigurationSearchBuilder {
    return new ConfigurationSearchBuilder(this.axiosApi, this.serializer)
  }
}

export class ConfigurationSearchBuilder {
  private axiosApi: AxiosInstance
  private clientSideFilterFunc: (configuration: Configuration) => boolean
  private serverSideFilterSettings: IFlaskJSONAPIFilter[] = []
  private serializer: ConfigurationSerializer

  constructor (axiosApi: AxiosInstance, serializer: ConfigurationSerializer) {
    this.axiosApi = axiosApi
    this.clientSideFilterFunc = (_c: Configuration) => true
    this.serializer = serializer
  }

  withTextInLabel (text: string | null) {
    if (text) {
      const ilikeValue = '%' + text + '%'
      const fieldsToSearchIn = [
        'label'
      ]

      const filter: IFlaskJSONAPIFilter[] = []
      for (const field of fieldsToSearchIn) {
        filter.push({
          name: field,
          op: 'ilike',
          val: ilikeValue
        })
      }

      this.serverSideFilterSettings.push({
        or: filter
      })
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
      this.serializer
    )
  }
}

export class ConfigurationSearcher {
  private axiosApi: AxiosInstance
  private clientSideFilterFunc: (configuration: Configuration) => boolean
  private serverSideFilterSettings: IFlaskJSONAPIFilter[]
  private serializer: ConfigurationSerializer

  constructor (
    axiosApi: AxiosInstance,
    clientSideFilterFunc: (configuration: Configuration) => boolean,
    serverSideFilterSettings: IFlaskJSONAPIFilter[],
    serializer: ConfigurationSerializer
  ) {
    this.axiosApi = axiosApi
    this.clientSideFilterFunc = clientSideFilterFunc
    this.serverSideFilterSettings = serverSideFilterSettings
    this.serializer = serializer
  }

  private get commonParams (): any {
    return {
      filter: JSON.stringify(this.serverSideFilterSettings),
      sort: 'label'
    }
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
