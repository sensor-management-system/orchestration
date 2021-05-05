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
  <v-container>
    <v-form
      ref="datesForm"
      v-model="datesAreValid"
      @submit.prevent
    >
      <v-row>
        <v-col cols="12" md="6">
          <DatePicker
            :value="actionCopy.beginDate"
            label="Start date"
            :rules="[rules.startDate, rules.startDateNotNull]"
            @input="setStartDateAndValidate"
          />
        </v-col>
        <v-col cols="12" md="6">
          <DatePicker
            :value="actionCopy.endDate"
            label="End date"
            :rules="[rules.endDate]"
            @input="setEndDateAndValidate"
          />
        </v-col>
      </v-row>
    </v-form>
    <CommonActionForm
      ref="commonForm"
      :description="actionCopy.description"
      :contact="actionCopy.contact"
      :rules="[rules.contactNotNull]"
      @descriptionChange="setDescription"
      @contactChange="setContact"
    />
  </v-container>
</template>

<script lang="ts">
/**
 * @file provides a component for a Generic Device Actions form
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Component, Prop, Vue, Watch } from 'nuxt-property-decorator'

import { DateTime } from 'luxon'
import { stringToDate } from '@/utils/dateHelper'

import { Contact } from '@/models/Contact'
import { GenericDeviceAction } from '@/models/GenericDeviceAction'

import CommonActionForm from '@/components/CommonActionForm.vue'
import DatePicker from '@/components/DatePicker.vue'

/**
 * A class component for a form for Generic Device Actions
 * @extends Vue
 */
@Component({
  components: {
    CommonActionForm,
    DatePicker
  }
})
// @ts-ignore
export default class GenericDeviceActionForm extends Vue {
  private actionCopy: GenericDeviceAction = new GenericDeviceAction()
  private datesAreValid: boolean = true
  private rules: Object = {
    startDate: this.validateInputForStartDate,
    startDateNotNull: this.mustBeProvided('Start date'),
    endDate: this.validateInputForEndDate,
    contactNotNull: this.mustBeProvided('Contact')
  }

  /**
   * a GenericDeviceAction
   */
  @Prop({
    default: () => new GenericDeviceAction(),
    required: true,
    type: Object
  })
  // @ts-ignore
  readonly value!: GenericDeviceAction

  created () {
    this.actionCopy = GenericDeviceAction.createFromObject(this.value)
  }

  setDescription (value: string) {
    this.actionCopy.description = value
    this.$emit('input', this.actionCopy)
  }

  setContact (value: Contact | null) {
    this.actionCopy.contact = value
    this.$emit('input', this.actionCopy)
  }

  setStartDateAndValidate (aDate: DateTime | null) {
    this.actionCopy.beginDate = aDate
    if (this.actionCopy.endDate !== null) {
      this.checkValidationOfDates()
    }
    this.$emit('input', this.actionCopy)
  }

  setEndDateAndValidate (aDate: DateTime | null) {
    this.actionCopy.endDate = aDate
    if (this.actionCopy.beginDate !== null) {
      this.checkValidationOfDates()
    }
    this.$emit('input', this.actionCopy)
  }

  checkValidationOfDates () {
    return (this.$refs.datesForm as Vue & { validate: () => boolean }).validate()
  }

  validateInputForStartDate (v: string): boolean | string {
    // NOTE: as the internals of the DatePicker component work with strings,
    // the validation functions should expect strings, too
    if (v === null || v === '') {
      return true
    }
    if (!this.actionCopy.endDate) {
      return true
    }
    if (stringToDate(v) <= this.actionCopy.endDate) {
      return true
    }
    return 'Start date must not be after end date'
  }

  validateInputForEndDate (v: string): boolean | string {
    // NOTE: as the internals of the DatePicker component work with strings,
    // the validation functions should expect strings, too
    if (v === null || v === '') {
      return true
    }
    if (!this.actionCopy.beginDate) {
      return true
    }
    if (stringToDate(v) >= this.actionCopy.beginDate) {
      return true
    }
    return 'End date must not be before start date'
  }

  mustBeProvided (fieldname: string): (v: any) => boolean | string {
    const innerFunc: (v: any) => boolean | string = function (v: any) {
      if (v == null || v === '') {
        return fieldname + ' must be provided'
      }
      return true
    }
    return innerFunc
  }

  isValid (): boolean {
    return this.checkValidationOfDates() && (this.$refs.commonForm as Vue & { isValid: () => boolean }).isValid()
  }

  @Watch('value', { immediate: true, deep: true })
  // @ts-ignore
  onValueChanged (val: GenericDeviceAction) {
    this.actionCopy = GenericDeviceAction.createFromObject(val)
  }
}
</script>
