/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

export class MaintenanceMessageApi {
  private readonly axiosApi: AxiosInstance

  constructor (axiosApi: AxiosInstance) {
    this.axiosApi = axiosApi
  }

  async getMessage (): Promise<string | null> {
    const response = await this.axiosApi.get('/maintenance-message', {
      headers: { Accept: 'text/plain' },
      responseType: 'text'
    })
    return response.status === 204 ? null : response.data
  }
}
