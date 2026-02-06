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
        :complete="stepMeasuredQuantitiesSelectionIsSelectable && step > deviceMountActionSelectionStep"
        :step="deviceMountActionSelectionStep"
        edit-icon="mdi-check"
        editable
      >
        Select devices and date ranges
        <small>Select one or multiple devices.</small>
      </v-stepper-step>

      <v-stepper-content :step="deviceMountActionSelectionStep">
        <TsmLinkingDeviceMountActionSelect
          v-model="selectedDeviceActionPropertyCombinations"
          :device-mount-actions="deviceMountActionsIncludingDeviceInformation"
          :devices="availableDevices"
          :linkings="linkings"
        />
        <v-btn
          :disabled="!stepMeasuredQuantitiesSelectionIsSelectable"
          class="my-2"
          color="primary"
          @click="step++"
        >
          Continue
        </v-btn>
      </v-stepper-content>

      <v-stepper-step
        :complete="stepLinkingInformationIsSelectable && step > measuredQuantitiesSelectionStep"
        :editable="stepMeasuredQuantitiesSelectionIsSelectable"
        :step="measuredQuantitiesSelectionStep"
        edit-icon="mdi-check"
      >
        Select measured quantities
        <small>Select one or multiple measured quantities to link.</small>
      </v-stepper-step>

      <v-stepper-content :step="measuredQuantitiesSelectionStep">
        <TsmLinkingMeasuredQuantitySelect
          v-model="selectedDeviceActionPropertyCombinations"
        />
        <v-btn
          :disabled="!stepLinkingInformationIsSelectable"
          class="my-2"
          color="primary"
          @click="step++"
        >
          Continue
        </v-btn>
      </v-stepper-content>

      <v-stepper-step
        :complete="stepLinkingInformationIsSelectable && step > predefinedLinkingInformationStep"
        :editable="stepLinkingInformationIsSelectable"
        :step="predefinedLinkingInformationStep"
        edit-icon="mdi-check"
      >
        Set pre-defined linking information
        <small>Set information that should be used for each linking.</small>
      </v-stepper-step>
      <v-stepper-content :step="predefinedLinkingInformationStep">
        <TsmLinkingFormPredefinedSettings
          v-model="newLinkings"
        />
        <v-btn
          :disabled="!stepLinkingInformationIsSelectable"
          class="my-2"
          color="primary"
          @click="step++"
        >
          Continue
        </v-btn>
      </v-stepper-content>

      <v-stepper-step
        :complete="allLinkingFormsValid"
        :editable="stepLinkingInformationIsSelectable"
        :rules="[() => step > linkingInformationStep ? allLinkingFormsValid : true]"
        :step="linkingInformationStep"
        edit-icon="mdi-check"
      >
        Add linking information
        <small>Assign datastreams of time series management system.</small>
      </v-stepper-step>
      <v-stepper-content
        :step="linkingInformationStep"
        eager
      >
        <TsmLinkingInformation
          ref="tsmLinkingInformation"
          v-model="newLinkings"
          :device-action-property-combinations="selectedDeviceActionPropertyCombinations"
          :devices="availableDevices"
        />
        <v-btn
          :disabled="!stepReviewIsSelectable"
          class="my-2"
          color="primary"
          @click="step++"
        >
          Continue
        </v-btn>
      </v-stepper-content>

      <v-stepper-step
        :editable="stepReviewIsSelectable"
        :step="reviewStep"
      >
        Review and Submit
        <small>Confirm your inputs.</small>
      </v-stepper-step>
      <v-stepper-content
        :step="reviewStep"
      >
        <TsmLinkingReview
          :devices="availableDevices"
          :tsm-linkings="newLinkings"
          @scroll-to-form="scrollToForm"
        >
          <template #save>
            <v-btn
              :disabled="isLoading"
              block
              color="primary"
              @click="validateAndSave()"
            >
              Submit
            </v-btn>
          </template>
        </TsmLinkingReview>
      </v-stepper-content>
    </v-stepper>

    <TsmLinkingConfirmDialog
      v-model="showConfirmDialog"
      title="Confirm with missing information"
      @cancel="closeDialog"
      @confirm="confirmAndSave"
    >
      You have linkings without <span class="font-weight-bold">license information</span>.
      <p>
        Do you want to proceed?
      </p>
    </TsmLinkingConfirmDialog>
  </v-container>
