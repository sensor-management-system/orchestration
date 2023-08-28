/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2021
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
