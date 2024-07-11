/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Wilhelm Becker <wilhelm.becker@gfz-potsdam.de>
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Erik Pongratz <erik.pongratz@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { OpenIDConnectScheme } from '~auth/runtime'

export default class CustomOIDCScheme extends OpenIDConnectScheme {
  constructor ($auth, options, ...defaults) {
    super($auth, options, ...defaults)
    this.options.scope = options.scope
  }

  // Fetch the userInfo from the user-info endpoint
  async fetchUser () {
    const checkExpiration = this.check(true)

    if (!checkExpiration.valid) {
      this.$auth.logout()
      return
    }
    const { data } = await this.$auth.requestWith(this.name, {
      url: this.options.endpoints.userInfo
    })

    // Compare id-token sub with user-info sub according to note in
    // https://openid.net/specs/openid-connect-core-1_0.html#UserInfoResponse
    if (this.$auth.strategies.customStrategy.idToken.userInfo().sub !== data.sub) {
      return
    }
    this.$auth.setUser(data)

    // activate token refresh after a certain amount of time
    if (!checkExpiration.refreshTokenExpired) {
      const intervalId = setInterval(() => {
        this.$auth.refreshTokens()
          .catch(() => {
            this.$auth.ctx.store.commit('snackbar/setError', 'Error while refreshing tokens!')
            clearInterval(intervalId)
          })
      }, process.env.NUXT_ENV_OIDC_REFRESH_INTERVAL_TIME || 30 * 60 * 1000) // time in milliseconds when to start the token refresh
    }

    // Fetch user info
    this.$auth.ctx.store.dispatch('permissions/loadUserInfo')

    // Fetch all permission groups
    this.$auth.ctx.store.dispatch('permissions/loadPermissionGroups')
  }
}
