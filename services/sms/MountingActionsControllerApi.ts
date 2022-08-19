/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 -2022
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

import { DateTime } from 'luxon'
import { Contact } from '@/models/Contact'
import { ConfigurationMountingAction } from '@/models/ConfigurationMountingAction'
import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { MountingActionsSerializer } from '@/serializers/custom/MountingActionsSerializer'

export class MountingActionsControllerApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private mountingActionsSerializer: MountingActionsSerializer

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
    this.mountingActionsSerializer = new MountingActionsSerializer()
  }

  async findMountingActions (configurationId: string): Promise<ConfigurationMountingAction[]> {
    const url = this.basePath + '/' + configurationId + '/mounting-action-timepoints'
    const rawServerResponse = await this.axiosApi.get(url)
    return this.mountingActionsSerializer.convertApiTimepointsToObject(rawServerResponse.data)
  }

  async findMountingActionsByDate (configurationId: string, timepoint: DateTime, contacts: Contact[]): Promise<ConfigurationsTree> {
    const url = this.basePath + '/' + configurationId + '/mounting-actions'
    const params = {
      timepoint: timepoint.setZone('UTC').toISO()
    }
    const rawServerResponse = await this.axiosApi.get(url, { params })

    return this.mountingActionsSerializer.convertApiObjectToTree(rawServerResponse.data, contacts)
  }
}
