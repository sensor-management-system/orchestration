/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { AxiosInstance } from 'axios'
import { DateTime } from 'luxon'

export class ActivityApi {
  private axiosApi: AxiosInstance

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
  }

  async getGlobalActivities (earliest: DateTime, latest: DateTime): Promise<any[]> {
    const params = {
      earliest: earliest.setZone('UTC').toISO(),
      latest: latest.setZone('UTC').toISO()
    }
    const rawResponse = await this.axiosApi.get('/controller/global-activities', { params })
    const rawData = rawResponse.data
    // rawData looks like this {"data": [{"date": "2024-07-04", "count": 2}]}
    // we return the list here
    return rawData.data
  }
}
