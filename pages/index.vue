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
  <v-container>
    <v-row>
      <v-col class="text-center">
        <v-btn
          v-if="isLoggedIn"
          color="primary"
          @click="silentRenew"
        >
          Silent Renew
        </v-btn>
      </v-col>
    </v-row>
    <v-row
      v-if="isLoggedIn"
      class="text-center"
    >
      <v-col>
        <h1><kbd>{{ username }}</kbd> you're now logged in.</h1>
        <h2>Go check you Profile</h2>
        <v-btn to="/profile">
          Show Profile
        </v-btn>
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="12">
        <h1>Welcome to the Sensor Management System</h1>
        <p>The purpose of this application is to help scientists and technicans to...</p>
        <p>
          If you don't have an account, you can browse and view all datasets.<br>
          If you're already registered, you can login above.
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>

export default {
  name: 'Home',
  data: () => ({
  }),
  computed: {
    isLoggedIn () {
      return this.$store.getters['auth/isAuthenticated']
    },
    username () {
      return this.$store.getters['auth/username']
    }
  },
  mounted () {
    this.$store.dispatch('auth/loadStoredUser')
  },
  methods: {
    loginPopup () {
      this.$store.dispatch('auth/loginPopup')
    },
    logoutPopup () {
      const routing = {
        router: this.$router,
        currentRoute: this.$route.path
      }
      this.$store.dispatch('auth/logoutPopup', routing)
    },
    silentRenew () {
      this.$store.dispatch('auth/silentRenew')
    }
  }
}
</script>
