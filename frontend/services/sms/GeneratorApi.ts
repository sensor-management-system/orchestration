/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * - Nils Brinckmann <nils.brinckmann@gfz.de>
 * - GFZ - Helmholtz Centre for Geosciences (GFZ, https://www.gfz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { AxiosInstance } from 'axios'

export class GeneratorApi {
  private axiosApi: AxiosInstance
  readonly basePath: string

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
  }

  async generateSerialNumber (): Promise<string> {
    const url = this.basePath + '/serial-number'
    const rawServerResponse = await this.axiosApi.get(url, {})
    return rawServerResponse.data.data
  }
}
