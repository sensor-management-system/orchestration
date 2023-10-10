<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
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
  <div>
    <v-form
      ref="datesForm"
      @submit.prevent
    >
      <v-row>
        <v-col cols="12" md="6">
          <DateTimePicker
            :value="actionCopy.currentCalibrationDate"
            label="Current calibration date"
            placeholder="e.g 2000-01-31 12:00"
            :required="true"
            :rules="[rules.currentCalibrationDate,rules.currentCalibrationDateNotNull]"
            @input="setCurrentCalibrationDateAndValidate"
          />
        </v-col>
        <v-col>
          <DateTimePicker
            :value="actionCopy.nextCalibrationDate"
            label="Next calibration date"
            placeholder="e.g. 2000-01-31 12:00"
            :rules="[rules.nextCalibrationDate]"
            @input="setNextCalibrationDateAndValidate"
          />
        </v-col>
      </v-row>
    </v-form>
    <v-row>
      <v-col cols="12" md="6">
        <autocomplete-text-input
          :value="actionCopy.formula"
          label="Formula"
          endpoint="device-calibration-action-formulas"
          @input="setFormula"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          :value="actionCopy.value"
          label="Value"
          type="number"
          step="any"
          @wheel.prevent
          @input="setValue"
        />
      </v-col>
    </v-row>
    <v-form
      ref="measuredQuanititiesForm"
      @submit.prevent
    >
      <v-row>
        <v-col cols="12">
          <!-- While it would be possible to add a rule here, so that
               it needs at least one device property selected, I skip it
               for now.
               The rule is still there, so in the case we want to introduce
               it again, we can do so easily by adding

               :rules="[rules.measuredQuantitiesNotEmpty]"

               to the v-select tag.
          -->
          <v-select
            :value="actionCopy.measuredQuantities"
            multiple
            clearable
            label="Affected measured quantities"
            :items="measuredQuantities"
            :item-text="(x) => x.toString()"
            return-object
            @input="setMeasuredQuantities"
          />
        </v-col>
      </v-row>
    </v-form>
    <CommonActionForm
      ref="commonForm"
      :value="actionCopy"
      :attachments="attachments"
      :rules="[rules.contactNotNull]"
      :current-user-mail="currentUserMail"
      @input="updateCommonFields"
    />
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component for a Device Calibration Action form
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Component, Prop, Vue, Watch } from 'nuxt-property-decorator'

import { DateTime } from 'luxon'

import { Attachment } from '@/models/Attachment'
import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'
import { ActionCommonDetails } from '@/models/ActionCommonDetails'
import { DeviceProperty } from '@/models/DeviceProperty'

import CommonActionForm from '@/components/actions/CommonActionForm.vue'
import DateTimePicker from '@/components/DateTimePicker.vue'
import AutocompleteTextInput from '@/components/shared/AutocompleteTextInput.vue'

/**
 * A class component for a form for Device calibration actions
 * @extends Vue
 */
@Component({
  components: {
    CommonActionForm,
    DateTimePicker,
    AutocompleteTextInput
  }
})
export default class DeviceCalibationActionForm extends Vue {
  private actionCopy: DeviceCalibrationAction = new DeviceCalibrationAction()
  private rules: Object = {
    currentCalibrationDate: this.validateInputForCurrentCalibrationDate,
    currentCalibrationDateNotNull: this.mustBeProvided('Current calibration date'),
    nextCalibrationDate: this.validateInputForNextCalibrationDate,
    contactNotNull: this.mustBeProvided('Contact'),
    measuredQuantitiesNotEmpty: this.measuredQuantitiesNotEmpty
  }

  /**
   * a DeviceCalibrationAction
   */
  @Prop({
    default: () => new DeviceCalibrationAction(),
    required: true,
    type: Object
  })
  readonly value!: DeviceCalibrationAction

  /**
   * a list of available attachments
   */
  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  // @ts-ignore
  readonly attachments!: Attachment[]

  @Prop({
    default: () => [],
    required: true,
    type: Array
  })
  readonly measuredQuantities!: DeviceProperty[]

  @Prop({
    type: String
  })
  // @ts-ignore
  readonly currentUserMail: string | null

  created () {
    this.createActionCopy(this.value)
  }

  setCurrentCalibrationDateAndValidate (aDate: DateTime | null) {
    this.actionCopy.currentCalibrationDate = aDate
    if (this.actionCopy.nextCalibrationDate !== null) {
      this.checkValidationOfDates()
    }
    this.$emit('input', this.actionCopy)
  }

