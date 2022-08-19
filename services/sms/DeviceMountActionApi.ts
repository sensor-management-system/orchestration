/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2021
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
    const response = await this.axiosApi.get(url, { params })
    return response.data
  }
}
