import oidcSettings from '@/config/oidc'
import { createOidcModul } from '@/oidc/module'

const storeModule = createOidcModul(oidcSettings, {
  namespaced: true,
  routeBase: process.env.NUXT_ENV_PUBLIC_PATH
})

export const state = () => (storeModule.state)

export const getters = storeModule.getters

export const actions = storeModule.actions

export const mutations = storeModule.mutations
