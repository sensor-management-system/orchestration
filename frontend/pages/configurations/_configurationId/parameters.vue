<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <NuxtChild />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapActions } from 'vuex'

import {
  LoadConfigurationParametersAction,
  LoadConfigurationParameterChangeActionsAction
} from '@/store/configurations'
import { LoadUnitsAction } from '@/store/vocabulary'
import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  methods: {
    ...mapActions('configurations', ['loadConfigurationParameters', 'loadConfigurationParameterChangeActions']),
    ...mapActions('vocabulary', ['loadUnits']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationParametersPage extends Vue {
  // vuex definition for typescript check
  loadConfigurationParameters!: LoadConfigurationParametersAction
  loadConfigurationParameterChangeActions!: LoadConfigurationParameterChangeActionsAction
  loadUnits!: LoadUnitsAction
  setLoading!: SetLoadingAction

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadConfigurationParameters(this.configurationId),
        this.loadConfigurationParameterChangeActions(this.configurationId),
        this.loadUnits()
      ])
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch parameters')
    } finally {
      this.setLoading(false)
    }
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  head () {
    return {
      titleTemplate: 'Parameters - %s'
    }
  }
}
</script>
