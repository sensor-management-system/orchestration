/*
Web client of the Sensor Management System software developed within
the Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
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
  if (context.route.path.match('^/login-success/?$') && institute.toLowerCase() === 'gfz') {
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
