<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
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
  <v-form
    ref="basicForm"
    @submit.prevent
  >
    <v-row>
      <v-col cols="12" md="6">
        <DateTimePicker
          :value="value.endDate"
          label="End date"
          placeholder="e.g 2000-01-31 12:00"
          :rules="combine([rules.required], endDateExtraRules)"
          @input="update('endDate', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="12">
        <v-textarea
          :value="value.description"
          label="Description"
          rows="3"
          @input="update('description', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-autocomplete
          :value="value.contact"
          :items="contacts"
          label="Contact"
          clearable
          required
          :item-text="(x) => x.toString()"
          :item-value="(x) => x"
          :rules="[rules.required]"
          @change="update('contact', $event)"
        />
      </v-col>
      <v-col v-if="currentUserMail" cols="12" md="1" align-self="center">
        <v-btn small @click="selectCurrentUserAsContact">
          {{ labelForSelectMeButton }}
        </v-btn>
      </v-col>
    </v-row>
  </v-form>
</template>

<script lang="ts">
import { Component, Vue, Prop, mixins } from 'nuxt-property-decorator'

import { DateTime } from 'luxon'

import DateTimePicker from '@/components/DateTimePicker.vue'

import { Rules } from '@/mixins/Rules'

import { Contact } from '@/models/Contact'
import { DynamicLocationEndAction } from '@/models/DynamicLocationEndAction'

import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'

@Component({
  components: {
    DateTimePicker
  }
})
export default class ConfigurationDynamicLocationEndActionDataForm extends mixins(Rules) {
  private readonly labelForSelectMeButton = 'Add current user'
  @Prop({
    default: () => new DynamicLocationEndAction(),
    required: true,
    type: DynamicLocationEndAction
  })
  readonly value!: DynamicLocationEndAction

  @Prop({
    default: () => [],
    required: true,
    type: Array
  })
  readonly contacts!: Contact[]

  @Prop({
    required: false,
    type: String
  })
  readonly currentUserMail!: string | null

  @Prop({
    required: false,
    default: null,
    type: DateTime
  })
  readonly earliestDateInclusive!: DateTime | null

  @Prop({
    required: false,
    default: null,
    type: DateTime
  })
  readonly latestDateInclusive!: DateTime | null

  @Prop({
    required: false,
    default: null,
    type: DateTime
  })
  readonly earliestDateExclusive!: DateTime | null

  @Prop({
    required: false,
    default: null,
    type: DateTime
  })
  readonly latestDateExclusive!: DateTime | null

  update (key: string, value: any) : void {
    const copy = DynamicLocationEndAction.createFromObject(this.value)

    switch (key) {
      case 'endDate':
        copy.endDate = value as DateTime | null
        break
      case 'description':
        copy.description = value as string
        break
      case 'contact':
        copy.contact = value as Contact | null
        break
    }
    this.$emit('input', copy)
  }

  public isValid (): boolean {
    return (this.$refs.basicForm as Vue & { validate: () => boolean }).validate()
  }

  selectCurrentUserAsContact () {
    if (this.currentUserMail) {
      const userIndex = this.contacts.findIndex(c => c.email === this.currentUserMail)
      if (userIndex > -1) {
        this.update('contact', this.contacts[userIndex])
        return
      }
    }
    this.$store.commit('snackbar/setError', 'No contact found with your data')
  }

  get endDateExtraRules (): any[] {
    const isLaterThanEarliestDate = () => {
      if (this.value.endDate === null || this.earliestDateExclusive === null) {
        return true
      }
      if (this.value.endDate <= this.earliestDateExclusive) {
        return 'Must be after ' + dateToDateTimeStringHHMM(this.earliestDateExclusive)
      }
      return true
    }
    const isEarlierThenLatestDate = () => {
      if (this.value.endDate === null || this.latestDateExclusive === null) {
        return true
      }
      if (this.value.endDate >= this.latestDateExclusive) {
        return 'Must be before ' + dateToDateTimeStringHHMM(this.latestDateExclusive)
      }
      return true
    }
    const isLaterOrEqualThanEarliestDate = () => {
      if (this.value.endDate === null || this.earliestDateInclusive === null) {
        return true
      }
      if (this.value.endDate < this.earliestDateInclusive) {
        return 'Must be after or equal to ' + dateToDateTimeStringHHMM(this.earliestDateInclusive)
      }
      return true
    }
    const isEarlierOrEqualThenLatestDate = () => {
      if (this.value.endDate === null || this.latestDateInclusive === null) {
        return true
      }
      if (this.value.endDate > this.latestDateInclusive) {
        return 'Must be before ' + dateToDateTimeStringHHMM(this.latestDateInclusive)
      }
      return true
    }
    return [
      isLaterThanEarliestDate,
      isEarlierThenLatestDate,
      isLaterOrEqualThanEarliestDate,
      isEarlierOrEqualThenLatestDate
    ]
  }

  combine (a: any[], b: any[]) : any[] {
    const result: any[] = []
    a.forEach(x => result.push(x))
    b.forEach(x => result.push(x))
    return result
  }
}

</script>
