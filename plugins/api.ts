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

const apiPlugin: Plugin = (_context, inject) => {
  inject('api', new Api())
}

export default apiPlugin
