<!--
 SPDX-FileCopyrightText: 2020 - 2024

SPDX-License-Identifier: EUPL-1.2
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
          :devices="availableDevices"
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
          :devices="availableDevices"
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
import { mapGetters, mapState } from 'vuex'

import TsmLinkingMeasuredQuantitySelect from '@/components/configurations/tsmLinking/TsmLinkingMeasuredQuantitySelect.vue'
import TsmLinkingInformation from '@/components/configurations/tsmLinking/TsmLinkingInformation.vue'
import TsmLinkingReview from '@/components/configurations/tsmLinking/TsmLinkingReview.vue'
import TsmLinkingDeviceMountActionSelect
  from '@/components/configurations/tsmLinking/TsmLinkingDeviceMountActionSelect.vue'
import {
  TsmDeviceMountPropertyCombination,
  TsmDeviceMountPropertyCombinationList
} from '@/utils/configurationInterfaces'
import { AvailableDevicesGetter, ConfigurationsState } from '@/store/configurations'
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
    ...mapState('tsmLinking', ['linkings', 'newLinkings']),
    ...mapGetters('configurations', ['availableDevices'])
  }
})
export default class TsmLinkingAddStepperPage extends Vue {
  private step = 1

  private selectedDeviceActionPropertyCombinations: TsmDeviceMountPropertyCombinationList = []

  // vuex definition for typescript check
  newLinkings!: ITsmLinkingState['newLinkings']
  deviceMountActionsIncludingDeviceInformation!: ConfigurationsState['deviceMountActionsIncludingDeviceInformation']
  availableDevices!: AvailableDevicesGetter

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
