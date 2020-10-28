import {UserManager} from "oidc-client";

export const createAuthModul = (oidcSettings, storeSettings = {}) => {
  const objectAssign = (objects) => {
    return objects.reduce(function (r, o) {
      Object.keys(o || {}).forEach(function (k) {
        r[k] = o[k]
      })
      return r
    }, {})
  }

  storeSettings = objectAssign([
    {
      namespaced: false,
      isAuthenticatedBy: 'id_token'
    },
    storeSettings
  ])

  const getOidcCallbackPath = (callbackUri, routeBase = '/') => {
    if (callbackUri) {
      const domainStartsAt = '://'
      const hostAndPath = callbackUri.substr(callbackUri.indexOf(domainStartsAt) + domainStartsAt.length);
      const routeBaseLength = routeBase === '/' ? 0 : routeBase.length;
      return hostAndPath.substr(hostAndPath.indexOf(routeBase) + routeBaseLength);
    }
    return null
  }

  const dispatchCustomBrowserEvent = (eventName, detail = {}, params = {}) => {
    if (window) {
      params = params || {bubbles: false, cancelable: false}
      params = objectAssign([params, {detail: detail}])
      var event = document.createEvent('CustomEvent')
      event.initCustomEvent(
        eventName,
        params.bubbles,
        params.cancelable,
        params.detail
      )
      window.dispatchEvent(event)
    }
  }

  const userManager = new UserManager(oidcSettings);

  const oidcCallbackPath = getOidcCallbackPath(oidcSettings.redirect_uri, storeSettings.routeBase || '/');
  const oidcPopupCallbackPath = getOidcCallbackPath(oidcSettings.popup_redirect_uri, storeSettings.routeBase || '/');
  const oidcSilentCallbackPath = getOidcCallbackPath(oidcSettings.silent_redirect_uri, storeSettings.routeBase || '/');
  const oidcLogoutCallbackPath = getOidcCallbackPath(oidcSettings.post_logout_redirect_uri, storeSettings.routeBase || '/');

  const isAuthenticated = (state) => {
    if (state.id_token) {
      return true
    }
    return false
  };

  const routeIsPublic = (route) => {
    if (route.meta && route.meta.isPublic) {
      return true;
    }
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
    if (route.path && route.path.replace(/\/$/, '') === oidcCallbackPath) {
      return true
    }
    if (route.path && route.path.replace(/\/$/, '') === oidcPopupCallbackPath) {
      return true
    }
    if (route.path && route.path.replace(/\/$/, '') === oidcSilentCallbackPath) {
      return true
    }
    if (route.path && route.path.replace(/\/$/, '') === oidcLogoutCallbackPath) {
      return true
    }
    return false
  }

  const parseJwt = (token) => {
    try {
      var base64Url = token.split('.')[1]
      var base64 = base64Url.replace('-', '+').replace('_', '/')
      return JSON.parse(window.atob(base64))
    } catch (error) {
      return {}
    }
  }

  const tokenExp = (token) => {
    if (token) {
      const parsed = parseJwt(token)
      return parsed.exp ? parsed.exp * 1000 : null
    }
    return null
  }

  const tokenIsExpired = (token) => {
    const tokenExpiryTime = tokenExp(token)
    if (tokenExpiryTime) {
      return tokenExpiryTime < new Date().getTime()
    }
    return false
  }

  //**********************************Store******************************************************//

  const state = {
    id_token: null,
    user: null,
    scopes: null,
    error: null,
    intervalId: null,
    isAutomaticSilentRenewOn: false
  };

  const getters = {
    oidcIdToken: (state) => {
      return state.id_token;
    },
    isAuthenticated: (state) => {
      return isAuthenticated(state);
    },
    username: (state) => {
      if (state.user) {
        return state.user.name;
      }
      return null;
    },
    initials(state) {
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
        return state.user.email;
      }
      return null;
    },
    allUserClaims: (state) => {
      if (state.user) {
        return state.user;
      }
      return [];
    },
    oidcUser: (state) => {
      return state.user
    }
  };

  const actions = {
    async loginPopup({dispatch, commit}) {

      return new Promise((resolve, reject) => {
        userManager.signinPopup()
          .then(user => {
            dispatch('oidcWasAuthenticated', user);
            dispatch('automaticSilentRenew');
            resolve(sessionStorage.getItem('ufz_vuex_oidc_active_route') || '/')
            dispatchCustomBrowserEvent('userLoaded', user);
          })
          .catch(err => {
            commit('setOidcError', errorPayload('oidcSignInCallback', err))
            reject(err)
          })
      })
    }
    ,
    oidcSignInPopupCallback(context, url) {
      return new Promise((resolve, reject) => {
        userManager.signinPopupCallback(url)
          .catch(err => {
            context.commit('setOidcError', errorPayload('oidcSignInPopupCallback', err))
            reject(err)
          })
      })
    },
    oidcWasAuthenticated({commit}, user) {
      commit('setOidcAuth', user);
    },
    async logoutPopup({commit}) {
      await userManager.signoutPopup();
      commit('unsetOidcAuth');
      commit('clearInterval');
    },
    silentRenew({dispatch}) {
      userManager.signinSilent()
        .then(user => {
          dispatch('oidcWasAuthenticated', user);
          dispatchCustomBrowserEvent('userLoaded', user);
        });
    },
    automaticSilentRenew({state, dispatch, commit}) {
      if (!state.intervalId) {
        let intervalId = setInterval(() => dispatch('silentRenew'), oidcSettings.renewIntervall);
        commit('setIntervalId', intervalId);
      }

    },
    handleSilentRenewCallback() {
      return new Promise(((resolve, reject) => {
        userManager.signinSilentCallback()
          .catch(err => reject(err));
      }))
    },
    handleSigninPopupCallback() {
      return new Promise((resolve, reject) => {
        userManager.signinPopupCallback()
          .catch(err => {
            reject(err)
          })
      })
    },
    handleSignoutPopupCallback() {
      return new Promise((resolve, reject) => {
        userManager.signoutPopupCallback()
          .catch(err => {
            reject(err)
          })
      })
    },
    loadStoredUser({commit, dispatch}) {
      userManager.getUser()
        .then((user) => {
          if (user !== null) {
            commit('setOidcAuth', user);
            dispatch('automaticSilentRenew');
          }
        })
    },
    async oidcCheckAccess(context, route) {
      return new Promise(resolve => {

        if (routeIsOidcCallback(route)) {
          resolve(true)
          return
        }

        let hasAccess = true;

        const getUserPromise = new Promise(resolve => {
          userManager.getUser().then(user => {
            resolve(user)
          }).catch(() => {
            resolve(null)
          })
        });

        const isAuthenticatedInStore = isAuthenticated(context.state);

        getUserPromise.then(user => {
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
            context.dispatch('automaticSilentRenew');
          }
          resolve(hasAccess)
        })

      })
    },
    authenticateOidc(context, payload = {}) {
      if (typeof payload === 'string') {
        payload = {redirectPath: payload}
      }
      if (payload.redirectPath) {
        sessionStorage.setItem('ufz_vuex_oidc_active_route', payload.redirectPath)
      } else {
        sessionStorage.removeItem('ufz_vuex_oidc_active_route');
      }
    },
    removeOidcUser({commit}) {
      /* istanbul ignore next */
      return userManager.removeUser().then(() => {
        commit('unsetOidcAuth');
        commit('clearInterval');

      })
    }
  };

  const mutations = {
    setOidcAuth(state, user) {
      state.id_token = user.id_token;
      state.user = user.profile;
      state.scopes = user.scopes;
      state.error = null;
    },
    unsetOidcAuth(state) {
      state.id_token = null;
      state.user = null;
      state.scopes = null;
      sessionStorage.removeItem('ufz_vuex_oidc_active_route');
    },
    setIntervalId(state, intervalId) {
      state.intervalId = intervalId
    },
    clearInterval(state) {
      clearInterval(state.intervalId);
      state.intervalId = null;
    },
    setOidcError(state, payload) {
      state.error = payload.error
    }
  };

  const storeModule = objectAssign([
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
