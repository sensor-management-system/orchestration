<!--
 SPDX-FileCopyrightText: 2020 - 2023

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <base-expandable-list-item>
    <template #header>
      <TsmLinkingFormItemHeader
        :selected-device-action="selectedDeviceActionMeasuredQuantities.action"
        :selected-measured-quantity="selectedMeasuredQuantity"
      />
    </template>
    <template #expandable>
      <TsmLinkingForm
        ref="tsmLinkingFormItemForm"
        v-model="newLinking"
        :selected-device-action-property-combination="selectedDeviceActionMeasuredQuantities"
        @input="update"
      />
    </template>
  </base-expandable-list-item>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import BaseExpandableListItem from '@/components/shared/BaseExpandableListItem.vue'
import TsmLinkingForm from '@/components/configurations/tsmLinking/TsmLinkingForm.vue'
import { TsmLinking } from '@/models/TsmLinking'
import TsmLinkingFormItemHeader from '@/components/configurations/tsmLinking/TsmLinkingFormItemHeader.vue'
import { TsmDeviceMountPropertyCombination } from '@/utils/configurationInterfaces'
import { DeviceProperty } from '@/models/DeviceProperty'

@Component({
  components: { TsmLinkingFormItemHeader, TsmLinkingForm, BaseExpandableListItem }
})
export default class TsmLinkingFormItem extends Vue {
  @Prop({
    required: true
  })
    selectedDeviceActionMeasuredQuantities!: TsmDeviceMountPropertyCombination

  @Prop({
    required: true
  })
    selectedMeasuredQuantity!: DeviceProperty

  private newLinking: TsmLinking = new TsmLinking()

  created () {
    this.newLinking.deviceMountAction = this.selectedDeviceActionMeasuredQuantities.action
    this.newLinking.device = this.selectedDeviceActionMeasuredQuantities.action.device
    this.newLinking.deviceProperty = this.selectedMeasuredQuantity
    this.newLinking.configurationId = this.configurationId
    // Pre Set Start and End Date of the linking
    this.newLinking.startDate = this.selectedDeviceActionMeasuredQuantities.action.beginDate
    this.newLinking.endDate = this.selectedDeviceActionMeasuredQuantities.action.endDate
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  update (linking: TsmLinking) {
    this.$emit('input', linking)
  }

  public validateForm (): boolean {
    return (this.$refs.tsmLinkingFormItemForm as Vue & { validateForm: () => boolean }).validateForm()
  }
}
</script>

<style scoped>

</style>
