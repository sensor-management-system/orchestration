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
