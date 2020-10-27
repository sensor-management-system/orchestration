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
  <div>
    <template v-if="!claims">
      You try to access the page without login.
    </template>
    <template v-else>
      <v-card class="ma-2">
        <v-card-text @click.stop.prevent="togglePersonalSection">
          <v-row>
            <v-col class="text-subtitle-1">
              Personal info
            </v-col>
            <v-col align-self="end" class="text-right">
              <b-btn icon @click.stop.prevent="togglePersonalSection">
                <v-icon>
                  {{ isPersonalSectionVisible ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
                </v-icon>
              </b-btn>
            </v-col>
          </v-row>
        </v-card-text>

        <v-expand-transition>
          <v-card v-show="isPersonalSectionVisible" flat tile color="grey lighten-5">
            <v-card-text>
              <v-row no-gutters>
                <v-col class="text-subtitle-2" :cols="firstCol">
                  Name
                </v-col>
                <v-col align-self="end" :cols="secondCol">
                  {{ claims.name }}
                </v-col>
              </v-row>
              <v-row no-gutters>
                <v-col class="text-subtitle-2" :cols="firstCol">
                  User name
                </v-col>
                <v-col align-self="end" :cols="secondCol">
                  {{ claims.preferred_username }}
                </v-col>
              </v-row>
              <v-row no-gutters>
                <v-col class="text-subtitle-2" :cols="firstCol">
                  Email address
                </v-col>
                <v-col align-self="end" :cols="secondCol">
                  {{ claims.email }}
                </v-col>
              </v-row>
              <v-row no-gutters>
                <v-col class="text-subtitle-2" :cols="firstCol">
                  Given name
                </v-col>
                <v-col align-self="end" :cols="secondCol">
                  {{ claims.given_name }}
                </v-col>
              </v-row>
              <v-row no-gutters>
                <v-col class="text-subtitle-2" :cols="firstCol">
                  Family name
                </v-col>
                <v-col align-self="end" :cols="secondCol">
                  {{ claims.family_name }}
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-expand-transition>
      </v-card>
      <v-card class="ma-2">
        <v-card-text @click.stop.prevent="toggleOpenIdConnectSection">
          <v-row>
            <v-col class="text-subtitle-1">
              OpenID Connect
            </v-col>
            <v-col align-self="end" class="text-right">
              <b-btn icon @click.stop.prevent="toggleOpenIdConnectSection">
                <v-icon>
                  {{ isOpenIdConnectSectionVisible ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
                </v-icon>
              </b-btn>
            </v-col>
          </v-row>
        </v-card-text>
        <v-expand-transition>
          <v-card v-show="isOpenIdConnectSectionVisible" flat tile color="grey lighten-5">
            <v-card-text>
              <v-row v-for="(value, claim) of notExplicitPrintedClaims" :key="claim" no-gutters>
                <v-col class="text-subtitle-2" :cols="firstCol">
                  {{ claim }}
                </v-col>
                <v-col align-self="end" :cols="secondCol">
                  {{ value }}
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-expand-transition>
      </v-card>
      <v-card class="ma-2">
        <v-card-text @click.stop.prevent="toggleTokenSection">
          <v-row>
            <v-col class="text-subtitle-1">
              Token
            </v-col>
            <v-col align-self="end" class="text-right">
              <b-btn icon @click.stop.prevent="toggleTokenSection">
                <v-icon>
                  {{ isTokenSectionVisible ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
                </v-icon>
              </b-btn>
            </v-col>
          </v-row>
        </v-card-text>
        <v-expand-transition>
          <v-card v-show="isTokenSectionVisible" flat tile color="grey lighten-5">
            <v-card-text>
              <v-row no-gutters>
                <v-col class="text-subtitle-2" :cols="firstCol">
                  Authentification
                </v-col>
                <v-col align-self="end" :cols="secondCol">
                  {{ claims.auth_time | timeStampToUTCDateTime }}
                </v-col>
              </v-row>
              <v-row no-gutters>
                <v-col class="text-subtitle-2" :cols="firstCol">
                  Your token expires
                </v-col>
                <v-col align-self="end" :cols="secondCol">
                  {{ claims.exp | timeStampToUTCDateTime }}
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-expand-transition>
      </v-card>
    </template>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import AppBarEditModeContent from '@/components/AppBarEditModeContent.vue'

import { timeStampToUTCDateTime } from '@/utils/dateHelper'

@Component({
  filters: {
    timeStampToUTCDateTime
  }
})
export default class ProfilePage extends Vue {
  private isOpenIdConnectSectionVisible: boolean = false
  private isPersonalSectionVisible: boolean = true
  private isTokenSectionVisible: boolean = false

  created () {
    this.$nuxt.$emit('app-bar-content', AppBarEditModeContent)
  }

  mounted () {
    this.$nextTick(() => {
      this.$nuxt.$emit('AppBarContent:title', 'Profile')
    })
  }

  beforeDestroy () {
    this.$nuxt.$emit('app-bar-content', null)
  }

  get userName (): string {
    return this.claims.name
  }

  get claims () {
    return this.$store.getters['oidc/allUserClaims']
  }

  get notExplicitPrintedClaims () {
    return this.objectWithoutKeys(this.claims, [
      'name', 'email', 'given_name',
      'family_name', 'preferred_username', 'exp',
      'auth_time'
    ])
  }

  objectWithoutKeys (object: {[idx: string]: any}, keys: string[]) {
    const result: {[idx:string]: any} = {}
    for (const key in object) {
      if (!keys.includes(key)) {
        result[key] = object[key]
      }
    }
    return result
  }

  get firstCol () { return 3 }
  get secondCol () { return 9 }

  toggleOpenIdConnectSection () {
    this.isOpenIdConnectSectionVisible = !this.isOpenIdConnectSectionVisible
  }

  togglePersonalSection () {
    this.isPersonalSectionVisible = !this.isPersonalSectionVisible
  }

  toggleTokenSection () {
    this.isTokenSectionVisible = !this.isTokenSectionVisible
  }
}

</script>

<style scoped>
.profile-card {
  background-color: #fff;
  color: #000;
  padding: 15vmin 20vmin;
  text-align: center;
}

.profile-card__title {
  margin: 0;
  font-size: 36px;
}

.profile-card__subtitle {
  margin: 0;
  color: #c0c0c0;
  font-size: 18px;
  margin-bottom: 5px;
}
</style>
