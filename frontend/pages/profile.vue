<!--
SPDX-FileCopyrightText: 2020 - 2023
- Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card v-if="contact" class="ma-2">
      <v-card-text @click.stop.prevent="toggleContactSection">
        <v-row no-gutters>
          <v-col class="text-subtitle-1">
            Contact info
          </v-col>
          <v-col align-self="end" class="text-right">
            <v-btn icon @click.stop.prevent="toggleContactSection">
              <v-icon>
                {{ isContactSectionVisible ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
              </v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
      <v-expand-transition>
        <v-card-text v-show="isContactSectionVisible">
          <p class="font-italic">
            This is the data that is visible for other users.
          </p>
          <v-row no-gutters>
            <v-col class="text-subtitle-2" :cols="firstCol">
              Given name
            </v-col>
            <v-col align-self="end" :cols="secondCol">
              {{ contact.givenName }}
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col class="text-subtitle-2" :cols="firstCol">
              Family name
            </v-col>
            <v-col align-self="end" :cols="secondCol">
              {{ contact.familyName }}
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col class="text-subtitle-2" :cols="firstCol">
              E-mail
            </v-col>
            <v-col align-self="end" :cols="secondCol">
              {{ contact.email }}
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col class="text-subtitle-2" :cols="firstCol">
              Website
            </v-col>
            <v-col align-self="end" :cols="secondCol">
              {{ contact.website }}
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col class="text-subtitle-2" :cols="firstCol">
              ORCID
            </v-col>
            <v-col align-self="end" :cols="secondCol">
              {{ contact.orcid }}
            </v-col>
          </v-row>
          <v-row no-gutters>
            <v-col class="text-subtitle-2" :cols="firstCol">
              Organization
            </v-col>
            <v-col align-self="end" :cols="secondCol">
              {{ contact.organization }}
            </v-col>
          </v-row>
          <v-card-actions v-show="isContactSectionVisible">
            <v-spacer />
            <v-btn color="primary" small :to="'/contacts/' + contactId">
              View contact page
            </v-btn>
          </v-card-actions>
        </v-card-text>
      </v-expand-transition>
    </v-card>
    <v-card class="ma-2">
      <v-card-text @click.stop.prevent="togglePersonalSection">
        <v-row>
          <v-col class="text-subtitle-1">
            IDP Personal info
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
        <v-card-text v-show="isPersonalSectionVisible">
          <p class="font-italic">
            This is the data that the IDP provides.
          </p>
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
              E-mail
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
        <v-card-text v-show="isExtendedSectionVisible">
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
        <v-card-text v-show="isOpenIdConnectSectionVisible">
          <v-row v-for="(value, claim) of notExplicitPrintedClaims" :key="claim" no-gutters>
            <v-col class="text-subtitle-2" :cols="firstCol">
              {{ claim }}
            </v-col>
            <v-col align-self="end" :cols="secondCol">
              {{ value }}
            </v-col>
          </v-row>
        </v-card-text>
      </v-expand-transition>
    </v-card>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'nuxt-property-decorator'

import { mapState, mapGetters, mapActions } from 'vuex'

import { PermissionGroup } from '@/models/PermissionGroup'
import { ContactIdGetter } from '@/store/permissions'
import { LoadContactAction } from '@/store/contacts'

@Component({
  filters: {
    getNames: (xs: PermissionGroup[]): string[] => {
      return xs.map(x => x.name)
    }
  },
  middleware: ['auth'],
  computed: {
    ...mapGetters('permissions', ['memberedPermissionGroups', 'administradedPermissionGroups', 'apikey', 'isSuperUser', 'termsOfUseAgreementDate', 'contactId']),
    ...mapState('contacts', ['contact'])
  },
  methods: {
    ...mapActions('contacts', ['loadContact'])
  }
})
export default class ProfilePage extends Vue {
  private isOpenIdConnectSectionVisible: boolean = false
  private isPersonalSectionVisible: boolean = false
  private isExtendedSectionVisible: boolean = false
  private isContactSectionVisible: boolean = true
  private firstCol = 3
  private secondCol = 9

  contactId!: ContactIdGetter
  loadContact!: LoadContactAction

  created () {
    this.$store.dispatch('appbar/init', { title: 'Profile' })
    if (this.contactId) {
      this.loadContact(this.contactId)
    }
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

  toggleContactSection () {
    this.isContactSectionVisible = !this.isContactSectionVisible
  }

  @Watch('contactId')
  onContactIdChange (newContactIdValue: string | null) {
    if (newContactIdValue) {
      this.loadContact(newContactIdValue)
    }
  }
}

</script>
