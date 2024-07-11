/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { AxiosInstance } from 'axios'
import {
  ILocationTimepoint,
  LocationActionTimepointSerializer
} from '@/serializers/controller/LocationActionTimepointSerializer'

export class LocationActionTimepointControllerApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: LocationActionTimepointSerializer

  constructor (axiosApi: AxiosInstance, basePath: string) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = new LocationActionTimepointSerializer()
  }

  async findLocationActions (configurationId: string): Promise<ILocationTimepoint[]> {
    const url = this.basePath + '/' + configurationId + '/location-action-timepoints'
    const rawServerResponse = await this.axiosApi.get(url)
    return this.serializer.convertJsonApiObjectListToModelList(rawServerResponse.data)
  }
}
