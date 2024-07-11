/*
SPDX-FileCopyrightText: 2020 - 2022
 *
 * SPDX-License-Identifier: EUPL-1.2
*/

import { Middleware, Context } from '@nuxt/types'

const institutePagesMiddleware: Middleware = function (context: Context) {
  const institute = context.env.institute
  if (context.route.path.match('^/info/legal-notice/?$')) {
    context.redirect(`info/legal-notice/${institute}`)
  }
  if (context.route.path.match('^/info/privacy-policy/?$')) {
    context.redirect(`info/privacy-policy/${institute}`)
  }
  if (context.route.path.match('^/info/terms-of-use/?$')) {
    context.redirect(`info/terms-of-use/${institute}`)
  }
  if (context.route.path.match('^/info/groups/?$')) {
    context.redirect(`info/groups/${institute}`)
  }
}
export default institutePagesMiddleware