</template>

<script lang="ts">
import { Component, PropSync, Vue, Watch } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import TsmLinkingMeasuredQuantitySelect
  from '@/components/configurations/tsmLinking/TsmLinkingMeasuredQuantitySelect.vue'
import TsmLinkingInformation from '@/components/configurations/tsmLinking/TsmLinkingInformation.vue'
import TsmLinkingReview from '@/components/configurations/tsmLinking/TsmLinkingReview.vue'
import TsmLinkingDeviceMountActionSelect
  from '@/components/configurations/tsmLinking/TsmLinkingDeviceMountActionSelect.vue'
import {
  TsmDeviceMountProperty,
  TsmDeviceMountPropertyCombination,
  TsmDeviceMountPropertyCombinationList
} from '@/utils/configurationInterfaces'
import { AvailableDevicesGetter, ConfigurationsState } from '@/store/configurations'
import TsmLinkingFormPredefinedSettings
  from '@/components/configurations/tsmLinking/TsmLinkingFormPredefinedSettings.vue'
import { TsmLinking } from '@/models/TsmLinking'
import TsmLinkingConfirmDialog from '@/components/configurations/tsmLinking/TsmLinkingConfirmDialog.vue'
import { LoadingSpinnerState, SetLoadingAction } from '@/store/progressindicator'
import { AddConfigurationTsmLinkingAction, LoadConfigurationTsmLinkingsAction } from '@/store/tsmLinking'

@Component({
  components: {
    TsmLinkingConfirmDialog,
    TsmLinkingFormPredefinedSettings,
    TsmLinkingDeviceMountActionSelect,
    TsmLinkingMeasuredQuantitySelect,
    TsmLinkingInformation,
    TsmLinkingReview
  },
  computed: {
    ...mapState('configurations', ['deviceMountActionsIncludingDeviceInformation', 'configuration']),
    ...mapState('tsmLinking', ['linkings']),
    ...mapGetters('configurations', ['availableDevices']),
    ...mapState('progressindicator', ['isLoading'])
  },
  methods: {
    ...mapActions('progressindicator', ['setLoading']),
    ...mapActions('tsmLinking', ['addConfigurationTsmLinking', 'loadConfigurationTsmLinkings'])
  }
})
export default class TsmLinkingWizard extends Vue {
  @PropSync('hasSaved', {
    required: false,
    type: Boolean
  })
    syncedHasSaved!: boolean

  // vuex definition for typescript check
  deviceMountActionsIncludingDeviceInformation!: ConfigurationsState['deviceMountActionsIncludingDeviceInformation']
  availableDevices!: AvailableDevicesGetter
  isLoading!: LoadingSpinnerState['isLoading']
  setLoading!: SetLoadingAction
  addConfigurationTsmLinking!: AddConfigurationTsmLinkingAction
  loadConfigurationTsmLinkings!: LoadConfigurationTsmLinkingsAction
  private step = 1
  private deviceMountActionSelectionStep = 1
  private measuredQuantitiesSelectionStep = 2
  private predefinedLinkingInformationStep = 3
  private linkingInformationStep = 4
  private reviewStep = 5
  private selectedDeviceActionPropertyCombinations: TsmDeviceMountPropertyCombinationList = []
  private allLinkingFormsValid: boolean = false
  private showConfirmDialog = false
  private newLinkings: TsmLinking[] = []
  private errorLinkings: TsmLinking[] = []

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get stepMeasuredQuantitiesSelectionIsSelectable (): boolean {
    return this.selectedDeviceActionPropertyCombinations.length > 0
  }

  get stepLinkingInformationIsSelectable (): boolean {
    return this.selectedDeviceActionPropertyCombinations.some((combination: TsmDeviceMountPropertyCombination) => {
      return combination.measuredQuantities.length > 0
    })
  }

  get stepReviewIsSelectable (): boolean {
    return this.newLinkings.length > 0
  }

