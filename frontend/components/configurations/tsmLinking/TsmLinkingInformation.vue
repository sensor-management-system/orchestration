<!--
 SPDX-FileCopyrightText: 2020 - 2023

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <div>
    <template v-for="selectedDeviceActionMeasuredQuantities in deviceActionPropertyCombinations">
      <template v-for="selectedMeasuredQuantity in selectedDeviceActionMeasuredQuantities.measuredQuantities">
        <TsmLinkingFormItem
          ref="informationForm"
          :key="`${selectedDeviceActionMeasuredQuantities.action.id}-${selectedMeasuredQuantity.id}`"
          :selected-device-action-measured-quantities="selectedDeviceActionMeasuredQuantities"
          :selected-measured-quantity="selectedMeasuredQuantity"
          @input="update($event)"
        />
      </template>
    </template>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'nuxt-property-decorator'
import { mapState } from 'vuex'
import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import { generatePropertyTitle } from '@/utils/stringHelpers'
import TsmLinkingFormItem from '@/components/configurations/tsmLinking/TsmLinkingFormItem.vue'
import {
  TsmDeviceMountPropertyCombination,
  TsmDeviceMountPropertyCombinationList
} from '@/utils/configurationInterfaces'
import { TsmLinking } from '@/models/TsmLinking'
import { ITsmLinkingState } from '@/store/tsmLinking'
import { DeviceProperty } from '@/models/DeviceProperty'

@Component({
  components: { TsmLinkingFormItem, BaseExpandableListItem },
  computed: {
    ...mapState('tsmLinking', ['newLinkings'])
  },
  filters: { generatePropertyTitle }
})
export default class TsmLinkingInformation extends Vue {
  @Prop({
    required: true,
    type: Array
  })
  private deviceActionPropertyCombinations!: TsmDeviceMountPropertyCombinationList

  private isValid = false

  // vuex definition for typescript check
  newLinkings!: ITsmLinkingState['newLinkings']

  update (newLinking: TsmLinking) {
    const copyValue = this.newLinkings.slice()
    const foundIndex = copyValue.findIndex((el) => {
      return el.device?.id === newLinking.device?.id &&
        el.deviceProperty?.id === newLinking.deviceProperty?.id &&
        el.deviceMountAction?.id === newLinking.deviceMountAction?.id
    })

    if (foundIndex !== -1) {
      copyValue[foundIndex] = newLinking
    } else {
      copyValue.push(newLinking)
    }

    this.$store.commit('tsmLinking/setNewLinkings', copyValue)
  }

  public validateForm (): boolean {
    const formsArray = this.$refs.informationForm as Array<Vue & { validateForm: () => boolean }>
    return formsArray.every(el => el.validateForm())
  }

  @Watch('deviceActionPropertyCombinations', {
    deep: true,
    immediate: true
  })
  onDeviceActionPropertyCombinationsChange (value: TsmDeviceMountPropertyCombinationList) {
    // remove from tsm linking if measured quantities got unselected
    const copyValue = this.newLinkings.slice()

    const arrayWithRemovedMeasuredQuantities = copyValue.filter((el: TsmLinking) => {
      const foundEntry = value.find((combination: TsmDeviceMountPropertyCombination) => {
        return combination.action.id === el.deviceMountAction?.id && combination.action.device.id === el.device?.id
      })
      if (!foundEntry) {
        return false
      }
      const foundQuantity = foundEntry.measuredQuantities.find((measuredQuantity: DeviceProperty) => {
        return measuredQuantity.id === el.deviceProperty?.id
      })
      if (!foundQuantity) {
        return false
      }
      return true
    })

    this.$store.commit('tsmLinking/setNewLinkings', arrayWithRemovedMeasuredQuantities)
  }
}
</script>

<style scoped>

</style>
