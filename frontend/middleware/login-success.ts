/*
SPDX-FileCopyrightText: 2020 - 2023
 *
 * SPDX-License-Identifier: EUPL-1.2
*/

import { Middleware, Context } from '@nuxt/types'

const loginSuccessMiddleware: Middleware = async function (context: Context) {
  // just when on /login-success
  if (context.route.path.match('^/login-success/?$')) {
    await context.store.dispatch('permissions/loadUserInfo', { skipBackendCache: true })
    await context.store.dispatch('permissions/loadPermissionGroups')
  }
}
export default loginSuccessMiddleware
