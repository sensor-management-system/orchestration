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
  <v-form
    ref="basicForm"
    @submit.prevent
  >
    <v-card>
      <v-card-title>
        Begin of the dynamic location
      </v-card-title>
      <v-card-text class="text--primary">
        <v-row>
          <v-col cols="12" md="6">
            <DateTimePicker
              :value="value.beginDate"
              label="Begin date"
              class="required"
              placeholder="e.g 2000-01-31 12:00"
              :rules="[...[rules.required],...beginDateExtraRules]"
              @input="update('beginDate', $event)"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="4">
            <device-property-hierarchy-select
              :value="value.x"
              :devices="devices"
              :device-select-rules="[rules.required]"
              :property-select-rules="[rules.required]"
              class="required"
              device-select-label="Device that measures x"
              property-select-label="Measured quantity for x"
              @input="update('x', $event)"
            />
          </v-col>
          <v-col cols="12" md="4">
            <device-property-hierarchy-select
              :value="value.y"
              :devices="devices"
              :device-select-rules="[rules.required]"
              :property-select-rules="[rules.required]"
              class="required"
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
              @input="update('beginDescription', $event)"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="6">
            <v-autocomplete
              :value="value.beginContact"
              class="required"
              :items="contacts"
              label="Contact"
              clearable
              required
              :item-text="(x) => x.toString()"
              :item-value="(x) => x"
              :rules="[rules.required]"
              @change="update('beginContact', $event)"
            />
          </v-col>
          <v-col v-if="currentUserMail" cols="12" md="1" align-self="center">
            <v-btn small @click="selectCurrentUserAsContact(typeBeginContact)">
              {{ labelForSelectMeButton }}
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
      <v-divider class="mx-4 mt-4" />
      <v-card-title>
        End of the dynamic location
      </v-card-title>
      <v-card-text class="text--primary">
        <v-row>
          <v-col cols="12" md="6">
            <DateTimePicker
              :value="value.endDate"
              label="End date"
              placeholder="e.g 2000-01-31 12:00"
              :rules="endDateExtraRules"
              :hint="endDateHint"
              @input="update('endDate', $event)"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="12">
            <v-textarea
              :value="value.endDescription"
              label="Description"
              rows="3"
              @input="update('endDescription', $event)"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="6">
            <v-autocomplete
              :value="value.endContact"
              :items="contacts"
              label="Contact"
              clearable
              required
              :item-text="(x) => x.toString()"
              :item-value="(x) => x"
              @change="update('endContact', $event)"
            />
          </v-col>
          <v-col v-if="currentUserMail" cols="12" md="1" align-self="center">
            <v-btn small @click="selectCurrentUserAsContact(typeEndContact)">
              {{ labelForSelectMeButton }}
            </v-btn>
          </v-col>
        </v-row>
      </v-card-text>
      <slot name="actions" />
    </v-card>
  </v-form>
</template>

<script lang="ts">
import { Component, mixins, Prop, Vue } from 'nuxt-property-decorator'
import { DateTime } from 'luxon'
import { mapGetters, mapState } from 'vuex'
import { VocabularyState } from '@/store/vocabulary'
import { ContactsState } from '@/store/contacts'
import {
  ConfigurationsState,
  EarliestEndDateOfRelatedDeviceOfDynamicActionGetter,
  LocationActionTimepointsExceptPassedIdAndTypeTypeGetter,
  LocationTypes
} from '@/store/configurations'
import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import { Device } from '@/models/Device'
import { ElevationDatum } from '@/models/ElevationDatum'
import { DeviceProperty } from '@/models/DeviceProperty'
import { Contact } from '@/models/Contact'
import Validator from '@/utils/validator'
import { Rules } from '@/mixins/Rules'
import DateTimePicker from '@/components/DateTimePicker.vue'
import DevicePropertyHierarchySelect from '@/components/DevicePropertyHierarchySelect.vue'

import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'

@Component({
  components: { DevicePropertyHierarchySelect, DateTimePicker },
  computed: {
    ...mapState('vocabulary', ['epsgCodes', 'elevationData']),
    ...mapState('contacts', ['contacts']),
    ...mapGetters('configurations', ['locationActionTimepointsExceptPassedIdAndType', 'earliestEndDateOfRelatedDeviceOfDynamicAction']),
    ...mapState('configurations', ['configuration'])
  }
})
export default class DynamicLocationActionDataForm extends mixins(Rules) {
  private readonly labelForSelectMeButton = 'Add current user'

  @Prop({
    default: () => new DynamicLocationAction(),
    required: true,
    type: DynamicLocationAction
  })
  readonly value!: DynamicLocationAction

  @Prop({
    default: () => [],
    required: true,
    type: Array
  })
  readonly devices!: Device[]

