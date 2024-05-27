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
  LoadPlatformParametersAction,
  LoadPlatformParameterChangeActionsAction
} from '@/store/platforms'
import { LoadUnitsAction } from '@/store/vocabulary'
import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  methods: {
    ...mapActions('platforms', ['loadPlatformParameters', 'loadPlatformParameterChangeActions']),
    ...mapActions('vocabulary', ['loadUnits']),
    ...mapActions('progressindicator', ['setLoading'])
  }
})
export default class PlatformParametersPage extends Vue {
  // vuex definition for typescript check
  loadPlatformParameters!: LoadPlatformParametersAction
  loadPlatformParameterChangeActions!: LoadPlatformParameterChangeActionsAction
  loadUnits!: LoadUnitsAction
  setLoading!: SetLoadingAction

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadPlatformParameters(this.platformId),
        this.loadPlatformParameterChangeActions(this.platformId),
        this.loadUnits()
      ])
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch parameters')
    } finally {
      this.setLoading(false)
    }
  }

  get platformId (): string {
    return this.$route.params.platformId
  }

  head () {
    return {
      titleTemplate: 'Parameters - %s'
    }
  }
}
</script>
