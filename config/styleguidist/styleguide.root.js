import Vuetify from 'vuetify/lib'

export default (previewComponent) => {
  // https://vuejs.org/v2/guide/render-function.html
  return {
    vuetify: new Vuetify(),
    render (createElement) {
      return createElement('v-app', [createElement(previewComponent)])
    }
  }
}
