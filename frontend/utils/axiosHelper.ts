/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
