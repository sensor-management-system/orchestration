<!--
SPDX-FileCopyrightText: 2020 - 2022
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
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
          v-model="valueCopy.beginDate"
          placeholder="e.g. 2000-01-31 12:00"
          label="Select mount date"
          hint="Mount date"
          required
          class="required"
          :rules="[rules.required, additionalRules.validateMountingDates, ...beginDateRules]"
          @input="dateChanged"
        />
      </v-col>
      <v-col cols="6">
        <DateTimePicker
          v-model="valueCopy.endDate"
          placeholder="Open End"
          label="Select unmount date"
          :hint="!endRequired ? 'Optional. Leave blank for open end' : ''"
          :required="endRequired"
          :rules="[additionalRules.validateMountingDates, ...endDateRules]"
          :class="{'required' : endRequired}"
          @input="dateChanged"
        />
      </v-col>
    </v-row>
  </v-form>
</template>

<script lang="ts">
import { Component, mixins, Prop, Watch } from 'nuxt-property-decorator'

import { DateTime } from 'luxon'

import { MountActionDateDTO } from '@/utils/configurationInterfaces'

import Validator from '@/utils/validator'

import DateTimePicker from '@/components/DateTimePicker.vue'

import { Rules } from '@/mixins/Rules'

@Component({
  components: {
    DateTimePicker
  }
})
export default class MountActionDateForm extends mixins(Rules) {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: MountActionDateDTO

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

  private valueCopy: MountActionDateDTO | null = null
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

  dateChanged () {
    this.$emit('input', this.valueCopy)
  }

  @Watch('value', {
    immediate: true,
    deep: true
  })
  onValueChange (value: MountActionDateDTO) {
    if (value) {
      this.valueCopy = value
    }
  }
}
</script>

<style scoped>
</style>
