/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { AxiosInstance } from 'axios'

export class ProxyApi {
  private axiosApi: AxiosInstance
  private baseUrl: string

  constructor (axiosInstance: AxiosInstance, baseUrl: string) {
    this.axiosApi = axiosInstance
    this.baseUrl = baseUrl
  }

  getUrlViaProxy (url: string): string {
    return this.baseUrl + '/proxy?url=' + encodeURIComponent(url)
  }

  async getContentViaProxy (url: string): Promise<string> {
    const proxyUrl = this.getUrlViaProxy(url)
    const response = await this.axiosApi.get(proxyUrl)
    return response.data
  }
}