  setNextCalibrationDateAndValidate (aDate: DateTime | null) {
    this.actionCopy.nextCalibrationDate = aDate
    if (this.actionCopy.currentCalibrationDate !== null) {
      this.checkValidationOfDates()
    }
    this.$emit('input', this.actionCopy)
  }

  setFormula (formula: string) {
    this.actionCopy.formula = formula
    this.$emit('input', this.actionCopy)
  }

  setValue (value: any) {
    // The input mostly gives back strings
    if (value === null || value === '') {
      this.actionCopy.value = null
    } else {
      this.actionCopy.value = parseFloat(value)
    }
    this.$emit('input', this.actionCopy)
  }

  setMeasuredQuantities (measuredQuantities: DeviceProperty[]) {
    this.actionCopy.measuredQuantities = measuredQuantities.map((m: DeviceProperty) => DeviceProperty.createFromObject(m))
    this.$emit('input', this.actionCopy)
  }

  updateCommonFields (action: ActionCommonDetails) {
    this.actionCopy.description = action.description
    this.actionCopy.contact = action.contact
    this.actionCopy.attachments = action.attachments.map((a: Attachment) => Attachment.createFromObject(a))
    this.$emit('input', this.actionCopy)
  }

  checkValidationOfDates () {
    return (this.$refs.datesForm as Vue & { validate (): boolean }).validate()
  }

  validateInputForCurrentCalibrationDate (): boolean | string {
    if (!this.actionCopy.currentCalibrationDate) {
      return true
    }
    if (!this.actionCopy.nextCalibrationDate) {
      return true
    }
    if (this.actionCopy.currentCalibrationDate <= this.actionCopy.nextCalibrationDate) {
      return true
    }
    return 'Current calibration date must not be after next calibration date'
  }

  validateInputForNextCalibrationDate (): boolean | string {
    if (!this.actionCopy.nextCalibrationDate) {
      return true
    }
    if (!this.actionCopy.currentCalibrationDate) {
      return true
    }
    if (this.actionCopy.nextCalibrationDate >= this.actionCopy.currentCalibrationDate) {
      return true
    }
    return 'Next calibration date must not be before current calibration date'
  }

  /**
   * a rule to check that an field is non-empty
   *
   * @param {string} fieldname - the (human readable) label of the field
   * @return {(v: any) => boolean | string} a function that checks whether the field is valid or an error message
   */
  mustBeProvided (fieldname: string): (v: any) => boolean | string {
    const innerFunc: (v: any) => boolean | string = function (v: any) {
      if (v == null || v === '') {
        return fieldname + ' must be provided'
      }
      return true
    }
    return innerFunc
  }

  measuredQuantitiesNotEmpty (selectedMeasuredQuantities: DeviceProperty[]): boolean | string {
    // in case that there are no measured quantities at all to use, we don't want
    // to complain about that
    if (this.measuredQuantities.length === 0) {
      return true
    }
    if (selectedMeasuredQuantities.length !== 0) {
      return true
    }
    return 'Measured quantities must be selected'
  }

  checkValidationOfCommonForm () {
    return (this.$refs.commonForm as Vue & { isValid: () => boolean }).isValid()
  }

  checkValidationOfMeasuredQuantitiesForm () {
    return (this.$refs.measuredQuanititiesForm as Vue & { validate (): boolean }).validate()
  }

  isValid (): boolean {
    const checkDates = this.checkValidationOfDates()
    const checkCommonForm = this.checkValidationOfCommonForm()
    const checkMeasuredQuantities = this.checkValidationOfMeasuredQuantitiesForm()
    // By running them all before the && we make sure that all
    // of them are checked. This way the user can see all the problems
    // at once. (With using the methods directly with the && the user
    // would see the problems with the dates, then fixes those just to
    // see then that there must be a contact in the common form part)
    // The need to do so is annoying. So we will show them all at once here.
    return checkDates && checkCommonForm && checkMeasuredQuantities
  }

  createActionCopy (action: DeviceCalibrationAction): void {
    this.actionCopy = DeviceCalibrationAction.createFromObject(action)
  }

  @Watch('value', { immediate: true, deep: true })
  onValueChanged (val: DeviceCalibrationAction) {
    this.createActionCopy(val)
  }
}
</script>
