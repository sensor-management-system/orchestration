/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Erik Pongratz <erik.pongratz@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

// eslint-disable-next-line camelcase
import jwt_decode from 'jwt-decode'
import { Oauth2Scheme } from '~auth/runtime'

export default class CustomScheme extends Oauth2Scheme {
  // Override `fetchUser` method of `social` scheme
  fetchUser () {
    // Token is required but not available
    if (!this.check().valid) {
      return
    }

    const idToken = this.token.get().replace('Bearer', '').trim()
    const customUser = jwt_decode(idToken)
    this.$auth.setUser(customUser)
  }
}
