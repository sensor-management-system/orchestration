<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
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

        <!-- Contacts -->
        <v-list-item to="/contacts" nuxt>
          <v-list-item-action>
            <v-icon>mdi-account-multiple</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Contacts</v-list-item-title>
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
      <v-container>
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
        <nuxt />
      </v-container>
    </v-main>
    <cookie-law
      button-text="Okay"
      button-class="v-btn v-btn--is-elevated v-btn--has-bg v-size--default primary"
    >
      <template #message>
        <!-- eslint-disable-next-line -->
        This site uses cookies to ensure technical functionality. To read more about what we store in the cookies, have a look at our <nuxt-link to="info/privacy-policy">Privacy Policy</nuxt-link>.
      </template>
    </cookie-law>
    <v-footer
      :fixed="fixed"
      app
      padless
    >
      <v-row
        no-gutters
      >
        <v-col
          cols="12"
          class="text-center caption"
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
          <span class="ma-2">&copy; {{ new Date().getFullYear() }}</span>
        </v-col>
      </v-row>
    </v-footer>
  </v-app>
</template>

<script>

import CookieLaw from 'vue-cookie-law'
import AppBarTabsExtension from '@/components/AppBarTabsExtension'
import AppBarEditModeContent from '@/components/AppBarEditModeContent'

import { saveCurrentRoute } from '@/utils/loginHelpers'

export default {
  components: {
    AppBarTabsExtension,
    AppBarEditModeContent,
    CookieLaw
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
    closeErrorSnackbar () {
      this.$store.commit('snackbar/clearError')
    },
    closeSuccessSnackbar () {
      this.$store.commit('snackbar/clearSuccess')
    },
    onChangeTab (tab) {
      this.$store.commit('appbar/setActiveTab', tab)
    },
    login () {
      saveCurrentRoute(this.$fullContext)
      this.$auth.loginWith('customStrategy').catch(() => {
        this.$store.commit('snackbar/setError', 'Login failed')
      })
    },
    logout () {
      this.$auth.logout()
    }
  }
}
</script>
