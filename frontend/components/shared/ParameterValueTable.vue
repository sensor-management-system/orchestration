<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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
