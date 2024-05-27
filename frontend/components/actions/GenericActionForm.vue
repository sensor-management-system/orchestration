<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-form
      ref="datesForm"
      v-model="datesAreValid"
      @submit.prevent
    >
      <v-row>
        <v-col cols="12" md="6">
          <DateTimePicker
            :value="actionCopy.beginDate"
            label="Start date"
            placeholder="e.g. 2000-01-31 12:00"
            :rules="[rules.startDate,rules.startDateNotNull]"
            :required="true"
            @input="setStartDateAndValidate"
          />
        </v-col>
        <v-col cols="12" md="6">
          <DateTimePicker
            :value="actionCopy.endDate"
            label="End date"
            placeholder="e.g. 2001-01-31 12:00"
            :rules="[rules.endDate]"
            @input="setEndDateAndValidate"
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
 * @file provides a component for a Generic Device Actions form
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Component, Prop, Vue, Watch } from 'nuxt-property-decorator'

import { DateTime } from 'luxon'

import { Attachment } from '@/models/Attachment'
import { GenericAction } from '@/models/GenericAction'
import { ActionCommonDetails } from '@/models/ActionCommonDetails'

import CommonActionForm from '@/components/actions/CommonActionForm.vue'
import DateTimePicker from '@/components/DateTimePicker.vue'

/**
 * A class component for a form for Generic Device Actions
 * @extends Vue
 */
@Component({
  components: {
    CommonActionForm,
    DateTimePicker
  }
})
// @ts-ignore
export default class GenericActionForm extends Vue {
  private actionCopy: GenericAction = new GenericAction()
  private datesAreValid: boolean = true
  private rules: Object = {
    startDate: this.validateInputForStartDate,
    startDateNotNull: this.mustBeProvided('Start date'),
    endDate: this.validateInputForEndDate,
    contactNotNull: this.mustBeProvided('Contact')
  }

  /**
   * a GenericAction
   */
  @Prop({
    default: () => new GenericAction(),
    required: true,
    type: Object
  })
  // @ts-ignore
  readonly value!: GenericAction

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
    type: String
  })
  // @ts-ignore
  readonly currentUserMail: string | null

  created () {
    // create a copy of the original value on which all operations will be applied
    this.createActionCopy(this.value)
  }

  /**
   * sets the start date and validates start- and enddate
   *
   * @param {DateTime | null} aDate - the start date
   */
  setStartDateAndValidate (aDate: DateTime | null) {
    this.actionCopy.beginDate = aDate
    if (this.actionCopy.endDate !== null) {
      this.checkValidationOfDates()
    }
    this.$emit('input', this.actionCopy)
  }

  /**
   * sets the end date and validates start- and enddate
   *
   * @param {DateTime | null} aDate - the end date
   */
  setEndDateAndValidate (aDate: DateTime | null) {
    this.actionCopy.endDate = aDate
    if (this.actionCopy.beginDate !== null) {
      this.checkValidationOfDates()
    }
    this.$emit('input', this.actionCopy)
  }

  updateCommonFields (action: ActionCommonDetails) {
    this.actionCopy.description = action.description
    this.actionCopy.contact = action.contact
    this.actionCopy.attachments = action.attachments.map((a: Attachment) => Attachment.createFromObject(a))
    this.$emit('input', this.actionCopy)
  }

  /**
   * validates the form based on its rules
   *
   */
  checkValidationOfDates () {
    return (this.$refs.datesForm as Vue & { validate: () => boolean }).validate()
  }

  /**
   * a rule to validate the start date
   *
   * @return {boolean | string} whether the date is valid or an error message
   */
  validateInputForStartDate (): boolean | string {
    if (!this.actionCopy.beginDate) {
      return true
    }
    if (!this.actionCopy.endDate) {
      return true
    }
    if (this.actionCopy.beginDate <= this.actionCopy.endDate) {
      return true
    }
    return 'Start date must not be after end date'
  }

  /**
   * a rule to validate the end date
   *
   * @return {boolean | string} whether the date is valid or an error message
   */
  validateInputForEndDate (): boolean | string {
    if (!this.actionCopy.endDate) {
      return true
    }
    if (!this.actionCopy.beginDate) {
      return true
    }
    if (this.actionCopy.endDate >= this.actionCopy.beginDate) {
      return true
    }
    return 'End date must not be before start date'
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

  /**
   * checks if the form is valid
   *
   */
  isValid (): boolean {
    return this.checkValidationOfDates() && (this.$refs.commonForm as Vue & { isValid: () => boolean }).isValid()
  }

  createActionCopy (action: GenericAction): void {
    this.actionCopy = GenericAction.createFromObject(action)
  }

  @Watch('value', { immediate: true, deep: true })
  // @ts-ignore
  onValueChanged (val: GenericAction) {
    this.createActionCopy(val)
  }
}
</script>
