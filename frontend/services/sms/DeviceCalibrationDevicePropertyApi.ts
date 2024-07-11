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
import { DeviceCalibrationDevicePropertySerializer } from '@/serializers/jsonapi/DeviceCalibrationDevicePropertySerializer'

export class DeviceCalibrationDevicePropertyApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: DeviceCalibrationDevicePropertySerializer

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
    this.serializer = new DeviceCalibrationDevicePropertySerializer()
  }

  async add (actionId: string, devicePropty: DeviceProperty): Promise<any> {
    const url = this.basePath
    const data = this.serializer.convertModelToJsonApiData(devicePropty, actionId)
    await this.axiosApi.post(url, { data })
  }

  async delete (id: string): Promise<void> {
    return await this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }
}
