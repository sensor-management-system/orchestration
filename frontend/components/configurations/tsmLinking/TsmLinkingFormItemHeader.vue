<!--
 Web client of the Sensor Management System software developed within the
 Helmholtz DataHub Initiative by GFZ and UFZ.

 Copyright (C) 2020 - 2023
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
