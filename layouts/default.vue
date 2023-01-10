<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2023
- Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)

Parts of this program were developed within the context of the
following publicly funded projects or measures:
- Helmholtz Earth and Environment DataHub
  (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)

Licensed under the HEESIL, Version 1.0 or - as soon they will be
approved by the "Community" - subsequent versions of the HEESIL
(the "Licence").

You may not use this work except in compliance with the Licence.

You may obtain a copy of the Licence at:
https://gitext.gfz-potsdam.de/software/heesil

Unless required by applicable law or agreed to in writing, software
distributed under the Licence is distributed on an "AS IS" basis,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the Licence for the specific language governing
permissions and limitations under the Licence.
-->
<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      :mini-variant="miniVariant"
      :clipped="clipped"
      fixed
      app
    >
      <v-list nav>
        <!-- Home -->
        <v-list-item to="/" exact nuxt>
          <v-list-item-action>
            <v-icon>mdi-apps</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <!-- Devices -->
        <v-list-item to="/devices" nuxt>
          <v-list-item-action>
            <v-icon>mdi-network</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Devices</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <!-- Platforms -->
        <v-list-item to="/platforms" nuxt>
          <v-list-item-action>
            <v-icon>mdi-rocket</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Platforms</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <!-- Configurations -->
        <v-list-item to="/configurations" nuxt>
          <v-list-item-action>
            <v-icon>mdi-file-cog</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Configurations</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <!-- Sites -->
        <v-list-item to="/sites" nuxt>
          <v-list-item-action>
            <v-icon>mdi-map-marker-radius</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Sites</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <!-- Contacts -->
        <v-list-item v-if="isLoggedIn" to="/contacts" nuxt>
          <v-list-item-action>
            <v-icon>mdi-account-multiple</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Contacts</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <!-- Group information -->
        <v-list-item to="/info/groups" nuxt>
          <v-list-item-action>
            <v-icon>mdi-account-group</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Groups</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider />

        <!-- Help -->
        <v-list-item to="/help" nuxt>
          <v-list-item-action>
            <v-icon>mdi-help-circle-outline</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Help</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
      :clipped-left="clipped"
      fixed
      app
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <AppBarEditModeContent
        :title="appBarTitle"
        :save-btn-hidden="saveBtnHidden"
        :cancel-btn-hidden="cancelBtnHidden"
        :save-btn-disabled="saveBtnDisabled"
        :cancel-btn-disabled="cancelBtnDisabled"
      />
      <template v-if="tabs.length" #extension>
        <AppBarTabsExtension
          :value="activeTab"
          :tabs="tabs"
          @change="onChangeTab"
        />
      </template>
      <v-menu close-on-click close-on-content-click offset-x>
        <template #activator="{ on }">
          <v-btn
            data-role="property-menu"
            icon
            small
            v-on="on"
          >
            <v-avatar>
              <template v-if="$auth.loggedIn">
                {{ initials }}
              </template>
              <template v-else>
                <v-icon>
                  mdi-account
                </v-icon>
              </template>
            </v-avatar>
          </v-btn>
        </template>
        <v-list>
          <template v-if="!$auth.loggedIn">
            <v-list-item dense @click="login">
              <v-list-item-content>
                <v-list-item-title>
                  <v-icon small left>
                    mdi-login
                  </v-icon>
                  <span>Login</span>
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </template>
          <template v-if="$auth.loggedIn">
            <v-list-item dense @click="logout">
              <v-list-item-content>
                <v-list-item-title>
                  <v-icon small left>
                    mdi-logout
                  </v-icon>
                  <span>Logout</span>
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item dense to="/profile">
              <v-list-item-content>
                <v-list-item-title>
                  <v-icon small left>
                    mdi-account-details
                  </v-icon>
                  <span>Profile</span>
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </template>
        </v-list>
      </v-menu>
    </v-app-bar>
    <v-main>
      <v-container :fluid="fullWidth" :class="fullWidth ? ['mx-0', 'px-0', 'pt-0']: []">
        <v-snackbar v-model="hasSuccess" top color="green">
          {{ success }}
          <template #action="{ attrs }">
            <v-btn icon small color="white" v-bind="attrs" @click="closeSuccessSnackbar">
              <v-icon small>
                mdi-close
              </v-icon>
            </v-btn>
          </template>
        </v-snackbar>
        <v-snackbar v-model="hasError" top color="error">
          {{ error }}
          <template #action="{ attrs }">
            <v-btn icon small color="white" v-bind="attrs" @click="closeErrorSnackbar">
              <v-icon small>
                mdi-close
              </v-icon>
            </v-btn>
          </template>
        </v-snackbar>
        <v-snackbar v-model="hasWarning" top color="orange" :timeout="-1">
          {{ warning }}
          <template #action="{ attrs }">
            <v-btn icon small color="white" v-bind="attrs" @click="closeWarningSnackbar">
              <v-icon small>
                mdi-close
              </v-icon>
            </v-btn>
          </template>
        </v-snackbar>
        <nuxt />
      </v-container>
    </v-main>
    <v-footer v-if="!isLandingPage" app absolute padless>
      <logo-footer :is-landing-page="isLandingPage" />
    </v-footer>
    <v-footer
      class="link-footer"
      :absolute="$vuetify.breakpoint.smAndDown"
      :fixed="$vuetify.breakpoint.smAndUp"
      app
      padless
    >
      <logo-footer v-if="isLandingPage" :is-landing-page="isLandingPage" class="logo-footer__landing" />
      <cookie-law
        button-text="Okay"
        button-class="v-btn v-btn--is-elevated v-btn--has-bg v-size--default primary"
        storage-name="cookie-and-terms-of-use-1:accepted"
        theme="sms"
      >
        <template #message>
          <!-- eslint-disable -->
          This site uses cookies to ensure technical functionality. To read more about what we store in the cookies, have
          a look at our
          <nuxt-link to="/info/privacy-policy">Privacy Policy</nuxt-link>
          .
          By using this service, I also accept the
          <nuxt-link to="/info/terms-of-use">Terms of Use</nuxt-link>
          .
          <!-- eslint-enable -->
        </template>
      </cookie-law>

      <v-row
        no-gutters
      >
        <v-col
          cols="12"
          md="8"
          offset-md="2"
          align-self="center"
          class="text-center caption text--secondary"
        >
          <v-btn
            to="/info/legal-notice"
            text
            class="ma-2"
            small
            color="secondary"
          >
            Legal Notice
          </v-btn>&nbsp;|&nbsp;
          <v-btn
            to="/info/privacy-policy"
            text
            class="ma-2"
            small
            color="secondary"
          >
            Privacy Policy
          </v-btn>&nbsp;|&nbsp;
          <v-btn
            to="/info/terms-of-use"
            text
            class="ma-2"
            small
            color="secondary"
          >
            Terms of Use
          </v-btn>
          |&nbsp;<span class="ma-2 pl-3">&copy;&nbsp;{{ new Date().getFullYear() }}</span>
        </v-col>
        <v-col
          cols="12"
          md="2"
          align-self="center"
          :class="iconLinksClass"
        >
          <v-btn
            href="https://codebase.helmholtz.cloud/hub-terra/sms/"
            target="_blank"
            title="Sensor Management System Repository"
            icon
          >
            <v-icon>mdi-gitlab</v-icon>
          </v-btn>
          <v-btn
            v-if="apiLink"
            :href="apiLink"
            target="_blank"
            title="Sensor Management System API"
            icon
          >
            <v-icon>mdi-api</v-icon>
          </v-btn>
          <v-btn
            href="mailto:gitlab-incoming+hub-terra-sms-service-desk-4415-issue-@hzdr.de"
            title="Request Support"
            icon
          >
            <v-icon>mdi-message-question-outline</v-icon>
          </v-btn>
        </v-col>
      </v-row>
      <!-- </v-container> -->
    </v-footer>
  </v-app>
