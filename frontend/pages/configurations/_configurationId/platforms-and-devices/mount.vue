<!--
SPDX-FileCopyrightText: 2020 - 2022
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card-actions>
      <v-card-title class="pl-0">
        Mount devices or platforms
      </v-card-title>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        small
        text
        nuxt
        :to="'/configurations/' + configurationId + '/platforms-and-devices'"
      >
        cancel
      </v-btn>
    </v-card-actions>

    <mount-wizard v-if="configuration" :has-saved.sync="hasSaved" />

    <navigation-guard-dialog
      v-model="showNavigationWarning"
      :has-entity-changed="true"
      :to="to"
      @close="to = null"
    />
  </div>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'
import { mapState, mapActions } from 'vuex'
import { RawLocation } from 'vue-router'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import { ConfigurationsState, LoadConfigurationAction } from '@/store/configurations'
import { ContactsState, LoadAllContactsAction } from '@/store/contacts'

import MountWizard from '@/components/configurations/MountWizard.vue'

import { SetLoadingAction } from '@/store/progressindicator'
import NavigationGuardDialog from '@/components/shared/NavigationGuardDialog.vue'

@Component({
  components: {
    MountWizard,
    NavigationGuardDialog
  },
  middleware: ['auth'],
  computed: {
    ...mapState('configurations', ['configuration'])
  },
  methods: {
    ...mapActions('configurations', ['loadConfiguration']),
    ...mapActions('contacts', ['loadAllContacts']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationMountPlatformsAndDevicesPage extends mixins(CheckEditAccess) {
  configuration!: ConfigurationsState['configuration']
  loadConfiguration!: LoadConfigurationAction
  contacts!: ContactsState['contacts']
  loadAllContacts!: LoadAllContactsAction
  setLoading!: SetLoadingAction

  private showNavigationWarning: boolean = false
  private to: RawLocation | null = null
  private hasSaved = false

  /**
   * route to which the user is redirected when he is not allowed to access the page
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a valid route path
   */
  getRedirectUrl (): string {
    return '/configurations/' + this.configurationId + '/platforms-and-devices'
  }

  /**
   * message which is displayed when the user is redirected
   *
   * is called by CheckEditAccess#created
   *
   * @returns {string} a message string
   */
  getRedirectMessage (): string {
    return 'You\'re not allowed to edit this configuration.'
  }

  async created () {
    if (!this.configuration) {
      try {
        this.setLoading(true)
        await this.loadAllContacts()
        await this.loadConfiguration(this.configurationId)
        // })
      } catch (_e) {
        this.$store.commit('snackbar/setError', 'Failed to fetch configuration')
      } finally {
        this.setLoading(false)
      }
    }
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  beforeRouteLeave (to: RawLocation, from: RawLocation, next: any) {
    if (!this.hasSaved && this.editable) {
      if (this.to) {
        next()
      } else {
        this.to = to
        this.showNavigationWarning = true
      }
    } else {
      return next()
    }
  }
}
</script>

<style scoped>

</style>
