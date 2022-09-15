<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
  <v-form
    v-if="valueCopy"
    ref="dateForm"
    v-model="formIsValid"
    @submit.prevent
  >
    <v-row justify="start" class="mb-6">
      <v-col cols="6" md="6">
        <DateTimePicker
          :value="valueCopy.beginDate"
          placeholder="e.g. 2000-01-31 12:00"
          label="Select begin date"
          hint="Start date"
          required
          class="required"
          :rules="[rules.required, additionalRules.validateMountingDates, ...beginDateRules]"
          @input="dateChanged('beginDate', $event)"
        />
      </v-col>
      <v-col cols="6">
        <DateTimePicker
          :value="valueCopy.endDate"
          placeholder="Open End"
          label="Select end date"
          :hint="!endRequired ? 'Optional. Leave blank for open end' : ''"
          :required="endRequired"
          :rules="[additionalRules.validateMountingDates, ...endDateRules]"
          :class="{'required' : endRequired}"
          @input="dateChanged('endDate', $event)"
        />
      </v-col>
    </v-row>
  </v-form>
</template>

<script lang="ts">
import { Component, mixins, Prop, Watch } from 'nuxt-property-decorator'

import { DateTime } from 'luxon'

import { IMountAction, MountAction } from '@/models/MountAction'

import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'
import Validator from '@/utils/validator'

import DateTimePicker from '@/components/DateTimePicker.vue'

import { Rules } from '@/mixins/Rules'

@Component({
  components: {
    DateTimePicker
  },
  filters: { dateToDateTimeStringHHMM }
})
export default class MountActionDateForm extends mixins(Rules) {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: MountAction

  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  readonly beginDateRules!: ((value: DateTime | null) => string | boolean)[]

  @Prop({
    default: () => [],
    required: false,
    type: Array
  })
  readonly endDateRules!: ((value: DateTime | null) => string | boolean)[]

  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  readonly endRequired!: boolean

  private valueCopy: IMountAction | null = null
  private formIsValid: boolean = true

  get additionalRules (): Object {
    return {
      validateMountingDates: this.validateMountingDates.bind(this)
    }
  }

  validateMountingDates (): string | boolean {
    if (this.valueCopy) {
      return Validator.validateMountingDates(this.valueCopy.beginDate, this.valueCopy.endDate)
    }
    return true
  }

  validateForm (): boolean {
    if (this.$refs.dateForm) {
      return (this.$refs.dateForm as Vue & { validate: () => boolean }).validate()
    } else {
      return true
    }
  }

  resetValidation (): void {
    if (this.$refs.dateForm) {
      (this.$refs.dateForm as Vue & { resetValidation: () => void }).resetValidation()
    }
  }

  dateChanged (target: keyof Pick<MountAction, 'beginDate' | 'endDate'>, value: null | DateTime) {
    if (this.valueCopy) {
      switch (target) {
        case 'beginDate':
          if (value) {
            this.valueCopy.beginDate = value
          }
          break
        case 'endDate':
          this.valueCopy.endDate = value
          break
      }
      this.$emit('input', this.valueCopy)
    }
  }

  @Watch('value', {
    immediate: true,
    deep: true
  })
  onValueChange (value: IMountAction) {
    if (value) {
      this.valueCopy = MountAction.createFromObject(value)
    }
  }
}
</script>

<style scoped>
</style>
