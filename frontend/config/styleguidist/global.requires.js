/*
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2021 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Erik Pongratz <erik.pongratz@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import Vue from 'vue'
import Vuetify from 'vuetify'
import options from '@/config/vuetify/vuetify.options'

Vue.component('NuxtLink', {
  props: {
    tag: { type: String, default: 'a' }
  },
  render (createElement) {
    return createElement(this.tag, {}, this.$slots.default)
  }
})

Vue.use(Vuetify, options)
