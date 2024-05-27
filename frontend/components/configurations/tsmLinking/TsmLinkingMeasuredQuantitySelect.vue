<!--
 SPDX-FileCopyrightText: 2020 - 2023

SPDX-License-Identifier: EUPL-1.2
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
