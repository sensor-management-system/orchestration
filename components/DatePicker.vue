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
    <v-menu
      v-if="!readonly"
      v-model="dateMenu"
      :close-on-content-click="false"
      :nudge-right="40"
      transition="scale-transition"
      offset-y
      min-width="290px"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-text-field
          :value="getDate()"
          :rules="rules"
          v-bind="attrs"
          :label="label"
          clearable
          prepend-icon="mdi-calendar-range"
          readonly
          v-on="on"
          @click:clear="setDate(null)"
        />
      </template>
      <v-date-picker
        :value="getDate()"
        first-day-of-week="1"
        :show-week="true"
        @input="setDate"
      />
    </v-menu>
    <v-text-field
      v-else
      :value="getDate()"
      :label="label"
      prepend-icon="mdi-calendar-range"
      readonly
      disabled
    />
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component to pick dates from an calendar
 * @author <marc.hanisch@gfz-potsdam.de>
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { DateTime } from 'luxon'
import { dateToString, stringToDate } from '@/utils/dateHelper'

/**
 * A class component to pick dates from an calendar
 * wraps a v-date-picker
 * @extends Vue
 */
@Component
// @ts-ignore
export default class DatePicker extends Vue {
  private dateMenu: boolean = false

  /**
   * a date
   */
  @Prop({
    default: null,
    type: Object
  })
  // @ts-ignore
  readonly value!: DateTime | null

  /**
   * the label of the component
   */
  @Prop({
    required: true,
    type: String
  })
  // @ts-ignore
  readonly label!: string

  /**
   * a rules array
   */
  @Prop({
    default: () => [],
    type: Array
  })
  // @ts-ignore
  readonly rules!: []

  /**
   * whether the component is in readonly mode or not
   */
  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

  /**
   * returns the date as a string representation
   *
   * @return {string} a date as an ISO string
   */
  getDate (): string {
    return dateToString(this.value)
  }

  /**
   * triggers an input event when a date was selected or cleared
   *
   * @param {string | null} aDate - the selected date from the v-date-picker component
   * @fires DatePicker#input
   */
  setDate (aDate: string | null) {
    this.dateMenu = false
    /**
     * fires an input event
     * @event DatePicker#input
     * @type {DateTime}
     */
    this.$emit('input', aDate !== null ? stringToDate(aDate) : null)
  }
}
</script>
