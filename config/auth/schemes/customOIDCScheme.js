/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2021
 * - Wilhelm Becker (GFZ, wilhelm.becker@gfz-potsdam.de)
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Erik Pongratz (UFZ, erik.pongratz@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
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

import { OpenIDConnectScheme } from '~auth/runtime'

export default class CustomOIDCScheme extends OpenIDConnectScheme {
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
  }
}
