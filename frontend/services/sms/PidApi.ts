/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2022
 * - Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *   (UFZ, https://www.ufz.de)
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
