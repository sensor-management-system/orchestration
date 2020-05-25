export const state = () => ({
  counter: 1,
  env: {},
  meta: []
})

export const mutations = {
  increment(state) {
    state.counter++
  },
  setMeta(state, meta) {
    state.meta = meta
  },
  setEnv(state, env) {
    state.env = env
  }
}
export const actions = {
  nuxtServerInit({commit}) {
    if (process.server) {
      commit('setEnv', {
        VAR1: process.env.VUE_APP_REDIRECT_URI,
        VAR2: process.env.VUE_APP_CLIENT_ID,
        VAR3: process.env.APP_AUTHORITY,
        VAR4: process.env.VUE_APP_RESPONSE_TYPE,
        VAR5: process.env.VUE_APP_SCOPE,
        VAR6: process.env.VUE_APP_POST_LOGOUT_REDIRECT_URI,
        VAR7: process.env.VUE_APP_FILTER_PROTOCOL_CLAIMS,
        VAR8: process.env.VUE_APP_AUTOMATIC_SILENT_RENEW,
        VAR9: process.env.VUE_APP_SILENT_REDIRECT_URI
      })
    }
  }
}
