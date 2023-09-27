<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
  <div>
    <v-form
      ref="dynamicLocationActionDateForm"
      @submit.prevent
    >
      <v-container>
        <v-row>
          <v-col>
            <v-btn
              color="primary"
              @click.stop="showDialog"
            >
              Show Available Date Ranges
            </v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" md="6">
            <DateTimePicker
              :value="value.beginDate"
              label="Select begin date"
              class="required"
              :rules="[rules.required,...beginDateExtraRules]"
              @input="update(constList.beginDate, $event)"
            />
          </v-col>
          <v-col cols="12" md="6">
            <DateTimePicker
              ref="endDatePicker"
              :value="value.endDate"
              label="Select end date"
              :rules="[...endDateExtraRules]"
              @input="update(constList.endDate, $event)"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-form>
    <AvailableDateRangeDialog
      v-model="show"
      @date-range-selected="applyDateRangesAndCloseDialog"
    />
  </div>
</template>

<script lang="ts">
import { Component, mixins, Prop, Vue } from 'nuxt-property-decorator'
import { mapGetters, mapState } from 'vuex'
import DateTimePicker from '@/components/DateTimePicker.vue'
import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Rules } from '@/mixins/Rules'
import Validator from '@/utils/validator'
import {
  ActiveDevicesWithPropertiesForDateGetter, ConfigurationsState, EarliestEndDateOfRelatedDeviceOfDynamicActionGetter,
  LocationActionTimepointsExceptPassedIdAndTypeTypeGetter,
  LocationTypes
} from '@/store/configurations'
import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'
import AvailableDateRangeDialog from '@/components/configurations/dynamicLocation/AvailableDateRangeDialog.vue'

@Component({
  components: { AvailableDateRangeDialog, ExtendedItemName, DateTimePicker },
  computed: {
    ...mapState('configurations', ['configuration']),
    ...mapGetters('configurations', ['locationActionTimepointsExceptPassedIdAndType', 'earliestEndDateOfRelatedDeviceOfDynamicAction', 'activeDevicesWithPropertiesForDate'])
  }
})
export default class DynamicLocationActionDateForm extends mixins(Rules) {
  @Prop({
    default: () => new DynamicLocationAction(),
    required: true,
    type: Object
  })
  readonly value!: DynamicLocationAction

  private constList = {
    beginDate: 'beginDate',
    endDate: 'endDate'
  }

  private show = false

  // vuex definition for typescript check
  configuration!: ConfigurationsState['configuration']
  activeDevicesWithPropertiesForDate!: ActiveDevicesWithPropertiesForDateGetter
  locationActionTimepointsExceptPassedIdAndType!: LocationActionTimepointsExceptPassedIdAndTypeTypeGetter
  earliestEndDateOfRelatedDeviceOfDynamicAction!: EarliestEndDateOfRelatedDeviceOfDynamicActionGetter

  get availableDevices () {
    return this.activeDevicesWithPropertiesForDate(this.value.beginDate, this.value.endDate)
  }

  get timepointsExceptCurrentlyEdited () {
    return this.locationActionTimepointsExceptPassedIdAndType(this.value.id, LocationTypes.dynamicStart)
  }

  get beginDateExtraRules (): any[] {
    const hasDevicesWithPropertiesForSelectedDate = () => {
      if (this.availableDevices.length <= 0) {
        return 'No devices with measured quantities for the selected date available'
      }
      return true
    }

    return [
      Validator.validateStartDateIsBeforeEndDate(this.value.beginDate, this.value.endDate),
      Validator.dateMustBeInRangeOfConfigurationDates(this.configuration, this.value.beginDate),
      hasDevicesWithPropertiesForSelectedDate,
      Validator.canNotIntersectWithExistingInterval(this.value.beginDate, this.timepointsExceptCurrentlyEdited),
      Validator.canNotStartAnActionAfterAnActiveAction(this.value.beginDate, this.timepointsExceptCurrentlyEdited)
    ]
  }

  get endDateExtraRules (): any[] {
    return [
      Validator.validateStartDateIsBeforeEndDate(this.value.beginDate, this.value.endDate),
      Validator.dateMustBeInRangeOfConfigurationDates(this.configuration, this.value.endDate),
      Validator.endDateMustBeBeforeNextAction(this.value.beginDate, this.value.endDate, this.timepointsExceptCurrentlyEdited),
      Validator.endDateMustBeBeforeEndDateOfRelatedDevice(this.value.endDate, this.earliestEndDateOfRelatedDeviceOfDynamicAction(this.value))
    ]
  }

  showDialog () {
    this.show = true
  }

  closeDialog () {
    this.show = false
  }

  applyDateRangesAndCloseDialog (action: DeviceMountAction) {
    this.presetDates(action)
    this.closeDialog()
  }

  presetDates (action: DeviceMountAction) {
    const newObj = DynamicLocationAction.createFromObject(this.value)
    newObj.beginDate = action.beginDate
    newObj.endDate = action.endDate

    if (!newObj.endDate) {
      (this.$refs.endDatePicker as Vue & { resetTextInput: () => void}).resetTextInput()
    }

    this.emit(newObj)
  }

  private emit (newObj: DynamicLocationAction) {
    this.$emit('input', newObj)
  }

  public validateForm (): boolean {
    return (this.$refs.dynamicLocationActionDateForm as Vue & { validate: () => boolean }).validate()
  }

  update (key: string, result: any) {
    const newObj = DynamicLocationAction.createFromObject(this.value)
    switch (key) {
      case this.constList.beginDate:
        newObj.beginDate = result
        break
      case this.constList.endDate:
        newObj.endDate = result
        break
    }
    this.emit(newObj)
  }
}
</script>

<style scoped>

</style>
