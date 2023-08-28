<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
  <div>
    <v-card class="ma-2">
      <v-card-text @click.stop.prevent="togglePersonalSection">
        <v-row>
          <v-col class="text-subtitle-1">
            Personal info
          </v-col>
          <v-col align-self="end" class="text-right">
            <v-btn icon @click.stop.prevent="togglePersonalSection">
              <v-icon>
                {{ isPersonalSectionVisible ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
              </v-icon>
            </v-btn>
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
                {{ $auth.user.name }}
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col class="text-subtitle-2" :cols="firstCol">
                User name
              </v-col>
              <v-col align-self="end" :cols="secondCol">
                {{ $auth.user.preferred_username }}
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col class="text-subtitle-2" :cols="firstCol">
                Email address
              </v-col>
              <v-col align-self="end" :cols="secondCol">
                {{ $auth.user.email }}
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col class="text-subtitle-2" :cols="firstCol">
                Given name
              </v-col>
              <v-col align-self="end" :cols="secondCol">
                {{ $auth.user.given_name }}
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col class="text-subtitle-2" :cols="firstCol">
                Family name
              </v-col>
              <v-col align-self="end" :cols="secondCol">
                {{ $auth.user.family_name }}
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-expand-transition>
    </v-card>
    <v-card class="ma-2">
      <v-card-text @click.stop.prevent="toggleExtendedSection">
        <v-row>
          <v-col class="text-subtitle-1">
            Extended
          </v-col>
          <v-col align-self="end" class="text-right">
            <v-btn icon @click.stop.prevent="toggleExtendedSection">
              <v-icon>
                {{ isExtendedSectionVisible ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
              </v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
      <v-expand-transition>
        <v-card v-show="isExtendedSectionVisible" flat tile color="grey lighten-5">
          <v-card-text>
            <v-row no-gutters>
              <v-col class="text-subtitle-2" :cols="firstCol">
                Apikey
              </v-col>
              <v-col align-self="end" :cols="secondCol">
                {{ apikey }}
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col class="text-subtitle-2" :cols="firstCol">
                Super user
              </v-col>
              <v-col align-self="end" :cols="secondCol">
                {{ isSuperUser }}
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col class="text-subtitle-2" :cols="firstCol">
                Terms of Use accepted
              </v-col>
              <v-col align-self="end" :cols="secondCol">
                {{ termsOfUseAgreementDate | toUtcDateTimeString }}
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col class="text-subtitle-2" :cols="firstCol">
                Membered permission groups
              </v-col>
              <v-col align-self="end" :cols="secondCol">
                {{ memberedPermissionGroups | getNames }}
              </v-col>
            </v-row>
            <v-row no-gutters>
              <v-col class="text-subtitle-2" :cols="firstCol">
                Administrated permission groups
              </v-col>
              <v-col align-self="end" :cols="secondCol">
                {{ administradedPermissionGroups | getNames }}
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
            <v-btn icon @click.stop.prevent="toggleOpenIdConnectSection">
              <v-icon>
                {{ isOpenIdConnectSectionVisible ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
              </v-icon>
            </v-btn>
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
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'

import { mapGetters } from 'vuex'

import { PermissionGroup } from '@/models/PermissionGroup'

@Component({
  filters: {
    getNames: (xs: PermissionGroup[]): string[] => {
      return xs.map(x => x.name)
    }
  },
  middleware: ['auth'],
  computed: mapGetters('permissions', ['memberedPermissionGroups', 'administradedPermissionGroups', 'apikey', 'isSuperUser', 'termsOfUseAgreementDate'])
})
export default class ProfilePage extends Vue {
  private isOpenIdConnectSectionVisible: boolean = false
  private isPersonalSectionVisible: boolean = true
  private isExtendedSectionVisible: boolean = false
  private firstCol = 3
  private secondCol = 9

  created () {
    this.$store.dispatch('appbar/init', { title: 'Profile' })
  }

  get notExplicitPrintedClaims () {
    return this.objectWithoutKeys(this.$auth.user as {[idx: string]: any}, [
      'name', 'email', 'given_name',
      'family_name', 'preferred_username', 'exp',
      'auth_time'
    ])
  }

  objectWithoutKeys (object: {[idx: string]: any}, keys: string[]) {
    const result: {[idx: string]: any} = {}
    for (const key in object) {
      if (!keys.includes(key)) {
        result[key] = object[key]
      }
    }
    return result
  }

  toggleOpenIdConnectSection () {
    this.isOpenIdConnectSectionVisible = !this.isOpenIdConnectSectionVisible
  }

  togglePersonalSection () {
    this.isPersonalSectionVisible = !this.isPersonalSectionVisible
  }

  toggleExtendedSection () {
    this.isExtendedSectionVisible = !this.isExtendedSectionVisible
  }
}

</script>
