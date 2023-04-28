<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
    <ProgressIndicator
      v-model="isLoading"
      color="primary"
    />
    <NuxtChild :is-fetching="isLoading" />
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

import ProgressIndicator from '@/components/ProgressIndicator.vue'

@Component({
  components: { ProgressIndicator },
  methods: {
    ...mapActions('devices', ['loadDeviceMeasuredQuantities']),
    ...mapActions('vocabulary', ['loadCompartments', 'loadSamplingMedia', 'loadProperties', 'loadUnits', 'loadMeasuredQuantityUnits', 'loadAggregationtypes'])
  }
})
export default class DevicePropertiesPage extends Vue {
  private isLoading = false

  // vuex definition for typescript check
  loadDeviceMeasuredQuantities!: LoadDeviceMeasuredQuantitiesAction
  loadCompartments!: LoadCompartmentsAction
  loadSamplingMedia!: LoadSamplingMediaAction
  loadProperties!: LoadPropertiesAction
  loadUnits!: LoadUnitsAction
  loadMeasuredQuantityUnits!: LoadMeasuredQuantityUnitsAction
  loadAggregationtypes!: LoadAggregationtypesAction

  async fetch (): Promise<void> {
    try {
      this.isLoading = true
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
      this.isLoading = false
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
