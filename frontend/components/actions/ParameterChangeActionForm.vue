<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-form
      ref="actionForm"
      @submit.prevent
    >
      <v-row>
        <v-col cols="12" md="6">
          <DateTimePicker
            :value="actionCopy.date"
            label="Date"
            placeholder="e.g 2000-01-31 12:00"
            :required="true"
            :rules="[rules.dateNotNull]"
            @input="setDate"
          />
        </v-col>
        <v-col cols="12" md="6">
          <v-select
            :value="actionCopy.parameter"
            class="required"
            clearable
            required
            label="Parameter"
            :items="parameters"
            :item-text="(parameter) => parameter.label + (parameter.unitName ? ' (' + parameter.unitName + ')' : '')"
            :item-value="(parameter) => parameter"
            :rules="[rules.parameterNotEmpty]"
            @input="setParameter"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="12">
          <v-textarea
            :value="actionCopy.value"
            label="Value"
            rows="3"
            @input="setValue"
          />
        </v-col>
      </v-row>
    </v-form>
    <CommonActionForm
      ref="commonForm"
      hide-attachments
      :value="actionCopy"
      :rules="[rules.contactNotNull]"
      :current-user-mail="currentUserMail"
      @input="updateCommonFields"
    />
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component for a Parameter Change Action form
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Component, Prop, Vue, Watch } from 'nuxt-property-decorator'

import { DateTime } from 'luxon'

import { ActionCommonDetails } from '@/models/ActionCommonDetails'
import { Parameter } from '@/models/Parameter'
import { ParameterChangeAction } from '@/models/ParameterChangeAction'

import CommonActionForm from '@/components/actions/CommonActionForm.vue'
import DateTimePicker from '@/components/DateTimePicker.vue'

/**
 * A class component for a form for Device calibration actions
 * @extends Vue
 */
@Component({
  components: {
    CommonActionForm,
    DateTimePicker
  }
})
export default class ParameterChangeActionForm extends Vue {
  private actionCopy: ParameterChangeAction = new ParameterChangeAction()
  private rules: Object = {
    dateNotNull: this.mustBeProvided('Date'),
    contactNotNull: this.mustBeProvided('Contact'),
    parameterNotEmpty: this.parameterNotEmpty
  }

  /**
   * a ParameterChangeAction
   */
  @Prop({
    default: () => new ParameterChangeAction(),
    required: true,
    type: Object
  })
  readonly value!: ParameterChangeAction

  @Prop({
    default: () => [],
    required: true,
    type: Array
  })
  readonly parameters!: Parameter[]

  @Prop({
    default: null,
    type: String,
    required: false
  })
  readonly currentUserMail!: string | null

  created () {
    this.createActionCopy(this.value)
  }

  setDate (aDate: DateTime | null) {
    this.actionCopy.date = aDate
    this.$emit('input', this.actionCopy)
  }

  setValue (value: string | null | undefined) {
    if (value === null || typeof value === 'undefined') {
      this.actionCopy.value = ''
    } else {
      this.actionCopy.value = value
    }
    this.$emit('input', this.actionCopy)
  }

  setParameter (parameter: Parameter) {
    this.actionCopy.parameter = parameter ? Parameter.createFromObject(parameter) : null
    this.$emit('input', this.actionCopy)
  }

  updateCommonFields (action: ActionCommonDetails) {
    this.actionCopy.description = action.description
    this.actionCopy.contact = action.contact
    this.$emit('input', this.actionCopy)
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

  parameterNotEmpty (parameter: Parameter | null): boolean | string {
    if (parameter) {
      return true
    }
    return 'Parameter must be selected'
  }

  checkValidationOfCommonForm () {
    return (this.$refs.commonForm as Vue & { isValid: () => boolean }).isValid()
  }

  isValid (): boolean {
    const checkActionForm = (this.$refs.actionForm as Vue & { validate: () => boolean }).validate()
    const checkCommonForm = this.checkValidationOfCommonForm()
    return checkActionForm && checkCommonForm
  }

  createActionCopy (action: ParameterChangeAction): void {
    this.actionCopy = ParameterChangeAction.createFromObject(action)
  }

  @Watch('value', { immediate: true, deep: true })
  onValueChanged (val: ParameterChangeAction) {
    if (val) {
      this.createActionCopy(val)
    }
  }
}
</script>
