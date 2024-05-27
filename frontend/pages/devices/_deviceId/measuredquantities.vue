<!--
SPDX-FileCopyrightText: 2020 - 2024
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

import { LoadDeviceMeasuredQuantitiesAction } from '@/store/devices'
import {
  LoadCompartmentsAction,
  LoadSamplingMediaAction,
  LoadPropertiesAction,
  LoadUnitsAction,
  LoadMeasuredQuantityUnitsAction,
  LoadAggregationtypesAction
} from '@/store/vocabulary'

import { SetLoadingAction } from '@/store/progressindicator'

@Component({
  methods: {
    ...mapActions('devices', ['loadDeviceMeasuredQuantities']),
    ...mapActions('vocabulary', ['loadCompartments', 'loadSamplingMedia', 'loadProperties', 'loadUnits', 'loadMeasuredQuantityUnits', 'loadAggregationtypes']),
    ...mapActions('progressindicator', ['setLoading'])

  }
})
export default class DevicePropertiesPage extends Vue {
  // vuex definition for typescript check
  loadDeviceMeasuredQuantities!: LoadDeviceMeasuredQuantitiesAction
  loadCompartments!: LoadCompartmentsAction
  loadSamplingMedia!: LoadSamplingMediaAction
  loadProperties!: LoadPropertiesAction
  loadUnits!: LoadUnitsAction
  loadMeasuredQuantityUnits!: LoadMeasuredQuantityUnitsAction
  loadAggregationtypes!: LoadAggregationtypesAction
  setLoading!: SetLoadingAction

  async fetch (): Promise<void> {
    try {
      this.setLoading(true)
      await Promise.all([
        this.loadDeviceMeasuredQuantities(this.deviceId),
        this.loadCompartments(),
        this.loadSamplingMedia(),
        this.loadProperties(),
        this.loadUnits(),
        this.loadMeasuredQuantityUnits(),
        this.loadAggregationtypes()
      ])
    } catch (e) {
      this.$store.commit('snackbar/setError', 'Failed to fetch measured quantities')
    } finally {
      this.setLoading(false)
    }
  }

  get deviceId (): string {
    return this.$route.params.deviceId
  }

  head () {
    return {
      titleTemplate: 'Measured Quantities - %s'
    }
  }
}
</script>
