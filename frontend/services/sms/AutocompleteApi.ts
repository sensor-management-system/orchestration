/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

interface SerialNumberOptions {
  ignore: string | null
  model: string | null
  manufacturerName: string | null
}

type DeviceOrPlatform = 'device' | 'platform'

export class AutocompleteApi {
  private axiosApi: AxiosInstance
  readonly basePath: string

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
  }

  async getSuggestions (endpoint: string, filters: Object = {}): Promise<string[]> {
    const url = this.basePath + '/' + endpoint
    const rawServerResponse = await this.axiosApi.get(url, { params: { ...filters } })
    if (rawServerResponse.data) {
      return rawServerResponse.data.data
    } else {
      return []
    }
  }

  private async getSerialNumbers (entity: DeviceOrPlatform, serialNumberOptions: SerialNumberOptions | null): Promise<string[]> {
    const url = this.basePath + '/' + entity + '-serial-numbers'
    const params: any = {}
    if (serialNumberOptions?.ignore) {
      params.ignore = serialNumberOptions.ignore
    }
    if (serialNumberOptions?.manufacturerName) {
      params.manufacturer_name = serialNumberOptions.manufacturerName
    }
    if (serialNumberOptions?.model) {
      params.model = serialNumberOptions.model
    }
    const rawServerResponse = await this.axiosApi.get(url, { params })
    if (rawServerResponse.data) {
      return rawServerResponse.data.data
    } else {
      return []
    }
  }

  getDeviceSerialNumbers (serialNumberOptions: SerialNumberOptions | null = null): Promise<string[]> {
    return this.getSerialNumbers('device', serialNumberOptions)
  }

  getPlatformSerialNumbers (serialNumberOptions: SerialNumberOptions | null = null): Promise<string[]> {
    return this.getSerialNumbers('platform', serialNumberOptions)
  }
}
