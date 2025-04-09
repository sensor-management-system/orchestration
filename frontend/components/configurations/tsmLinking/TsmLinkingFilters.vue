<!--
 SPDX-FileCopyrightText: 2020 - 2025

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <v-container>
    <v-row>
      <v-col>
        <SimpleAutoComplete
          v-model="selectedDevices"
          :items="devicesInLinkings"
          label="Device filter"
          hint="Please select a device"
          :item-text="deviceSelectionText"
        >
          <template #item="{ item }">
            <DeviceShortNameSerialNumber :value="item" />
          </template>
        </SimpleAutoComplete>
      </v-col>
      <v-col>
        <SimpleAutoComplete
          v-model="selectedMeasuredQuantities"
          :items="measuredQuantitiesInLinkings"
          label="Measured quantity filter"
          hint="Please select a measured quantity"
          :item-text="(x) => x.propertyName"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-row>
          <v-col>
            <h4>Start Date Filter</h4>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="4">
            <date-time-picker
              ref="startDateRef"
              v-model="selectedStartDate"
              label="Select a date"
              use-date
            />
          </v-col>
          <v-col cols="2">
            <v-select
              v-model="selectedStartDateOption"
              label="Operation"
              :items="dateFilterOption"
              item-text="text"
              return-object
              clearable
            />
          </v-col>
          <v-col align-self="center">
            <v-btn
              small
              :disabled="startDateFilter === null"
              @click="clearStartDateFilter"
            >
              clear
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-row />
    <v-row>
      <v-col>
        <v-row>
          <v-col>
            <h4>End Date Filter</h4>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="4">
            <date-time-picker
              ref="endDateRef"
              v-model="selectedEndDate"
              label="Select a date"
              use-date
            />
          </v-col>
          <v-col cols="2">
            <v-select
              v-model="selectedEndDateOption"
              label="Operation"
              :items="dateFilterOption"
              item-text="text"
              return-object
              clearable
            />
          </v-col>
          <v-col align-self="center">
            <v-btn
              small
              :disabled="endDateFilter === null"
              @click="clearEndDateFilter"
            >
              clear
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-btn @click="clearFilter">
          Clear Filters
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapGetters, mapState } from 'vuex'
import { DateTime } from 'luxon'
import DateTimePicker from '@/components/DateTimePicker.vue'
import { Device } from '@/models/Device'
import { DeviceProperty } from '@/models/DeviceProperty'
import {
  DateFilterGetter,
  DevicesInLinkingsGetter,
  ITsmLinkingState,
  MeasuredQuantitiesInLinkingsGetter, TSMLinkingDateFilterOperation, TsmLinkingDateFilterOption
} from '@/store/tsmLinking'
import DeviceShortNameSerialNumber from '@/components/devices/DeviceShortNameSerialNumber.vue'
import TsmLinkingDeviceSelect from '@/components/configurations/tsmLinking/TsmLinkingDeviceSelect.vue'
import SimpleAutoComplete from '@/components/shared/SimpleAutoComplete.vue'

@Component({
  components: { SimpleAutoComplete, TsmLinkingDeviceSelect, DeviceShortNameSerialNumber, DateTimePicker },
  computed: {
    ...mapGetters('tsmLinking',
      [
        'devicesInLinkings',
        'measuredQuantitiesInLinkings',
        'startDateFilter',
        'endDateFilter'
      ]),
    ...mapState('tsmLinking', [
      'filterSelectedDevices',
      'filterSelectedMeasuredQuantities',
      'filterSelectedStartDate',
      'filterSelectedEndDate',
      'filterSelectedStartDateOperation',
      'filterSelectedEndDateOperation',
      'linkings'
    ])
  }
})
export default class TsmLinkingFilters extends Vue {
  dateFilterOption: TsmLinkingDateFilterOption[] = [
    {
      text: 'later than or equals',
      id: TSMLinkingDateFilterOperation.GTE
    },
    {
      text: 'earlier than or equals',
      id: TSMLinkingDateFilterOperation.LTE
    }
  ]

  // vuex type definitions
  devicesInLinkings!: DevicesInLinkingsGetter
  measuredQuantitiesInLinkings!: MeasuredQuantitiesInLinkingsGetter
  filterSelectedDevices!: ITsmLinkingState['filterSelectedDevices']
  filterSelectedMeasuredQuantities!: ITsmLinkingState['filterSelectedMeasuredQuantities']
  filterSelectedStartDate!: ITsmLinkingState['filterSelectedStartDate']
  filterSelectedEndDate!: ITsmLinkingState['filterSelectedEndDate']
  filterSelectedStartDateOperation!: ITsmLinkingState['filterSelectedStartDateOperation']
  filterSelectedEndDateOperation!: ITsmLinkingState['filterSelectedEndDateOperation']
  startDateFilter!: DateFilterGetter
  endDateFilter!: DateFilterGetter

  get selectedDevices (): Device[] {
    return this.filterSelectedDevices
  }

  set selectedDevices (selected: Device[]) {
    this.$store.commit('tsmLinking/setFilterSelectedDevices', selected)
  }

  get selectedMeasuredQuantities (): DeviceProperty[] {
    return this.filterSelectedMeasuredQuantities
  }

  set selectedMeasuredQuantities (selected: DeviceProperty[]) {
    this.$store.commit('tsmLinking/setFilterSelectedMeasuredQuantities', selected)
  }

  get selectedStartDate (): DateTime | null {
    return this.filterSelectedStartDate
  }

  set selectedStartDate (date: DateTime | null) {
    this.$store.commit('tsmLinking/setFilterSelectedStartDate', date)
  }

  get selectedEndDate (): DateTime | null {
    return this.filterSelectedEndDate
  }

  set selectedEndDate (date: DateTime | null) {
    this.$store.commit('tsmLinking/setFilterSelectedEndDate', date)
  }

  get selectedStartDateOption (): TsmLinkingDateFilterOption | null {
    return this.filterSelectedStartDateOperation
  }

  set selectedStartDateOption (operation: TsmLinkingDateFilterOption | null) {
    this.$store.commit('tsmLinking/setFilterSelectedStartDateOperation', operation)
  }

  get selectedEndDateOption (): TsmLinkingDateFilterOption | null {
    return this.filterSelectedEndDateOperation
  }

  set selectedEndDateOption (operation: TsmLinkingDateFilterOption | null) {
    this.$store.commit('tsmLinking/setFilterSelectedEndDateOperation', operation)
  }

  clearStartDateFilter () {
    this.selectedStartDate = null
    const startDateRef = this.$refs.startDateRef as Vue & { resetTextInput: () => void }
    startDateRef.resetTextInput()
    this.selectedStartDateOption = null
  }

  clearEndDateFilter () {
    this.selectedEndDate = null
    const endDateRef = this.$refs.endDateRef as Vue & { resetTextInput: () => void }
    endDateRef.resetTextInput()
    this.selectedEndDateOption = null
  }

  public clearFilter () {
    this.clearStartDateFilter()
    this.clearEndDateFilter()
    this.selectedDevices = []
    this.selectedMeasuredQuantities = []
  }

  deviceSelectionText (item: Device) {
    if (item.serialNumber) {
      return `${item.shortName} (${item.serialNumber})`
    }
    return `${item.shortName}`
  }

  measuredQuantitySelectionText (item: DeviceProperty) {
    return item.propertyName
  }
}
</script>

<style scoped>

</style>
