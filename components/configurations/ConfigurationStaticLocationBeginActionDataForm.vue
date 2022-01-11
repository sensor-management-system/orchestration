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
          :value="value.beginDate"
          label="Begin date"
          placeholder="e.g 2000-01-31 12:00"
          :rules="combine([rules.required], beginDateExtraRules)"
          @input="update('beginDate', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="4">
        <v-text-field
          :value="value.x"
          label="x"
          type="number"
          step="any"
          :rules="[rules.required]"
          @wheel.prevent
          @change="update('x', $event)"
        />
      </v-col>
      <v-col cols="12" md="4">
        <v-text-field
          :value="value.y"
          label="y"
          type="number"
          step="any"
          :rules="[rules.required]"
          @wheel.prevent
          @change="update('y', $event)"
        />
      </v-col>
      <v-col cols="12" md="4">
        <v-select
          :value="value.epsgCode"
          :item-value="(x) => x.code"
          :item-text="(x) => x.text"
          :items="epsgCodes"
          label="EPSG Code"
          :rules="[rules.required]"
          @change="update('epsgCode', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="4" offset-md="4">
        <v-text-field
          :value="value.z"
          label="z"
          type="number"
          step="any"
          @wheel.prevent
          @change="update('z', $event)"
        />
      </v-col>
      <v-col cols="12" md="4">
        <v-select
          :value="elevationDatum"
          :item-value="(x) => x.name"
          :item-text="(x) => x.name"
          :items="elevationData"
          label="Elevation Datum"
          :rules="[rules.required]"
          @change="update('elevationDatum', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-alert
          dense
          type="info"
        >
          You can select a point on the map to set the coordinates.
        </v-alert>
        <location-map
          :value="location"
          @input="update('location', $event)"
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
import LocationMap from '@/components/configurations/LocationMap.vue'

import { Rules } from '@/mixins/Rules'

import { Contact } from '@/models/Contact'
import { ElevationDatum } from '@/models/ElevationDatum'
import { EpsgCode } from '@/models/EpsgCode'
import { StaticLocationBeginAction } from '@/models/StaticLocationBeginAction'
import { StationaryLocation } from '@/models/Location'

import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'
import {
  extractStationaryLocationFromStaticLocationBeginAction,
  setCoordinatesInStaticLocationBeginActionFromStationaryLocation
} from '@/utils/locationHelper'

@Component({
  components: {
    DateTimePicker,
    LocationMap
  }
})
export default class ConfigurationStaticLocationBeginActionDataForm extends mixins(Rules) {
  private readonly labelForSelectMeButton = 'Add current user'
  @Prop({
    default: () => new StaticLocationBeginAction(),
    required: true,
    type: StaticLocationBeginAction
  })
  readonly value!: StaticLocationBeginAction

  @Prop({
    default: () => [],
    required: true,
    type: Array
  })
  readonly epsgCodes!: EpsgCode[]

  @Prop({
    default: () => [],
    required: true,
    type: Array
  })
  readonly elevationData!: ElevationDatum[]

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

  get elevationDatum (): string {
    const elevationDatumIndex = this.elevationData.findIndex(d => d.uri === this.value.elevationDatumUri)
    if (elevationDatumIndex > -1) {
      return this.elevationData[elevationDatumIndex].name
    }
    return this.value.elevationDatumName
  }

  get location (): StationaryLocation {
    return extractStationaryLocationFromStaticLocationBeginAction(this.value)
  }

  update (key: string, value: any) : void {
    const copy = StaticLocationBeginAction.createFromObject(this.value)

    switch (key) {
      case 'beginDate':
        copy.beginDate = value as DateTime | null
        break
      case 'x':
        copy.x = value as number | null
        break
      case 'y':
        copy.y = value as number | null
        break
      case 'z':
        copy.z = value as number | null
        break
      case 'location':
        (() => {
          const newLocation = value as StationaryLocation
          setCoordinatesInStaticLocationBeginActionFromStationaryLocation(copy, newLocation)
        })()
        break
      case 'epsgCode':
        copy.epsgCode = value as string
        break
      case 'elevationDatum':
        (() => {
          const elevationDatumIndex = this.elevationData.findIndex(d => d.name === value)
          if (elevationDatumIndex > -1) {
            copy.elevationDatumUri = this.elevationData[elevationDatumIndex].uri
          }
          copy.elevationDatumName = value as string
        })()
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

  get beginDateExtraRules (): any[] {
    const isLaterThanEarliestDate = () => {
      if (this.value.beginDate === null || this.earliestDateExclusive === null) {
        return true
      }
      if (this.value.beginDate <= this.earliestDateExclusive) {
        return 'Must be after ' + dateToDateTimeStringHHMM(this.earliestDateExclusive)
      }
      return true
    }
    const isEarlierThenLatestDate = () => {
      if (this.value.beginDate === null || this.latestDateExclusive === null) {
        return true
      }
      if (this.value.beginDate >= this.latestDateExclusive) {
        return 'Must be before ' + dateToDateTimeStringHHMM(this.latestDateExclusive)
      }
      return true
    }
    const isLaterOrEqualThanEarliestDate = () => {
      if (this.value.beginDate === null || this.earliestDateInclusive === null) {
        return true
      }
      if (this.value.beginDate < this.earliestDateInclusive) {
        return 'Must be after or equal to ' + dateToDateTimeStringHHMM(this.earliestDateInclusive)
      }
      return true
    }
    const isEarlierOrEqualThenLatestDate = () => {
      if (this.value.beginDate === null || this.latestDateInclusive === null) {
        return true
      }
      if (this.value.beginDate > this.latestDateInclusive) {
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
