import settings from '../authConfig/oidcSettings'
import {UserManager} from "oidc-client";

const userManager = new UserManager(settings);

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
    isAutomaticSilentRenewOn:false
})

const getters = {
  isAuthenticated (state) {
    return isAuthenticated(state);
  },
  username (state) {
    if (state.user) {
      return state.user.name;
    }
    return null;
  },
  userEmail (state) {
    if (state.user) {
      return state.user.email;
    }
    return null;
  },
  allUserClaims (state) {
    if (state.user) {
      return state.user;
    }
    return null;
  }

}

const actions = {
    loginPopup({dispatch}) {
        userManager.signinPopup()
                   .then(user => {
                       dispatch('oidcWasAuthenticated', user);
                       dispatch('automaticSilentRenew');
                   })
    },
    oidcWasAuthenticated({commit}, user) {
        commit('setOidcAuth', user);
    },
    logoutPopup({commit,dispatch}, routing) {
        userManager.signoutPopup()
                   .then(() => {
                       commit('unsetOidcAuth');
                       dispatch('stopAutomaticSilentRenew');
                       if (routing.currentRoute !== '/') {
                           routing.router.push('/')
                       }
                   });
    },
    silentRenew({dispatch}) {
        userManager.signinSilent()
                   .then(user => {
                       dispatch('oidcWasAuthenticated', user);
                   });
    },
    automaticSilentRenew({state,dispatch,commit}) {
        if(!state.isAutomaticSilentRenewOn){
            let intervalId = setInterval(() => dispatch('silentRenew'), process.env.NUXT_ENV_SILENT_RENEW_INTERVAL);
            commit('setIntervalId',intervalId);
            commit('enableAutomaticSilentRenewOn')
        }

    },
    stopAutomaticSilentRenew({commit}){
        commit('stopInterval');
        commit('disableAutomaticSilentRenewOn');

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
    loadStoredUser({commit,dispatch}) {
        userManager.getUser()
                   .then((user) => {
                       if (user !== null) {
                           commit('setOidcAuth', user);
                           dispatch('automaticSilentRenew');
                       }
                   })
    },
    oidcCheckAccess(context, route) {
        return new Promise(resolve => {
            if (!route.meta.isSecure) {
                resolve(true);
                return
            }
            let hasAccess = true;
            const getUserPromise = new Promise(resolve => {
                userManager.getUser()
                           .then(user => {
                               resolve(user)
                           })
                           .catch(() => {
                               resolve(null)
                           })
            });
            const isAuthenticatedInStore = isAuthenticated(context.state);
            getUserPromise.then(user => {
                if (!user || user.expired) {
                    if (isAuthenticatedInStore) {
                        context.commit('unsetOidcAuth')
                    }
                    hasAccess = false;
                } else {
                    context.dispatch('oidcWasAuthenticated', user);

                }
                resolve(hasAccess)
            })
        })
    }
};

export const mutations = {
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
    },
    setIntervalId(state,intervalId){
        state.intervalId = intervalId
    },
    stopInterval(state){
        clearInterval(state.intervalId);
        state.intervalId = null;
    },
    enableAutomaticSilentRenewOn(state){
        state.isAutomaticSilentRenewOn = true;
    },
    disableAutomaticSilentRenewOn(state){
        state.isAutomaticSilentRenewOn = false;
    }
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
