<!--
SPDX-FileCopyrightText: 2020 - 2024
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <v-container>
    <v-row dense>
      <v-col
        cols="4"
        class="font-weight-medium"
      >
        Device
      </v-col>
      <v-col
        cols="8"
        class="nowrap-truncate"
      >
        <ExtendedItemName :value="selectedDeviceAction.device" />
      </v-col>
    </v-row>
    <v-row dense>
      <v-col
        cols="4"
        class="font-weight-medium"
      >
        Measured Quantity
      </v-col>
      <v-col
        cols="8"
        class="nowrap-truncate"
      >
        {{ selectedMeasuredQuantity | generatePropertyTitle }}
      </v-col>
    </v-row>
    <v-row dense>
      <v-col
        cols="4"
        class="font-weight-medium"
      >
        Mount dates
      </v-col>
      <v-col
        cols="8"
        class="nowrap-truncate"
      >
        <tsm-linking-dates
          :from="selectedDeviceAction.beginDate"
          :to="selectedDeviceAction.endDate"
        />
      </v-col>
    </v-row>
    <v-row v-if="selectedDeviceAction.label" dense>
      <v-col
        cols="4"
        class="font-weight-medium"
      >
        Mount label
      </v-col>
      <v-col
        cols="8"
        class="nowrap-truncate"
      >
        {{ selectedDeviceAction.label }}
      </v-col>
    </v-row>
    <v-row dense>
      <v-col
        cols="4"
        class="font-weight-medium"
      >
        Offsets
      </v-col>
      <v-col
        cols="8"
        class="nowrap-truncate"
      >
        {{ getOffsets(selectedDeviceAction) }}
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import TsmLinkingDates from '@/components/configurations/tsmLinking/TsmLinkingDates.vue'
import { generatePropertyTitle } from '@/utils/stringHelpers'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { DeviceProperty } from '@/models/DeviceProperty'
import { IOffsets } from '@/utils/configurationInterfaces'
import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'

@Component({
  components: { ExtendedItemName, TsmLinkingDates },
  filters: { generatePropertyTitle }
})
export default class TsmLinkingFormItemHeader extends Vue {
  @Prop({
    required: true
  })
    selectedDeviceAction!: DeviceMountAction

  @Prop({
    required: true,
    type: Object
  })
    selectedMeasuredQuantity!: DeviceProperty

  getOffsets (valueWithOffsets: IOffsets): string {
    return `X = ${valueWithOffsets.offsetX} m | Y = ${valueWithOffsets.offsetY} m | Z = ${valueWithOffsets.offsetZ} m`
  }
}

</script>

<style scoped>

</style>
