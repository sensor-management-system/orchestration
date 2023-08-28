/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2022
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
import axios, { AxiosInstance, AxiosRequestConfig } from 'axios'

/**
 * creates an axios instance
 *
 * @param {string | undefined} baseUrl - the base URL for all requests
 * @param {AxiosRequestConfig} baseConfig - an AxiosRequestConfig instance
 * @param {() => (string | null)} [getIdToken] - a function that returns the IDToken
 * @returns {AxiosInstance} a new axios instance
 */
export function createAxios (
  baseUrl: string | undefined,
  baseConfig: AxiosRequestConfig,
  getIdToken?: () => (string | null)
): AxiosInstance {
  const config: AxiosRequestConfig = {
    ...baseConfig,
    baseURL: baseUrl
  }
  const instance = axios.create(config)

  // If we have a function to query our id tokens on the time of the request
  // we want to use it here.
  if (getIdToken) {
    instance.interceptors.request.use((config) => {
      const idToken = getIdToken()
      // But it can be that we are not logged in, so that our idToken is null.
      // So in this case, we don't send the id token with the request.
      if (idToken) {
        // But once we have it, we want to send it with.
        if (!config.headers) {
          config.headers = {}
        }
        config.headers.Authorization = idToken
      }
      return config
    })
  }
  return instance
}
