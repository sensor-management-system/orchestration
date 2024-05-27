/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

/**
 * @file provides a mixin component for edit pages to handle the check if a
 * user is allowed to access the page
 * @author <marc.hanisch@gfz-potsdam.de>
 */

import { Vue, Component, InjectReactive } from 'nuxt-property-decorator'

/**
 * A mixin component that validates if the user is allowed to access a page
 * @extends Vue
 */
@Component
export default class CheckEditAccess extends Vue {
  @InjectReactive()
    editable!: boolean

  created () {
    if (!this.editable) {
      this.$router.replace(this.getRedirectUrl(), () => {
        this.$store.commit('snackbar/setError', this.getRedirectMessage())
      })
    }
  }

  getRedirectUrl (): string {
    return '/'
  }

  getRedirectMessage (): string {
    return 'You\'re not allowed to access this page.'
  }
}
