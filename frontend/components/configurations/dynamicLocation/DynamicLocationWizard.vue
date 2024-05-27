<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-stepper
    v-model="step"
    vertical
  >
    <v-stepper-step
      editable
      step="1"
    >
      Select a date
      <small>The referenced time zone is UTC. </small>
    </v-stepper-step>
    <v-stepper-content step="1">
      <DynamicLocationActionDateForm
        ref="DynamicLocationActionDateFormWizard"
        :value="value"
        @input="update"
      />
      <v-btn
        color="primary"
        :disabled="!stepTwoIsSelectable"
        @click="step=2"
      >
        Continue
      </v-btn>
    </v-stepper-content>

    <v-stepper-step
      :editable="stepTwoIsSelectable"
      step="2"
    >
      Select devices &amp; location measurements
    </v-stepper-step>
    <v-stepper-content step="2">
      <DynamicLocationActionDeviceForm
        ref="DynamicLocationActionDeviceFormWizard"
        :value="value"
        @input="update"
      />
      <v-btn
        color="primary"
        :disabled="!stepThreeIsSelectable"
        @click="step=3"
      >
        Continue
      </v-btn>
    </v-stepper-content>

    <v-stepper-step
      :editable="stepThreeIsSelectable"
      step="3"
    >
      Add dynamic location information
    </v-stepper-step>
    <v-stepper-content step="3">
      <v-container>
        <v-row>
          <v-col cols="12">
            <DynamicLocationActionInfoForm
              ref="DynamicLocationActionInfoFormWizard"
              :value="value"
              @input="update"
            />
            <v-btn
              color="primary"
              :disabled="!stepFourIsSelectable"
              @click="step=4"
            >
              Continue
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-stepper-content>

    <v-stepper-step
      :editable="stepFourIsSelectable"
      step="4"
    >
      Submit
    </v-stepper-step>
    <v-stepper-content step="4">
      <v-container>
        <v-row>
          <v-col>
            <DynamicLocationWizardSubmitOverview :new-dynamic-location-action="value" />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <slot name="save" />
          </v-col>
        </v-row>
      </v-container>
    </v-stepper-content>
  </v-stepper>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'
import DynamicLocationActionDateForm
  from '@/components/configurations/dynamicLocation/DynamicLocationActionDateForm.vue'
import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import DynamicLocationActionDeviceForm
  from '@/components/configurations/dynamicLocation/DynamicLocationActionDeviceForm.vue'
import DynamicLocationActionInfoForm
  from '@/components/configurations/dynamicLocation/DynamicLocationActionInfoForm.vue'
import DynamicLocationWizardSubmitOverview
  from '@/components/configurations/dynamicLocation/DynamicLocationWizardSubmitOverview.vue'

@Component({
  components: {
    DynamicLocationWizardSubmitOverview,
    DynamicLocationActionInfoForm,
    DynamicLocationActionDeviceForm,
    DynamicLocationActionDateForm
  }
})
export default class DynamicLocationWizard extends Vue {
  @Prop({
    default: () => new DynamicLocationAction(),
    required: true,
    type: Object
  })
  readonly value!: DynamicLocationAction

  private step = 1
  private isMounted = false

  mounted () {
    this.isMounted = true
  }

  get stepTwoIsSelectable () {
    if (!this.isMounted) {
      return false
    }
    return this.validateFormDynamicLocationActionDateForm()
  }

  get stepThreeIsSelectable () {
    if (!this.isMounted) {
      return false
    }
    return this.stepTwoIsSelectable && this.validateFormDynamicLocationActionDeviceForm()
  }

  get stepFourIsSelectable () {
    if (!this.isMounted) {
      return false
    }
    return this.stepThreeIsSelectable && this.validateFormDynamicLocationActionInfoForm()
  }

  update (updatedLocationAction: DynamicLocationAction) {
    this.$emit('input', updatedLocationAction)
  }

  validateFormDynamicLocationActionDateForm () {
    return (this.$refs.DynamicLocationActionDateFormWizard as Vue & { validateForm: () => boolean }).validateForm()
  }

  validateFormDynamicLocationActionDeviceForm () {
    return (this.$refs.DynamicLocationActionDeviceFormWizard as Vue & { validateForm: () => boolean }).validateForm()
  }

  validateFormDynamicLocationActionInfoForm () {
    return (this.$refs.DynamicLocationActionInfoFormWizard as Vue & { validateForm: () => boolean }).validateForm()
  }

  public validateForm (): boolean {
    // separate calls to display the form errors in the steps otherwise only one form error would be shown
    const isValidDynamicLocationActionDateForm = this.validateFormDynamicLocationActionDateForm()
    const isValidDynamicLocationActionDeviceForm = this.validateFormDynamicLocationActionDeviceForm()
    const isValidDynamicLocationActionInfoForm = this.validateFormDynamicLocationActionInfoForm()

    return isValidDynamicLocationActionDateForm && isValidDynamicLocationActionDeviceForm && isValidDynamicLocationActionInfoForm
  }
}
</script>

<style scoped>

</style>