  private readonly typeBeginContact = 'beginContact'
  private readonly typeEndContact = 'endContact'

  // vuex definition for typescript check
  epsgCodes!: VocabularyState['epsgCodes']
  elevationData!: VocabularyState['elevationData']
  contacts!: ContactsState['contacts']
  configuration!: ConfigurationsState['configuration']
  locationActionTimepointsExceptPassedIdAndType!: LocationActionTimepointsExceptPassedIdAndTypeTypeGetter
  earliestEndDateOfRelatedDeviceOfDynamicAction!: EarliestEndDateOfRelatedDeviceOfDynamicActionGetter

  get currentUserMail (): string | null {
    return this.$auth.user?.email as string | null
  }

  get epsgCode (): string {
    const epsgCodeIndex = this.epsgCodes.findIndex(e => e.code === this.value.epsgCode)
    if (epsgCodeIndex > -1) {
      return this.epsgCodes[epsgCodeIndex].text
    }
    return this.value.epsgCode
  }

  get elevationDatum (): string {
    const elevationDatumIndex = this.elevationData.findIndex((d: ElevationDatum) => d.uri === this.value.elevationDatumUri)
    if (elevationDatumIndex > -1) {
      return this.elevationData[elevationDatumIndex].name
    }
    return this.value.elevationDatumName
  }

  get endDateHint () {
    if (this.earliestEndDateOfRelatedDeviceOfDynamicAction(this.value) !== null) {
      return `The end date can not be after "${dateToDateTimeStringHHMM(this.earliestEndDateOfRelatedDeviceOfDynamicAction(this.value))}" because of a planned unmount.`
    }
    return null
  }

  update (key: string, value: any): void {
    const copy = DynamicLocationAction.createFromObject(this.value)

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
          const elevationDatumIndex = this.elevationData.findIndex((d: ElevationDatum) => d.name === value)
          if (elevationDatumIndex > -1) {
            copy.elevationDatumUri = this.elevationData[elevationDatumIndex].uri
          }
          copy.elevationDatumName = value as string
        })()
        break
      case 'beginDescription':
        copy.beginDescription = value as string
        break
      case 'beginContact':
        copy.beginContact = value as Contact | null
        break
      case 'endDate':
        copy.endDate = value as DateTime | null
        break
      case 'endDescription':
        copy.endDescription = value as string
        break
      case 'endContact':
        copy.endContact = value as Contact | null
        break
    }
    this.$emit('input', copy)
  }

  public isValid (): boolean {
    return (this.$refs.basicForm as Vue & { validate: () => boolean }).validate()
  }

  selectCurrentUserAsContact (type: string) {
    if (this.currentUserMail) {
      const foundUser = this.contacts.find((c: Contact) => c.email === this.currentUserMail)
      if (foundUser) {
        this.update(type, foundUser)
        return
      }
    }
    this.$store.commit('snackbar/setError', 'No contact found with your data')
  }

  get timepointsExceptCurrentlyEdited () {
    return this.locationActionTimepointsExceptPassedIdAndType(this.value.id, LocationTypes.dynamicStart)
  }

  get beginDateExtraRules (): any[] {
    const hasDevicesWithPropertiesForSelectedDate = () => {
      if (this.devices.length <= 0) {
        return 'No devices with measured quantities for the selected date'
      }
      return true
    }
    return [
      Validator.canNotIntersectWithExistingInterval(this.value.beginDate, this.timepointsExceptCurrentlyEdited),
      Validator.startDateMustBeAfterPreviousAction(this.value.beginDate, this.value.endDate, this.timepointsExceptCurrentlyEdited),
      Validator.validateStartDateIsBeforeEndDate(this.value.beginDate, this.value.endDate),
      Validator.canNotStartAnActionAfterAnActiveAction(this.value.beginDate, this.timepointsExceptCurrentlyEdited),
      hasDevicesWithPropertiesForSelectedDate,
      Validator.dateMustBeInRangeOfConfigurationDates(this.configuration, this.value.beginDate)

    ]
  }

  get endDateExtraRules (): any[] {
    return [
      Validator.canNotIntersectWithExistingInterval(this.value.endDate, this.timepointsExceptCurrentlyEdited),
      Validator.validateStartDateIsBeforeEndDate(this.value.beginDate, this.value.endDate),
      Validator.endDateMustBeBeforeNextAction(this.value.beginDate, this.value.endDate, this.timepointsExceptCurrentlyEdited),
      Validator.endDateMustBeBeforeEndDateOfRelatedDevice(this.value.endDate, this.earliestEndDateOfRelatedDeviceOfDynamicAction(this.value)),
      Validator.dateMustBeInRangeOfConfigurationDates(this.configuration, this.value.endDate)
    ]
  }
}
</script>

<style scoped>

</style>
