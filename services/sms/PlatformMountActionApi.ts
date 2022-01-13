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
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { PlatformMountActionSerializer } from '@/serializers/jsonapi/PlatformMountActionSerializer'

export class PlatformMountActionApi {
  private axiosApi: AxiosInstance
  private serializer: PlatformMountActionSerializer

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
    this.serializer = new PlatformMountActionSerializer()
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(id)
  }

  async add (configurationId: string, platformMountAction: PlatformMountAction): Promise<string> {
    const url = ''
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
    const url = platformMountAction.id
    const data = this.serializer.convertModelToJsonApiData(configurationId, platformMountAction)
    const response = await this.axiosApi.patch(url, { data })
    // we can't return a full entity here, as we need to included data about the contacts & the device
    // so we just return the id, and let the client load the full element with the included data
    // once it is necessary
    return response.data.id
  }
}
