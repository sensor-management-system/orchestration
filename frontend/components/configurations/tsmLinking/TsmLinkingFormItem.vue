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
