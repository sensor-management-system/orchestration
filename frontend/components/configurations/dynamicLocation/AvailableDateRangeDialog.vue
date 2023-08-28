<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
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
  <v-dialog
    v-model="showDialog"
    max-width="600px"
  >
    <v-card>
      <v-card-title>Available Date Ranges</v-card-title>
      <v-card-subtitle>Available periods of the mounted devices are displayed here. Only time periods for devices that have measured quantities are displayed.</v-card-subtitle>
      <v-divider />
      <AvailableDateRanges
        @selected="emitDateRangeSelected"
      />
      <v-card-actions>
        <v-btn
          text
          @click="closeDialog"
        >
          Cancel
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import AvailableDateRanges from '@/components/configurations/dynamicLocation/AvailableDateRanges.vue'

@Component({
  components: { AvailableDateRanges }
})
export default class ActionAvailableDateRangeDialog extends Vue {
  @Prop({
    required: true,
    type: Boolean
  })
  readonly value!: boolean

  get showDialog (): boolean {
    return this.value
  }

  set showDialog (value: boolean) {
    this.$emit('input', value)
  }

  closeDialog () {
    this.showDialog = false
  }

  emitDateRangeSelected (action: DeviceMountAction) {
    this.$emit('date-range-selected', action)
  }
}
</script>

<style scoped>
</style>