  get newLinkingsWithMissingLicense () {
    return this.newLinkings.filter(linking => !linking.licenseName)
  }

  get redirectRoute () {
    return '/configurations/' + this.configurationId + '/tsm-linking'
  }

  get selectedDeviceActionPropertyCombinationsAsFlatArray () {
    return this.selectedDeviceActionPropertyCombinations
      .flatMap(combo => combo.measuredQuantities
        .map(measuredQuantity => ({
          action: combo.action,
          measuredQuantity
        }))
      )
  }

  created () {
    this.syncedHasSaved = false
  }

  validateAndSave () {
    if (this.newLinkings.length === 0) {
      return
    }

    if (!this.validateForm()) {
      this.$store.commit('snackbar/setError', 'At least one linking is invalid. Please correct your inputs in step "Add linking information"')
      return
    }

    if (this.newLinkingsWithMissingLicense.length > 0) {
      this.showConfirmDialog = true
      return
    }

    this.save()
  }

  async save () {
    this.setLoading(true)

    for (const newLinking of this.newLinkings) {
      try {
        await this.addConfigurationTsmLinking(newLinking)
      } catch (_e) {
        this.errorLinkings.push(newLinking)
      }
    }

    this.setLoading(false)
    this.syncedHasSaved = true

    if (this.errorLinkings.length > 0) {
      this.$store.commit('snackbar/setError', 'Save failed')
    } else {
      await this.loadConfigurationTsmLinkings(this.configurationId)
      this.$store.commit('snackbar/setSuccess', 'Linkings saved')
      this.$router.push(this.redirectRoute)
    }
  }

  async scrollToForm (linking: TsmLinking) {
    this.step = this.linkingInformationStep
    const target = `linking-form-item-${linking.deviceMountAction!.id}-${linking.deviceProperty!.id}`

    const tsmLinkingInformationRef = this.$refs.tsmLinkingInformation as TsmLinkingInformation

    await tsmLinkingInformationRef.closeAndOpenTarget(target)

    /*
     * Because of the unforseen internals of vue2/vuetify2 tsmLinkingInformationRef.closeAndOpenTarget(target)
     * does not scroll to the correct form when called outside of the component, but it does open the correct form
     * We use this additional timeout (after all animation/transition is done) and find the correct form element by it's
     * id and scroll to it
     */
    setTimeout(() => {
      const el = document.getElementById(target)
      if (!el) { return }

      el.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      })
    }, 1000)
  }

  validateForm (): boolean {
    this.allLinkingFormsValid = (this.$refs.tsmLinkingInformation as TsmLinkingInformation).validateForm()
    return this.allLinkingFormsValid
  }

  closeDialog () {
    this.showConfirmDialog = false
  }

  confirmAndSave () {
    this.closeDialog()
    this.save()
  }

  createNewLinking (entity: TsmDeviceMountProperty) {
    const existingNewLinking = this.newLinkings.find((el: TsmLinking) => {
      return el.device?.id === entity.action.device?.id &&
        el.deviceProperty?.id === entity.measuredQuantity?.id &&
        el.deviceMountAction?.id === entity.action?.id
    })

    if (existingNewLinking) {
      return existingNewLinking
    }

    const newLinking: TsmLinking = new TsmLinking()
    newLinking.deviceMountAction =
      entity.action
    newLinking.device =
      entity.action.device
    newLinking.deviceProperty = entity.measuredQuantity
    newLinking.configurationId = this.configurationId
    // Pre Set Start and End Date of the linking
    newLinking.startDate = entity.action.beginDate
    newLinking.endDate = entity.action.endDate

    return newLinking
  }

  @Watch('selectedDeviceActionPropertyCombinations', {
    deep: true,
    immediate: true
  })
  onDeviceActionPropertyCombinationsChange (_value: TsmDeviceMountPropertyCombinationList) {
    this.newLinkings = this.selectedDeviceActionPropertyCombinationsAsFlatArray.map(i => this.createNewLinking(i))
  }

  @Watch('step')
  private validateForReview () {
    if (this.step === this.reviewStep) {
      this.validateForm()
    }
  }
}

</script>

<style>
</style>
