<!--
 SPDX-FileCopyrightText: 2020 - 2023

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <div>
    <NuxtChild
      v-if="configuration"
    />
  </div>
</template>

<script lang="ts">
import { Component, mixins } from 'nuxt-property-decorator'
import { mapState, mapActions } from 'vuex'

import CheckEditAccess from '@/mixins/CheckEditAccess'

import { SetLoadingAction } from '@/store/progressindicator'
import { LoadDeviceMountActionsIncludingDeviceInformationAction } from '@/store/configurations'

@Component({
  computed: {
    ...mapState('configurations', ['configuration'])
  },
  methods: {
    ...mapActions('configurations', ['loadDeviceMountActionsIncludingDeviceInformation']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationNewTsmLinkingPageParent extends mixins(CheckEditAccess) {
  // vuex definition for typescript check
  loadDeviceMountActionsIncludingDeviceInformation!: LoadDeviceMountActionsIncludingDeviceInformationAction
  setLoading!: SetLoadingAction

  async created () {
    try {
      this.setLoading(true)
      // reset new linkings to remove cached data
      this.$store.commit('tsmLinking/setNewLinkings', [])
      await this.loadDeviceMountActionsIncludingDeviceInformation(this.configurationId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Loading device mount actions failed')
    } finally {
      this.setLoading(false)
    }
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }
}
</script>

<style scoped>

</style>
