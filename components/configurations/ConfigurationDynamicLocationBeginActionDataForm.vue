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
  <div>
    <v-form ref="basicForm">
      <v-row>
        <v-col cols="12" md="6">
          <DateTimePicker
            :value="value.beginDate"
            label="Begin date"
            class="required"
            placeholder="e.g 2000-01-31 12:00"
            :rules="combine([rules.required], beginDateExtraRules)"
            @input="update('beginDate', $event)"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="4">
          <device-property-hierarchy-select
            :value="value.x"
            :devices="devices"
            device-select-label="Device that measures x"
            property-select-label="Measured quantity for x"
            @input="update('x', $event)"
          />
        </v-col>
        <v-col cols="12" md="4">
          <device-property-hierarchy-select
            :value="value.y"
            :devices="devices"
            device-select-label="Device that measures y"
            property-select-label="Measured quantity for y"
            @input="update('y', $event)"
          />
        </v-col>
        <v-col cols="12" md="4">
          <device-property-hierarchy-select
            :value="value.z"
            :devices="devices"
            device-select-label="Device that measures z"
            property-select-label="Measured quantity for z"
            @input="update('z', $event)"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="4">
          <v-select
            :value="value.epsgCode"
            class="required"
            :item-value="(x) => x.code"
            :item-text="(x) => x.text"
            :items="epsgCodes"
            label="EPSG Code"
            :rules="[rules.required]"
            @change="update('epsgCode', $event)"
          />
        </v-col>
        <v-col cols="12" md="4">
          <v-select
            :value="elevationDatum"
            class="required"
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
            class="required"
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
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, mixins } from 'nuxt-property-decorator'

import { DateTime } from 'luxon'

import DateTimePicker from '@/components/DateTimePicker.vue'
import DevicePropertyHierarchySelect from '@/components/DevicePropertyHierarchySelect.vue'

import { Rules } from '@/mixins/Rules'

import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'
import { DeviceProperty } from '@/models/DeviceProperty'
import { ElevationDatum } from '@/models/ElevationDatum'
import { EpsgCode } from '@/models/EpsgCode'
import { DynamicLocationBeginAction } from '@/models/DynamicLocationBeginAction'

import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'

@Component({
  components: {
    DateTimePicker,
    DevicePropertyHierarchySelect
  }
})
export default class ConfigurationDynamicLocationActionDataForm extends mixins(Rules) {
  private readonly labelForSelectMeButton = 'Add current user'

  @Prop({
    default: () => new DynamicLocationBeginAction(),
    required: true,
    type: DynamicLocationBeginAction
  })
  readonly value!: DynamicLocationBeginAction

  @Prop({
    default: () => [],
    required: true,
    type: Array
  })
  readonly devices!: Device[]

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
    type: Object
  })
  readonly earliestDateInclusive!: DateTime | null

  @Prop({
    required: false,
    default: null,
    type: Object
  })
  readonly latestDateInclusive!: DateTime | null

  @Prop({
    required: false,
    default: null,
    type: Object
  })
  readonly earliestDateExclusive!: DateTime | null

  @Prop({
    required: false,
    default: null,
    type: Object
  })
  readonly latestDateExclusive!: DateTime | null

  get epsgCode (): string {
    const epsgCodeIndex = this.epsgCodes.findIndex(e => e.code === this.value.epsgCode)
    if (epsgCodeIndex > -1) {
      return this.epsgCodes[epsgCodeIndex].text
    }
    return this.value.epsgCode
  }

  get elevationDatum (): string {
    const elevationDatumIndex = this.elevationData.findIndex(d => d.uri === this.value.elevationDatumUri)
    if (elevationDatumIndex > -1) {
      return this.elevationData[elevationDatumIndex].name
    }
    return this.value.elevationDatumName
  }

  update (key: string, value: any): void {
    const copy = DynamicLocationBeginAction.createFromObject(this.value)

    switch (key) {
      case 'beginDate':
        copy.beginDate = value as DateTime | null
        break
      case 'x':
        copy.x = value as DeviceProperty | null
        break
      case 'y':
        copy.y = value as DeviceProperty | null
        break
      case 'z':
        copy.z = value as DeviceProperty | null
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
    const devicesForCoordinatesAreStillMounted = () => {
      if (this.value.beginDate === null) {
        return true
      }
      // This here can happen in case that we select a date
      // get the devices for it, and then select another date
      // where the devices are still not mounted yet
      // or they are unmounted again
      // This here relies that the devices are a computed property
      // so that they update accodingly if we change the beginDate
      // Otherwise this logic may not work as expected...
      // (I expect the check just to pass, as the devices array is
      // still the one that was used to select the device properties)
      if (this.value.x !== null) {
        let deviceStillFound = false
        for (const device of this.devices) {
          for (const deviceProperty of device.properties) {
            if (this.value.x.id === deviceProperty.id) {
              deviceStillFound = true
            }
          }
        }
        if (!deviceStillFound) {
          return 'Device for x is not mounted on the selected date'
        }
      }
      if (this.value.y !== null) {
        let deviceStillFound = false
        for (const device of this.devices) {
          for (const deviceProperty of device.properties) {
            if (this.value.y.id === deviceProperty.id) {
              deviceStillFound = true
            }
          }
        }
        if (!deviceStillFound) {
          return 'Device for y is not mounted on the selected date'
        }
      }
      if (this.value.z !== null) {
        let deviceStillFound = false
        for (const device of this.devices) {
          for (const deviceProperty of device.properties) {
            if (this.value.z.id === deviceProperty.id) {
              deviceStillFound = true
            }
          }
        }
        if (!deviceStillFound) {
          return 'Device for z is not mounted on the selected date'
        }
      }

      return true
    }
    return [
      isLaterThanEarliestDate,
      isEarlierThenLatestDate,
      isLaterOrEqualThanEarliestDate,
      isEarlierOrEqualThenLatestDate,
      devicesForCoordinatesAreStillMounted
    ]
  }

  combine (a: any[], b: any[]): any[] {
    const result: any[] = []
    a.forEach(x => result.push(x))
    b.forEach(x => result.push(x))
    return result
  }
}

</script>
<style lang="scss">
@import '@/assets/styles/_forms.scss';
</style>
