<!--
SPDX-FileCopyrightText: 2020 - 2022
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Erik Pongratz <erik.pongratz@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

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
  LoadAllConfigurationActionsAction
} from '@/store/configurations'

import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  methods: {
    ...mapActions('configurations', ['loadAllConfigurationActions']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class ConfigurationActions extends Vue {
  loadAllConfigurationActions!: LoadAllConfigurationActionsAction
  setLoading!: SetLoadingAction

  head () {
    return {
      titleTemplate: 'Actions - %s'
    }
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  async fetch () {
    try {
      this.setLoading(true)
      await this.loadAllConfigurationActions(this.configurationId)
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch actions')
    } finally {
      this.setLoading(false)
    }
  }
}
</script>

<style scoped>

</style>
