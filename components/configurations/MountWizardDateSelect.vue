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
  <v-row justify="start" class="mb-6">
    <v-col cols="6" md="6">
      <DateTimePicker
        :value="syncedSelectedDate"
        placeholder="e.g. 2000-01-31 12:00"
        label="Select begin date"
        hint="Start date"
        @input="setStartDate"
      />
    </v-col>
    <v-col cols="6">
      <v-form ref="form">
        <DateTimePicker
          :value="syncedSelectedEndDate"
          placeholder="Open End"
          label="Select end date"
          hint="Optional. Leave blank for open end"
          :rules="[rules.validateMountingDates, rules.validateMountingTimeRange]"
          @input="setEndDate"
        />
      </v-form>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Component, Vue, Prop, PropSync } from 'nuxt-property-decorator'

import { DateTime } from 'luxon'

import DateTimePicker from '@/components/DateTimePicker.vue'

import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'
import Validator from '@/utils/validator'

@Component({
  components: {
    DateTimePicker
  },
  filters: { dateToDateTimeStringHHMM }
})
export default class MountWizardDateSelect extends Vue {
  @PropSync('selectedDate', {
    required: true,
    type: Object
  })
    syncedSelectedDate!: DateTime

  @PropSync('selectedEndDate', {
    required: false,
    type: Object
  })
    syncedSelectedEndDate!: DateTime | null

  @Prop({
    required: false,
    type: Object
  }) readonly selectedNodeEndDate!: DateTime | null

  get rules (): Object {
    return {
      validateMountingDates: Validator.validateMountingDates(this.syncedSelectedDate, this.syncedSelectedEndDate),
      validateMountingTimeRange: Validator.validateMountingTimeRange(this.syncedSelectedEndDate, this.selectedNodeEndDate)
    }
  }

  setStartDate (aDate: DateTime) {
    this.syncedSelectedDate = aDate
  }

  setEndDate (aDate: DateTime | null) {
    this.syncedSelectedEndDate = aDate
  }

  // TODO: this method should trigger a form validation but needs to be called from MountWizardNodeSelect
  // async checkEndDateOfDatePicker () {
  //   await this.$nextTick()
  //   return (this.$refs.form as Vue & { validate: () => boolean }).validate()
  // }
}
</script>

<style scoped>
</style>
