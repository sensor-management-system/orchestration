/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2021 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

import { DeviceProperty } from '@/models/DeviceProperty'
import { DevicePropertySerializer } from '@/serializers/jsonapi/DevicePropertySerializer'

export class DevicePropertyApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: DevicePropertySerializer

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
    this.serializer = new DevicePropertySerializer()
  }

  findById (id: string): Promise<DeviceProperty> {
    return this.axiosApi.get(this.basePath + '/' + id).then((rawRespmse) => {
      const rawData = rawRespmse.data
      return this.serializer.convertJsonApiObjectToModel(rawData)
    })
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }

  add (deviceId: string, deviceProperty: DeviceProperty): Promise<DeviceProperty> {
    const url = this.basePath
    const data = this.serializer.convertModelToJsonApiData(deviceProperty, deviceId)
    return this.axiosApi.post(url, { data }).then((serverResponse) => {
      return this.serializer.convertJsonApiObjectToModel(serverResponse.data)
    })
  }

  update (deviceId: string, deviceProperty: DeviceProperty): Promise<DeviceProperty> {
    return new Promise<string>((resolve, reject) => {
      if (deviceProperty.id) {
        resolve(deviceProperty.id)
      } else {
        reject(new Error('no id for the Attachment'))
      }
    }).then((devicePropertyId) => {
      const data = this.serializer.convertModelToJsonApiData(deviceProperty, deviceId)
      return this.axiosApi.patch(this.basePath + '/' + devicePropertyId, { data }).then((serverResponse) => {
        return this.serializer.convertJsonApiObjectToModel(serverResponse.data)
      })
    })
  }
}
