/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { Plugin, Context } from '@nuxt/types'

declare module 'vue/types/vue' {
  interface Vue {
    $fullContext: Context
  }
}

declare module '@nuxt/types' {
  interface NuxtAppOptions {
    $fullContext: Context
  }
}

const fullContextPlugin: Plugin = (context: Context, inject) => {
  inject('fullContext', context)
}

export default fullContextPlugin
