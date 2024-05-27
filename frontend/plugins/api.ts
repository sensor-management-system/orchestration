/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { Plugin } from '@nuxt/types'
import { Api } from '@/services/Api'

declare module 'vue/types/vue' {
  interface Vue {
    $api: Api
  }
}

declare module '@nuxt/types' {
  interface NuxtAppOptions {
    $api: Api
  }
}

declare module 'vuex' {
  interface Store<S> { // eslint-disable-line
    $api: Api
  }
}

const apiPlugin: Plugin = (context, inject) => {
  const getIdToken = (): string | null => {
    // @ts-ignore
    return context.$auth.strategy.token.get()
  }
  inject('api', new Api(getIdToken))
}

export default apiPlugin
