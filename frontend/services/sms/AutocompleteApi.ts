/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2024
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tim Eder (UFZ, tim.eder@ufz.de)
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
