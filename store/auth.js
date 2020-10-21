/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
 * - Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *   (UFZ, https://www.ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
 */
import { UserManager } from 'oidc-client'
import settings from '@/config/oidc'

const userManager = new UserManager(settings)

const isAuthenticated = (state) => {
  if (state.id_token) {
    return true
  }
  return false
}

const state = () => ({
  id_token: null,
  user: null,
  scopes: null,
  error: null,
  intervalId: null,
  isAutomaticSilentRenewOn: false
})

const getters = {
  isAuthenticated (state) {
    return isAuthenticated(state)
  },
  username (state) {
    if (state.user) {
      return state.user.name
    }
    return null
  },
  initials (state) {
    if (state.user) {
      const givenName = state.user.given_name
      const familyName = state.user.family_name

      if (
        givenName != null && givenName.length > 0 &&
        familyName != null && familyName.length > 0
      ) {
        return givenName[0] + familyName[0]
      }

      if (state.user.name.length > 2) {
        return state.user.name[0] + state.user.name[1]
      }
    }
    return null
  },
  userEmail (state) {
    if (state.user) {
      return state.user.email
    }
    return null
  },
  allUserClaims (state) {
    if (state.user) {
      return state.user
    }
    return null
  }

}

const actions = {
  loginPopup ({ dispatch }) {
    return userManager.signinPopup()
      .then((user) => {
        dispatch('oidcWasAuthenticated', user)
        dispatch('automaticSilentRenew')
        return user
      })
  },
  oidcWasAuthenticated ({ commit }, user) {
    commit('setOidcAuth', user)
  },
  logoutPopup ({ commit, dispatch }, routing) {
    return userManager.signoutPopup()
      .then(() => {
        commit('unsetOidcAuth')
        dispatch('stopAutomaticSilentRenew')
        if (routing.currentRoute !== '/') {
          routing.router.push('/')
        }
      })
  },
  silentRenew ({ dispatch }) {
    return userManager.signinSilent()
      .then((user) => {
        dispatch('oidcWasAuthenticated', user)
        return user
      })
  },
  automaticSilentRenew ({ state, dispatch, commit }) {
    if (!state.isAutomaticSilentRenewOn) {
      const intervalId = setInterval(() => dispatch('silentRenew'), process.env.NUXT_ENV_SILENT_RENEW_INTERVAL)
      commit('setIntervalId', intervalId)
      commit('enableAutomaticSilentRenewOn')
    }
  },
  stopAutomaticSilentRenew ({ commit }) {
    commit('stopInterval')
    commit('disableAutomaticSilentRenewOn')
  },
  handleSilentRenewCallback () {
    return userManager.signinSilentCallback()
  },
  handleSigninPopupCallback () {
    return userManager.signinPopupCallback().then((value) => {
      console.log('auth handleSgininPopup sucessful')
      return value
    })
  },
  handleSignoutPopupCallback () {
    return userManager.signoutPopupCallback()
  },
  loadStoredUser ({ commit, dispatch }) {
    userManager.getUser()
      .then((user) => {
        if (user !== null) {
          commit('setOidcAuth', user)
          dispatch('automaticSilentRenew')
        }
      })
  },
  oidcCheckAccess (context, route) {
    return new Promise((resolve) => {
      if (!route.meta.isSecure) {
        resolve(true)
        return
      }
      let hasAccess = true
      const getUserPromise = new Promise((resolve) => {
        userManager.getUser()
          .then((user) => {
            resolve(user)
          })
          .catch(() => {
            resolve(null)
          })
      })
      const isAuthenticatedInStore = isAuthenticated(context.state)
      getUserPromise.then((user) => {
        if (!user || user.expired) {
          if (isAuthenticatedInStore) {
            context.commit('unsetOidcAuth')
          }
          hasAccess = false
        } else {
          context.dispatch('oidcWasAuthenticated', user)
        }
        resolve(hasAccess)
      })
    })
  }
}

export const mutations = {
  setOidcAuth (state, user) {
    state.id_token = user.id_token
    state.user = user.profile
    state.scopes = user.scopes
    state.error = null
  },
  unsetOidcAuth (state) {
    state.id_token = null
    state.user = null
    state.scopes = null
  },
  setIntervalId (state, intervalId) {
    state.intervalId = intervalId
  },
  stopInterval (state) {
    clearInterval(state.intervalId)
    state.intervalId = null
  },
  enableAutomaticSilentRenewOn (state) {
    state.isAutomaticSilentRenewOn = true
  },
  disableAutomaticSilentRenewOn (state) {
    state.isAutomaticSilentRenewOn = false
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
