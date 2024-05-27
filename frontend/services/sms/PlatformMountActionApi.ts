/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2021
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { AxiosInstance } from 'axios'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { PlatformMountActionSerializer } from '@/serializers/jsonapi/PlatformMountActionSerializer'

export class PlatformMountActionApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: PlatformMountActionSerializer

  constructor (axiosApi: AxiosInstance, basePath: string) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = new PlatformMountActionSerializer()
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }

  async findById (id: string): Promise<PlatformMountAction|null> {
    const url = this.basePath + '/' + id
    const params = {
      include: [
        'begin_contact',
        'end_contact',
        'parent_platform',
        'platform'
      ].join(',')
    }
    const response = await this.axiosApi.get(url, { params })
    if ('data' in response && !response.data) {
      return null
    }
    return this.serializer.convertJsonApiObjectToModel(response.data)
  }

  async add (configurationId: string, platformMountAction: PlatformMountAction): Promise<string> {
    const url = this.basePath
    const data = this.serializer.convertModelToJsonApiData(configurationId, platformMountAction)
    const response = await this.axiosApi.post(url, { data })
    // we can't return a full entity here, as we need to included data about the contacts & the device
    // so we just return the id, and let the client load the full element with the included data
    // once it is necessary
    return response.data.id
  }

  async update (configurationId: string, platformMountAction: PlatformMountAction): Promise<string> {
    if (!platformMountAction.id) {
      throw new Error('no id for the PlatformMountAction')
    }
    const url = this.basePath + '/' + platformMountAction.id
    const data = this.serializer.convertModelToJsonApiData(configurationId, platformMountAction)
    const response = await this.axiosApi.patch(url, { data })
    // we can't return a full entity here, as we need to included data about the contacts & the device
    // so we just return the id, and let the client load the full element with the included data
    // once it is necessary
    return response.data.id
  }

  async getRelatedActions (configurationId: string) {
    const url = '/configurations/' + configurationId + '/platform-mount-actions'
    const params = {
      'page[size]': 10000,
      include: [
        'begin_contact',
        'end_contact',
        'parent_platform',
        'platform'
      ].join(',')
    }
    const rawServerResponse = await this.axiosApi.get(url, { params })
    return this.serializer.convertJsonApiObjectListToModelList(rawServerResponse.data)
  }
}
