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
    <v-row>
      <v-col cols="12">
        <template v-for="actionMeasuredQuantity in value">
          <TsmLinkingMeasuredQuantitySelectItem
            :key="actionMeasuredQuantity.action.id"
            :action="actionMeasuredQuantity.action"
            @input="update(actionMeasuredQuantity,$event)"
          />
        </template>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import {
  TsmDeviceMountPropertyCombination,
  TsmDeviceMountPropertyCombinationList
} from '@/utils/configurationInterfaces'
import { DeviceProperty } from '@/models/DeviceProperty'
import TsmLinkingMeasuredQuantitySelectItem
  from '@/components/configurations/tsmLinking/TsmLinkingMeasuredQuantitySelectItem.vue'

@Component({
  components: { TsmLinkingMeasuredQuantitySelectItem }
})
export default class TsmLinkingMeasuredQuantitySelect extends Vue {
  @Prop({
    required: true,
    type: Array
  })
  private value!: TsmDeviceMountPropertyCombinationList

  update (actionMeasuredQuantity: TsmDeviceMountPropertyCombination, newMeasuredQuantities: DeviceProperty[]) {
    const updatedDeviceActionPropertyCombinations = this.value.slice()
    const found = updatedDeviceActionPropertyCombinations.find((el) => {
      return el.action.id === actionMeasuredQuantity.action.id
    })
    if (found) {
      found.measuredQuantities = newMeasuredQuantities
    }
    this.$emit('input', updatedDeviceActionPropertyCombinations)
  }
}
</script>

<style scoped>

</style>
