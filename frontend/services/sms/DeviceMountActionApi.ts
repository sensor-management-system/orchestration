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
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { DeviceMountActionSerializer } from '@/serializers/jsonapi/DeviceMountActionSerializer'

export class DeviceMountActionApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: DeviceMountActionSerializer

  constructor (axiosApi: AxiosInstance, basePath: string) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = new DeviceMountActionSerializer()
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }

  async findById (id: string): Promise<DeviceMountAction|null> {
    const url = this.basePath + '/' + id
    const params = {
      include: [
        'begin_contact',
        'end_contact',
        'parent_platform',
        'device',
        'device.device_properties'
      ].join(',')
    }
    const response = await this.axiosApi.get(url, { params })
    if ('data' in response && !response.data) {
      return null
    }
    return this.serializer.convertJsonApiObjectToModel(response.data)
  }

  async add (configurationId: string, deviceMountAction: DeviceMountAction): Promise<string> {
    const url = this.basePath
    const data = this.serializer.convertModelToJsonApiData(configurationId, deviceMountAction)
    const response = await this.axiosApi.post(url, { data })
    // we can't return a full entity here, as we need to included data about the contacts & the device
    // so we just return the id, and let the client load the full element with the included data
    // once it is necessary
    return response.data.id
  }

  async update (configurationId: string, deviceMountAction: DeviceMountAction): Promise<string> {
    if (!deviceMountAction.id) {
      throw new Error('no id for the DeviceMountAction')
    }
    const url = this.basePath + '/' + deviceMountAction.id
    const data = this.serializer.convertModelToJsonApiData(configurationId, deviceMountAction)
    const response = await this.axiosApi.patch(url, { data })
    // we can't return a full entity here, as we need to included data about the contacts & the device
    // so we just return the id, and let the client load the full element with the included data
    // once it is necessary
    return response.data.id
  }

  async getRelatedActions (configurationId: string) {
    const url = '/configurations/' + configurationId + '/device-mount-actions'
    const params = {
      'page[size]': 10000,
      include: [
        'begin_contact',
        'end_contact',
        'parent_platform',
        'device'
      ].join(',')
    }
    const rawServerResponse = await this.axiosApi.get(url, { params })
    return this.serializer.convertJsonApiObjectListToModelList(rawServerResponse.data)
  }

  async getRelatedActionsIncludingDeviceInformation (configurationId: string) {
    const url = '/configurations/' + configurationId + '/device-mount-actions'
    const params = {
      'page[size]': 10000,
      include: [
        'device',
        'device.device_properties'
      ].join(',')
    }
    const rawServerResponse = await this.axiosApi.get(url, { params })
    return this.serializer.convertJsonApiObjectListToModelList(rawServerResponse.data)
  }
}
