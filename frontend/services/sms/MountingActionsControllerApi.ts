/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
