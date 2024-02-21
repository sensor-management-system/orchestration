<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
    <div
      v-if="value.length"
      class="mt-4"
    >
      <v-subheader>Parameter values for specific dates:</v-subheader>
      <v-row
        no-gutters
        class="mx-4"
      >
        <v-col cols="12" sm="6" md="4">
          <DateTimePicker
            v-model="date"
            label="Select a date"
          />
        </v-col>
      </v-row>
      <v-simple-table
        v-if="parameterChangeActionsForSelectedDate.length"
        class="mx-6"
      >
        <thead>
          <tr>
            <th
              width="30%"
            >
              Parameter
            </th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="action in parameterChangeActionsForSelectedDate"
            :key="`parameter-change-action-${action.id}`"
          >
            <td>
              {{ action.parameter.label }} <span v-if="action.parameter.unitName" class="text--secondary">({{ action.parameter.unitName }})</span>
            </td>
            <td
              class="py-2"
            >
              <ExpandableText v-model="action.value" :shorten-at="120" />
            </td>
          </tr>
        </tbody>
      </v-simple-table>
      <div
        v-else
        class="mx-4 text-caption text--secondary"
      >
        There are currently no parameter values for the selected date.
      </div>
    </div>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component for a Parameter Change Action form
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { DateTime } from 'luxon'

import { ParameterChangeAction } from '@/models/ParameterChangeAction'
import { currentAsUtcDateSecondsAsZeros } from '@/utils/dateHelper'

import DateTimePicker from '@/components/DateTimePicker.vue'
import ExpandableText from '@/components/shared/ExpandableText.vue'

/**
 * A class component for a list of parameter change actions
 * @extends Vue
 */
@Component({
  components: {
    DateTimePicker,
    ExpandableText
  }
})
export default class ParameterValueTable extends Vue {
  private date: DateTime = currentAsUtcDateSecondsAsZeros()

  /**
   * a list of ParameterChangeAction
   */
  @Prop({
    required: true,
    type: Array
  })
  readonly value!: ParameterChangeAction[]

  get parameterChangeActionsForSelectedDate (): ParameterChangeAction[] {
    return this.value.filter((action) => {
      if (!action.date) {
        return false
      }
      if (!action.parameter) {
        return false
      }
      // date of action is in the future
      if (action.date > this.date) {
        return false
      }
      const otherActionsOfParam = this.value.filter(someAction => someAction.id !== action.id && someAction.parameter?.id === action.parameter!.id)
      // there are no other actions
      if (!otherActionsOfParam.length) {
        return true
      }
      // look if there are more recent actions
      const moreRecentActions = otherActionsOfParam.filter(someAction => someAction.date && someAction.date > action.date! && someAction.date <= this.date)
      if (moreRecentActions.length) {
        return false
      }
      return true
    }).sort((a, b) => {
      if (!a.parameter || !a.parameter.id) {
        return -1
      }
      if (!b.parameter || !b.parameter.id) {
        return 1
      }

      return a.parameter.label.toLowerCase().localeCompare(b.parameter.label.toLowerCase())
    })
  }
}
</script>
