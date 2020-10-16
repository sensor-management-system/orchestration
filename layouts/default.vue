<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
        <v-list-item to="/search/devices" exact nuxt>
          <v-list-item-action>
            <v-icon>mdi-network</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Devices</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <!-- Platforms -->
        <v-list-item to="/search/platforms" exact nuxt>
          <v-list-item-action>
            <v-icon>mdi-rocket</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Platforms</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <!-- Configurations -->
        <v-list-item to="/search/configurations" exact nuxt>
          <v-list-item-action>
            <v-icon>mdi-file-cog</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Configurations</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <!-- Projects -->
        <v-list-item to="/projects" exact nuxt>
          <v-list-item-action>
            <v-icon>mdi-nature-people</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Projects</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <!-- Users -->
        <v-list-item to="/users" exact nuxt>
          <v-list-item-action>
            <v-icon>mdi-account-multiple</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Users</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider />

        <!-- Help -->
        <v-list-item to="/help" nuxt exact>
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
      <template v-if="appBarContent">
        <Component :is="appBarContent" />
      </template>
      <template v-else>
        <v-toolbar-title v-text="title" />
      </template>
      <template v-if="appBarExtension" v-slot:extension>
        <Component :is="appBarExtension" />
      </template>
    </v-app-bar>
    <v-content>
      <v-container>
        <v-snackbar v-model="hasSuccess" top color="green">
          {{ success }}
          <template v-slot:action="{ attrs }">
            <v-btn fab small v-bind="attrs" @click="closeSuccessSnackbar">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </template>
        </v-snackbar>
        <v-snackbar v-model="hasError" top color="error">
          {{ error }}
          <template v-slot:action="{ attrs }">
            <v-btn fab small v-bind="attrs" @click="closeErrorSnackbar">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </template>
        </v-snackbar>
        <nuxt />
      </v-container>
    </v-content>
    <v-footer
      :fixed="fixed"
      app
    >
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>

export default {
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
  computed: {
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
    }
  }
}
</script>
