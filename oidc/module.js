/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
 * - Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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

import { mergeObjectsAndMaybeOverwrite } from '@/utils/objectHelpers'
import { tokenIsExpired } from '@/utils/tokenHelpers'
import { toRouterPath, removeTrailingSlash } from '@/utils/urlHelpers'

export const createOidcModul = (oidcSettings, storeSettings = {}) => {
  storeSettings = mergeObjectsAndMaybeOverwrite([
    {
      namespaced: false,
      isAuthenticatedBy: 'id_token'
    },
    storeSettings
  ])

  const sessionStorageItemName = 'sms_oidc_active_route'

  const dispatchCustomBrowserEvent = (eventName, detail = {}, params = {}) => {
    if (window) {
      params = params || { bubbles: false, cancelable: false }
      params = mergeObjectsAndMaybeOverwrite([params, { detail }])
      const event = document.createEvent('CustomEvent')
      event.initCustomEvent(
        eventName,
        params.bubbles,
        params.cancelable,
        params.detail
      )
      window.dispatchEvent(event)
    }
  }

  const userManager = new UserManager(oidcSettings)

  const oidcCallbackPath = toRouterPath(oidcSettings.redirect_uri, storeSettings.routeBase || '/')
  const oidcPopupCallbackPath = toRouterPath(oidcSettings.popup_redirect_uri, storeSettings.routeBase || '/')
  const oidcSilentCallbackPath = toRouterPath(oidcSettings.silent_redirect_uri, storeSettings.routeBase || '/')
  const oidcLogoutCallbackPath = toRouterPath(oidcSettings.post_logout_redirect_uri, storeSettings.routeBase || '/')

  const hasTokenId = (state) => {
    if (state.id_token) {
      return true
    }
    return false
  }

  const routeIsPublic = (route) => {
    if (route.meta) {
      // locally and on the server this meta attribute is a list of objects
      // it would be easier to asume that it is just one meta object (for the
      // currently active route, but it is not that way...)
      const metaList = route.meta
      const meta = mergeObjectsAndMaybeOverwrite(metaList)
      // the values can be specified in the meta section of the
      // component decorator
      // something like:
      // @Component({
      //  meta: {
      //    loginRequired: true
      //  }
      // })
      if (meta.loginRequired) {
        return false
      }
      if (meta.isPublic) {
        return true
      }
    }
    return true
  }

  const errorPayload = (context, error) => {
    return {
      context,
      error: error && error.message ? error.message : error
    }
  }

  const routeIsOidcCallback = (route) => {
    if (route.meta && route.meta.isOidcCallback) {
      return true
    }
    if (route.path && removeTrailingSlash(route.path) === oidcCallbackPath) {
      return true
    }
    if (route.path && removeTrailingSlash(route.path) === oidcPopupCallbackPath) {
      return true
    }
    if (route.path && removeTrailingSlash(route.path) === oidcSilentCallbackPath) {
      return true
    }
    if (route.path && removeTrailingSlash(route.path) === oidcLogoutCallbackPath) {
      return true
    }
    return false
  }

  // **********************************Store******************************************************

  const state = {
    id_token: null,
    user: null,
    scopes: null,
    error: null,
    intervalId: null,
    isAutomaticSilentRenewOn: false
  }

  const getters = {
    oidcIdToken: (state) => {
      return state.id_token
    },
    isAuthenticated: (state) => {
      return hasTokenId(state)
    },
    username: (state) => {
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

    userEmail: (state) => {
      if (state.user) {
        return state.user.email
      }
      return null
    },
    allUserClaims: (state) => {
      if (state.user) {
        return state.user
      }
      return []
    },
    oidcUser: (state) => {
      return state.user
    }
  }

  const actions = {
    // ESLint wants to have an await in an async function.
    // As we don't have it, I comment it out
    /* async */ loginPopup ({ dispatch, commit }) {
      return new Promise((resolve, reject) => {
        userManager.signinPopup().then((user) => {
          dispatch('oidcWasAuthenticated', user)
          dispatch('automaticSilentRenew')
          resolve(sessionStorage.getItem(sessionStorageItemName) || '/')
          dispatchCustomBrowserEvent('userLoaded', user)
        }).catch((err) => {
          commit('setOidcError', errorPayload('oidcSignInCallback', err))
          reject(err)
        })
      })
    },
    oidcSignInPopupCallback (context, url) {
      return new Promise((resolve, reject) => {
        userManager.signinPopupCallback(url).then((result) => {
          resolve(result)
        }).catch((err) => {
          context.commit('setOidcError', errorPayload('oidcSignInPopupCallback', err))
          reject(err)
        })
      })
    },
    oidcWasAuthenticated ({ commit }, user) {
      commit('setOidcAuth', user)
    },
    async logoutPopup ({ commit }) {
      await userManager.signoutPopup()
      commit('unsetOidcAuth')
      commit('clearInterval')
    },
    silentRenew ({ dispatch }) {
      userManager.signinSilent().then((user) => {
        dispatch('oidcWasAuthenticated', user)
        dispatchCustomBrowserEvent('userLoaded', user)
      })
    },
    automaticSilentRenew ({ state, dispatch, commit }) {
      if (!state.intervalId) {
        const intervalId = setInterval(() => dispatch('silentRenew'), oidcSettings.renewIntervall)
        commit('setIntervalId', intervalId)
      }
    },
    handleSilentRenewCallback () {
      return new Promise((resolve, reject) => {
        userManager.signinSilentCallback().then((result) => {
          resolve(result)
        }).catch(err => reject(err))
      })
    },
    handleSigninPopupCallback () {
      return new Promise((resolve, reject) => {
        userManager.signinPopupCallback().then((result) => {
          resolve(result)
        }).catch((err) => {
          reject(err)
        })
      })
    },
    handleSignoutPopupCallback () {
      return new Promise((resolve, reject) => {
        userManager.signoutPopupCallback().then((result) => {
          resolve(result)
        }).catch((err) => {
          reject(err)
        })
      })
    },
    loadStoredUser ({ commit, dispatch }) {
      userManager.getUser().then((user) => {
        if (user !== null) {
          commit('setOidcAuth', user)
          dispatch('automaticSilentRenew')
        }
      })
    },
    /* async */ oidcCheckAccess (context, route) {
      return new Promise((resolve) => {
        if (routeIsOidcCallback(route)) {
          resolve(true)
          return
        }

        let hasAccess = true

        const getUserPromise = new Promise((resolve) => {
          userManager.getUser().then((user) => {
            resolve(user)
          }).catch(() => {
            resolve(null)
          })
        })

        const isAuthenticatedInStore = hasTokenId(context.state)

        getUserPromise.then((user) => {
          if (!user || tokenIsExpired(user.id_token)) {
            if (routeIsPublic(route)) {
              if (isAuthenticatedInStore) {
                context.commit('unsetOidcAuth')
              }
            } else {
              const authenticate = () => {
                if (isAuthenticatedInStore) {
                  context.commit('unsetOidcAuth')
                }
                context.dispatch('authenticateOidc', {
                  redirectPath: route.fullPath
                })
              }
              // If no silent signin is set up, perform explicit authentication and deny access
              authenticate()
              hasAccess = false
            }
          } else {
            context.dispatch('oidcWasAuthenticated', user)
            context.dispatch('automaticSilentRenew')
          }
          resolve(hasAccess)
        })
      })
    },
    authenticateOidc (_context, payload = {}) {
      if (typeof payload === 'string') {
        payload = { redirectPath: payload }
      }
      if (payload.redirectPath) {
        sessionStorage.setItem(sessionStorageItemName, payload.redirectPath)
      } else {
        sessionStorage.removeItem(sessionStorageItemName)
      }
    },
    removeOidcUser ({ commit }) {
      return userManager.removeUser().then(() => {
        commit('unsetOidcAuth')
        commit('clearInterval')
      })
    }
  }

  const mutations = {
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
      sessionStorage.removeItem(sessionStorageItemName)
    },
    setIntervalId (state, intervalId) {
      state.intervalId = intervalId
    },
    clearInterval (state) {
      clearInterval(state.intervalId)
      state.intervalId = null
    },
    setOidcError (state, payload) {
      state.error = payload.error
    }
  }

  const storeModule = mergeObjectsAndMaybeOverwrite([
    storeSettings,
    {
      state,
      getters,
      actions,
      mutations
    }
  ])

  return storeModule
}
