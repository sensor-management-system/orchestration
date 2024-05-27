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
import { StatisticsCount } from '@/models/Statistics'

export class StatisticsApi {
  private axiosApi: AxiosInstance
  readonly basePath: string

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
  }

  async getCounts (): Promise<StatisticsCount> {
    const url = this.basePath + '/usage-statistics'
    const rawServerResponse = await this.axiosApi.get(url)

    const rawData: StatisticsCount = rawServerResponse.data.counts
    return rawData
  }
}
