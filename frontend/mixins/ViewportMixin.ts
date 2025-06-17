/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2025
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { Vue, Component } from 'nuxt-property-decorator'
/**
 * A mixin component with helper functions to handle logic regarding the current viewport
 * @extends Vue
 */
@Component
export class ViewPort extends Vue {
  get isMobileView () {
    return this.$vuetify.breakpoint.smAndDown
  }

  get isDesktopView () {
    return !this.isMobileView
  }
}