</template>

<script>

import CookieLaw from 'vue-cookie-law'
import { mapActions, mapState } from 'vuex'
import AppBarTabsExtension from '@/components/AppBarTabsExtension'
import AppBarEditModeContent from '@/components/AppBarEditModeContent'
import LogoFooter from '@/components/LogoFooter'

import { saveCurrentRoute } from '@/utils/loginHelpers'

export default {
  components: {
    AppBarTabsExtension,
    AppBarEditModeContent,
    CookieLaw,
    LogoFooter
  },
  data () {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
      miniVariant: false,
      title: 'Sensor Management System',
      appBarContent: null,
      appBarExtension: null
    }
  },
  head () {
    return {
      title: this.browserTitle
    }
  },
  computed: {
    ...mapState('defaultlayout', ['fullWidth']),
    browserTitle () {
      if (this.title === this.appBarTitle) {
        return this.title
      }
      if (!this.appBarTitle) {
        return this.title
      }
      return this.appBarTitle + ' - ' + this.title
    },
    error () {
      return this.$store.state.snackbar.error
    },
    hasError: {
      get () {
        return this.$store.state.snackbar.error !== ''
      },
      set (newValue) {
        if (!newValue) {
          this.$store.commit('snackbar/clearError')
        }
      }
    },
    success () {
      return this.$store.state.snackbar.success
    },
    hasSuccess: {
      get () {
        return this.$store.state.snackbar.success !== ''
      },
      set (newValue) {
        if (!newValue) {
          this.$store.commit('snackbar/clearSuccess')
        }
      }
    },
    warning () {
      return this.$store.state.snackbar.warning
    },
    hasWarning: {
      get () {
        return this.$store.state.snackbar.warning !== ''
      },
      set (newValue) {
        if (!newValue) {
          this.$store.commit('snackbar/clearWarning')
        }
      }
    },
    tabs () {
      return this.$store.state.appbar.tabs
    },
    activeTab () {
      return this.$store.state.appbar.activeTab
    },
    appBarTitle () {
      return this.$store.state.appbar.title || this.title
    },
    saveBtnHidden () {
      return this.$store.state.appbar.saveBtnHidden
    },
    saveBtnDisabled () {
      return this.$store.state.appbar.saveBtnDisabled
    },
    cancelBtnHidden () {
      return this.$store.state.appbar.cancelBtnHidden
    },
    cancelBtnDisabled () {
      return this.$store.state.appbar.cancelBtnDisabled
    },
    initials () {
      if (this.$auth.loggedIn) {
        const givenName = this.$auth.user.given_name
        const familyName = this.$auth.user.family_name

        if (
          givenName != null && givenName.length > 0 &&
          familyName != null && familyName.length > 0
        ) {
          return givenName[0] + familyName[0]
        }

        if (this.$auth.user.name.length > 2) {
          return this.$auth.user.name[0] + this.$auth.user.name[1]
        }
      }
      return null
    },
    apiLink () {
      let link = ''
      if (this.$fullContext.env.smsBackendUrl) {
        link = this.$fullContext.env.smsBackendUrl + '/openapi'
      }
      return link
    },
    iconLinksClass () {
      let align = ''
      switch (this.$vuetify.breakpoint.name) {
        case 'xs':
        case 'sm':
          align = 'text-center'
          break
        case 'md':
        case 'lg':
        case 'xl':
          align = 'text-right'
          break
      }
      return align + ' pr-2'
    },
    isLoggedIn () {
      return this.$auth.loggedIn
    },
    isLandingPage () {
      return this.$route.path === '/'
    }
  },
  created () {
    this.$nuxt.$on('app-bar-content', (component) => {
      this.appBarContent = component
    })
    this.$nuxt.$on('app-bar-extension', (component) => {
      this.appBarExtension = component
    })
  },
  methods: {
    ...mapActions('permissions', ['clearUserInfo']),
    closeErrorSnackbar () {
      this.$store.commit('snackbar/clearError')
    },
    closeSuccessSnackbar () {
      this.$store.commit('snackbar/clearSuccess')
    },
    closeWarningSnackbar () {
      this.$store.commit('snackbar/clearWarning')
    },
    onChangeTab (tab) {
      this.$store.commit('appbar/setActiveTab', tab)
    },
    login () {
      saveCurrentRoute(this.$fullContext)
      let params = {}
      try {
        params = JSON.parse(process.env.NUXT_ENV_OIDC_LOGIN_PARAMS)
      } catch (error) {
        // Error handling skipped, as params is set to {} by default
      }
      this.$auth.loginWith('customStrategy', params)
        .catch(() => {
          this.$store.commit('snackbar/setError', 'Login failed')
        })
    },
    async logout () {
      await this.$auth.logout()
      this.clearUserInfo()
    }
  }
}
</script>

<style lang="scss" scoped>
  @import '~vuetify/src/styles/styles.sass';

  .Cookie--sms {
    position: relative;
    background: map-get($grey, 'lighten-3');
    padding: $grid-gutter / 2;
  }

  .link-footer {
    z-index: 10;
  }

  .logo-footer__landing {
    z-index: 1 !important;
    margin-bottom: 0 !important;
  }

</style>>
