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
  <div>
    <v-card-actions
      v-if="editable"
    >
      <v-spacer />
      <v-btn
        color="primary"
        :disabled="isDisabled"
        small
        nuxt
        :to="'/configurations/' + configurationId + '/locations/static-location-actions/new'"
      >
        Start Static Location
      </v-btn>
      <v-tooltip
        v-if="isDynamicStartButtonDisabled"
        bottom
      >
        <template #activator="{ on }">
          <div v-on="on">
            <v-btn
              class="extraMarginForTooltipBtn"
              color="primary"
              small
              disabled
            >
              Start Dynamic Location
              <v-icon
                right
                dark
              >
                mdi-help-circle
              </v-icon>
            </v-btn>
          </div>
        </template>
        <div>
          <div><span>The configuration has no devices with properties mounted.</span></div>
          <div>
            <span>To start a new action, you must mount devices with suitable properties.</span>
          </div>
        </div>
      </v-tooltip>
      <v-btn
        v-else-if="$auth.loggedIn"
        color="primary"
        :disabled="isDisabled"
        small
        nuxt
        :to="'/configurations/' + configurationId + '/locations/dynamic-location-actions/new'"
      >
        Start Dynamic Location
      </v-btn>
    </v-card-actions>
    <v-row>
      <v-col cols="12" md="3">
        <DateTimePicker
          v-model="selectedDate"
          :disabled="isDisabled"
          :readonly="isDisabled"
          placeholder="e.g. 2000-01-31 12:00"
          label="Configuration at date"
          @input="updateTimepointItemWhenDateSelected"
        />
      </v-col>
      <v-col>
        <v-select
          v-model="selectedTimepoint"
          :items="configurationLocationActionTimepoints"
          :disabled="isDisabled"
          item-text="text"
          clearable
          label="Dates defined by actions"
          hint="The referenced time zone is UTC."
          return-object
          persistent-hint
          @input="selectTimepoint"
        />
      </v-col>
    </v-row>
    <NuxtChild />
  </div>
</template>

<script lang="ts">
import { Component, Vue, InjectReactive } from 'nuxt-property-decorator'
import { mapActions, mapGetters, mapState } from 'vuex'

import { DateTime } from 'luxon'

import {
  ConfigurationsState,
  HasActiveDevicesWithPropertiesForDate,
  HasMountedDevicesWithPropertiesGetter,
  LocationTypes,
  SetSelectedLocationDateAction,
  SetSelectedTimepointItemAction
} from '@/store/configurations'

import { currentAsUtcDateSecondsAsZeros } from '@/utils/dateHelper'

import DateTimePicker from '@/components/DateTimePicker.vue'
import { ILocationTimepoint } from '@/serializers/controller/LocationActionTimepointSerializer'
import { isTimePointForDynamicAction, isTimePointForStaticAction } from '@/utils/locationHelper'

@Component({
  components: {
    DateTimePicker
  },
  computed: {
    ...mapState('configurations',
      ['configurationLocationActionTimepoints',
        'selectedTimepointItem',
        'selectedLocationDate']),
    ...mapGetters('configurations', [
      'hasMountedDevicesWithProperties',
      'hasActiveDevicesWithPropertiesForDate'
    ])
  },
  methods: {
    ...mapActions('configurations', ['setSelectedTimepointItem', 'setSelectedLocationDate'])
  }
})
export default class ConfigurationShowLocationPage extends Vue {
  @InjectReactive()
    editable!: boolean

  // vuex definition for typescript check
  private configurationLocationActionTimepoints!: ConfigurationsState['configurationLocationActionTimepoints']
  private selectedTimepointItem!: ConfigurationsState['selectedTimepointItem']
  private selectedLocationDate!: ConfigurationsState['selectedLocationDate']
  private setSelectedTimepointItem!: SetSelectedTimepointItemAction
  private setSelectedLocationDate!: SetSelectedLocationDateAction
  private hasDeviceMountActionsForDynamicLocation!: () => boolean
  private hasMountedDevicesWithProperties!: HasMountedDevicesWithPropertiesGetter
  private hasActiveDevicesWithPropertiesForDate!: HasActiveDevicesWithPropertiesForDate

  created () {
    if (this.selectedTimepoint) {
      this.selectTimepoint()
    } else {
      this.selectedDate = currentAsUtcDateSecondsAsZeros()
    }
  }

  get selectedTimepoint () {
    return this.selectedTimepointItem
  }

  set selectedTimepoint (newVal: ILocationTimepoint | null) {
    this.setSelectedTimepointItem(newVal)
  }

  get selectedDate () {
    return this.selectedLocationDate
  }

  set selectedDate (newVal: DateTime | null) {
    this.setSelectedLocationDate(newVal)
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  get isDisabled () {
    return this.$route.path.endsWith('/new') || this.$route.path.endsWith('/edit') || this.$route.path.endsWith('/stop')
  }

  get isDynamicStartButtonDisabled () {
    return !this.hasMountedDevicesWithProperties || !this.hasActiveDevicesWithPropertiesForDate(this.selectedDate)
  }

  selectTimepoint () {
    if (this.selectedTimepoint !== null) {
      this.selectedDate = this.selectedTimepoint.timepoint
    }
    this.updateRoute()
  }

  updateRoute () {
    if (this.selectedTimepoint) {
      if (isTimePointForStaticAction(this.selectedTimepoint)) {
        this.$router.push(`/configurations/${this.configurationId}/locations/static-location-actions/${this.selectedTimepoint.id}`)
      }

      if (isTimePointForDynamicAction(this.selectedTimepoint)) {
        this.$router.push(`/configurations/${this.configurationId}/locations/dynamic-location-actions/${this.selectedTimepoint.id}`)
      }
    } else {
      this.$router.push(`/configurations/${this.configurationId}/locations`)
    }
  }

  updateTimepointItemWhenDateSelected () {
    const filteredList = this.configurationLocationActionTimepoints.filter((item: ILocationTimepoint) => {
      return item.timepoint <= this.selectedDate!
    })
    if (filteredList.length > 0) {
      const lastEntry = filteredList[filteredList.length - 1]
      if (this.isEndLocationAndTimepointIsBeforeSelectedDate(lastEntry)) {
        this.selectedTimepoint = null
      } else {
        this.selectedTimepoint = lastEntry
      }
    } else {
      this.selectedTimepoint = null
    }
    this.updateRoute()
  }

  isEndLocationAndTimepointIsBeforeSelectedDate (item: ILocationTimepoint) {
    return (item.type === LocationTypes.staticEnd || item.type === LocationTypes.dynamicEnd) && item.timepoint < this.selectedDate!
  }
}
</script>

<style scoped>
.extraMarginForTooltipBtn{
  margin-left: 8px
}
</style>
