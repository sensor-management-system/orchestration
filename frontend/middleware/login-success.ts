/*
SPDX-FileCopyrightText: 2020 - 2023
 *
 * SPDX-License-Identifier: EUPL-1.2
*/

import { Middleware, Context } from '@nuxt/types'
import { AxiosResponse } from 'axios'

import { createAxios } from '@/utils/axiosHelper'

/**
 * triggers the GFZ IDL which updates the groups of the currently logged in user
 *
 * @param {() => string | null} getIdTokenFunc - a function that returns the ID token
 * @returns {null | Promise<AxiosResponse<any, any>>} returns `null` if the URL to the IDL was not defined, otherwise the axios response object
 */
const syncGroups = (getIdTokenFunc: () => string | null): null | Promise<AxiosResponse<any, any>> => {
  const IDL_SYNC_URL = process.env.idlSyncUrl
  if (!IDL_SYNC_URL) {
    return null
  }
  const axios = createAxios(
    IDL_SYNC_URL,
    {
      headers: {
        'Content-Type': 'application/vnd.api+json'
      }
    },
    getIdTokenFunc
  )
  return axios.get('/')
}

const loginSuccessMiddleware: Middleware = async function (context: Context) {
  const institute: string = context.env.institute
  // just when on /login-success and for GFZ only
  if (context.route.path.match('^/login-success/?$') && (institute.toLowerCase() === 'gfz' || institute.toLowerCase() === 'ufz')) {
    const getIdToken = (): string | null => {
      // @ts-ignore
      return context.$auth.strategy.token.get()
    }
    await syncGroups(getIdToken)
    // And we must force the backend to invalide its caches as we want to see the
    // new groups right away.
    Promise.all([
      context.store.dispatch('permissions/loadUserInfo', { skipBackendCache: true }),
      context.store.dispatch('permissions/loadPermissionGroups', { skipBackendCache: true })
    ])
  }
}
export default loginSuccessMiddleware
