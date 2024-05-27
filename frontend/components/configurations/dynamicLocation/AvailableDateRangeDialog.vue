<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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
