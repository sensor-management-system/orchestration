<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
- Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
  <v-container fill-height fluid>
    <v-row
      align="center"
      justify="center"
    >
      <v-col>
        <v-card>
          <v-alert type="error" class="text-center" :icon="false">
            <h1 class="display-4">
              Access not allowed!
            </h1>
            <h2 class="display-2">
              Log in!
            </h2>
          </v-alert>
        </v-card>
        <div class="text-center">
          <h4>Redirect Uri</h4>
          {{ $route.query.redirect }}
        </div>
        <div>
          <h4>IsLoggedIn</h4>
          {{ isLoggedIn }}
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'AccessDenied',
  computed: {
    isLoggedIn () {
      return this.$store.getters['oidc/isAuthenticated']
    }
  },
  watch: {
    isLoggedIn () {
      this.redirectUserIfLoggedIn()
    }
  },
  mounted () {
    this.redirectUserIfLoggedIn()
  },
  methods: {
    redirectUserIfLoggedIn () {
      if (this.isLoggedIn) {
        let redirectRoute = '/'
        if (this.$route.query.redirect !== undefined) {
          redirectRoute = this.$route.query.redirect
        }
        this.$router.push(redirectRoute)
      }
    }
  }
}
</script>
