<!--
 Web client of the Sensor Management System software developed within the
 Helmholtz DataHub Initiative by GFZ and UFZ.

 Copyright (C) 2020 - 2024
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
    <v-stepper
      v-model="step"
      vertical
    >
      <v-stepper-step
        step="1"
        editable
      >
        Select devices and date ranges
        <small>Select one or multiple devices.</small>
      </v-stepper-step>

      <v-stepper-content step="1">
        <TsmLinkingDeviceMountActionSelect
          v-model="selectedDeviceActionPropertyCombinations"
          :linkings="linkings"
          :devices="availableDevices"
          :device-mount-actions="deviceMountActionsIncludingDeviceInformation"
        />
        <v-btn
          color="primary"
          :disabled="!stepTwoIsSelectable"
          @click="step++"
        >
          Continue
        </v-btn>
      </v-stepper-content>

      <v-stepper-step
        step="2"
        :editable="stepTwoIsSelectable"
      >
        Select measured quantities
        <small>Select one or multiple measured quantities to link.</small>
      </v-stepper-step>

      <v-stepper-content step="2">
        <TsmLinkingMeasuredQuantitySelect
          v-model="selectedDeviceActionPropertyCombinations"
        />
        <v-btn
          color="primary"
          :disabled="!stepThreeIsSelectable"
          @click="step++"
        >
          Continue
        </v-btn>
      </v-stepper-content>

      <v-stepper-step
        step="3"
        :editable="stepThreeIsSelectable"
      >
        Add linking information
        <small>Assign data streams of time series management system</small>
      </v-stepper-step>
      <v-stepper-content step="3">
        <TsmLinkingInformation
          ref="tsmLinkingInformation"
          :device-action-property-combinations="selectedDeviceActionPropertyCombinations"
        />
        <v-btn
          color="primary"
          :disabled="!stepFourIsSelectable"
          @click="step++"
        >
          Continue
        </v-btn>
      </v-stepper-content>

      <v-stepper-step
        :editable="stepFourIsSelectable"
        step="4"
      >
        Review and Submit
        <small>Confirm your inputs.</small>
      </v-stepper-step>
      <v-stepper-content
        step="4"
      >
        <TsmLinkingReview
          :tsm-linkings="newLinkings"
        >
          <template #save>
            <slot name="save" />
          </template>
        </TsmLinkingReview>
      </v-stepper-content>
    </v-stepper>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapState } from 'vuex'

import TsmLinkingMeasuredQuantitySelect from '@/components/configurations/tsmLinking/TsmLinkingMeasuredQuantitySelect.vue'
import { Device } from '@/models/Device'
import TsmLinkingInformation from '@/components/configurations/tsmLinking/TsmLinkingInformation.vue'
import TsmLinkingReview from '@/components/configurations/tsmLinking/TsmLinkingReview.vue'
import TsmLinkingDeviceMountActionSelect
  from '@/components/configurations/tsmLinking/TsmLinkingDeviceMountActionSelect.vue'
import {
  TsmDeviceMountPropertyCombination,
  TsmDeviceMountPropertyCombinationList
} from '@/utils/configurationInterfaces'
import { ConfigurationsState } from '@/store/configurations'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { ITsmLinkingState } from '@/store/tsmLinking'

@Component({
  components: {
    TsmLinkingDeviceMountActionSelect,
    TsmLinkingMeasuredQuantitySelect,
    TsmLinkingInformation,
    TsmLinkingReview
  },
  computed: {
    ...mapState('configurations', ['deviceMountActionsIncludingDeviceInformation', 'configuration']),
    ...mapState('tsmLinking', ['linkings', 'newLinkings'])
  }
})
export default class TsmLinkingAddStepperPage extends Vue {
  private step = 1

  private selectedDeviceActionPropertyCombinations: TsmDeviceMountPropertyCombinationList = []

  // vuex definition for typescript check
  newLinkings!: ITsmLinkingState['newLinkings']
  deviceMountActionsIncludingDeviceInformation!: ConfigurationsState['deviceMountActionsIncludingDeviceInformation']

  get availableDevices (): Device[] {
    const devices = this.deviceMountActionsIncludingDeviceInformation.map((mountAction: DeviceMountAction) => {
      return mountAction.device
    })

    const uniqueDevices = [...new Map(devices.map((device: Device) =>
      [device.id, device])).values()]

    return uniqueDevices
  }

  get stepTwoIsSelectable (): boolean {
    return this.selectedDeviceActionPropertyCombinations.length > 0
  }

  get stepThreeIsSelectable (): boolean {
    return this.selectedDeviceActionPropertyCombinations.some((combination: TsmDeviceMountPropertyCombination) => {
      return combination.measuredQuantities.length > 0
    })
  }

  get stepFourIsSelectable (): boolean {
    return this.newLinkings.length > 0
  }

  public validateForm (): boolean {
    return (this.$refs.tsmLinkingInformation as Vue & { validateForm: () => boolean }).validateForm()
  }
}

</script>

<style>
.sticky-top {
  position: sticky;
  top: 112px;
}
</style>
