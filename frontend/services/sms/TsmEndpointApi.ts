/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { AxiosInstance } from 'axios'
import { TsmEndpointSerializer } from '@/serializers/jsonapi/TsmEndpointSerializer'
import { TsmEndpoint } from '@/models/TsmEndpoint'

export class TsmEndpointApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: TsmEndpointSerializer

  constructor (axiosApi: AxiosInstance, basePath: string) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = new TsmEndpointSerializer()
  }

  async findAll (): Promise<TsmEndpoint[]> {
    const params = {
      'page[size]': 10000
    }
    const rawServerResponse = await this.axiosApi.get(this.basePath, { params })
    return this.serializer.convertJsonApiObjectListToModelList(rawServerResponse.data)
  }

  async findOneById (id: string): Promise<TsmEndpoint | null> {
    const url = this.basePath + '/tsm-endpoints/' + id
    const rawServerResponse = await this.axiosApi.get(url)
    return this.serializer.convertJsonApiEntityToModel(rawServerResponse.data)
  }
}
