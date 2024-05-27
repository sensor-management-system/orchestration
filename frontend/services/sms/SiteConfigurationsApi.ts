/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { AxiosInstance } from 'axios'
import { Configuration } from '@/models/Configuration'
import { ConfigurationSerializer, configurationWithMetaToConfigurationByThrowingNoErrorOnMissing } from '@/serializers/jsonapi/ConfigurationSerializer'
import { PermissionGroup } from '@/models/PermissionGroup'

export type ConfigurationPermissionFetchFunction = () => Promise<PermissionGroup[]>

export class SiteConfigurationsApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: ConfigurationSerializer

  private permissionFetcher: ConfigurationPermissionFetchFunction | undefined

  constructor (
    axiosApi: AxiosInstance,
    basePath: string,
    permissionFetcher?: ConfigurationPermissionFetchFunction
  ) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = new ConfigurationSerializer()
    if (permissionFetcher) {
      this.permissionFetcher = permissionFetcher
    }
  }

  async findRelatedConfigurations (siteId: string): Promise<Configuration[]> {
    if (this.permissionFetcher) {
      this.serializer.permissionGroups = await this.permissionFetcher()
    }
    const url = '/sites/' + siteId + '/configurations'
    const params = {
      'page[size]': 10000
    }
    const rawServerResponse = await this.axiosApi.get(url, { params })
    const configs = this.serializer.convertJsonApiObjectListToModelList(rawServerResponse.data)
    const result = configs.map(config => configurationWithMetaToConfigurationByThrowingNoErrorOnMissing(config))
    return result
  }
}
