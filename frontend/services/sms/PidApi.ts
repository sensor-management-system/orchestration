/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'
import { removeTrailingSlash } from '@/utils/urlHelpers'

interface PidResponse {
  data: {
    pid: string
  }
}

interface PidRequest {
  instrument_instance: {
    source_uri: string;
    type: string;
    id: string;
  };
}

export class PidApi {
  private axiosApi: AxiosInstance
  readonly apiPath: string

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    this.axiosApi = axiosInstance
    this.apiPath = basePath
  }

  async create (id: string | null, type: string): Promise<string> {
    if (!id) { return '' }

    const smsBaseUrl = process.env.basePath ?? '/'
    const smsBaseUrlWithoutTrailingSlash = removeTrailingSlash(smsBaseUrl)
    const typePlural = type + 's'

    const requestData: PidRequest = {
      instrument_instance: {
        source_uri: `${location.origin}${smsBaseUrlWithoutTrailingSlash}/${typePlural}/${id}`,
        type,
        id
      }
    }
    const result: PidResponse = await this.axiosApi.post(this.apiPath, requestData, {
      headers: {
        'Content-Type': 'application/vnd.api+json'
      }
    })

    return result.data.pid as string
  }
}
