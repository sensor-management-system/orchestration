<!--
 SPDX-FileCopyrightText: 2020 - 2024

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <div>
    <v-card-actions>
      <v-card-title class="pl-0">
        New Data Linking
      </v-card-title>
      <v-spacer />
      <v-btn
        v-if="$auth.loggedIn"
        small
        text
        nuxt
        :to="'/configurations/' + configurationId + '/tsm-linking'"
      >
        cancel
      </v-btn>
    </v-card-actions>

    <tsm-linking-wizard
      ref="tsmWizard"
      :has-saved.sync="hasSaved"
    />

    <NavigationGuardDialog
      v-model="showNavigationWarning"
      :has-entity-changed="true"
      :to="to"
      @close="to = null"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { RawLocation } from 'vue-router'

import TsmLinkingWizard from '@/components/configurations/tsmLinking/TsmLinkingWizard.vue'
import NavigationGuardDialog from '@/components/shared/NavigationGuardDialog.vue'

@Component({
  components: {
    NavigationGuardDialog,
    TsmLinkingWizard
  },
  middleware: ['auth']
})
export default class ConfigurationNewTsmLinkingPageChild extends Vue {
  private hasSaved = false
  private to: RawLocation | null = null
  private showNavigationWarning = false

  get configurationId () {
    return this.$route.params.configurationId
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  beforeRouteLeave (to: RawLocation, from: RawLocation, next: any) {
    if (!this.hasSaved) {
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
