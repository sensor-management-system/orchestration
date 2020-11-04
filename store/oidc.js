import oidcSettings from '@/config/oidc'
import { createAuthModul } from '@/utils/auth'

const storeModule = createAuthModul(oidcSettings, {
  namespaced: true,
  routeBase: process.env.NUXT_ENV_PUBLIC_PATH
})

export const state = () => (storeModule.state)

export const getters = storeModule.getters

export const actions = storeModule.actions

export const mutations = storeModule.mutations
