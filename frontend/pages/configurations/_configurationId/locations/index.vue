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
      <v-btn
        v-if="$auth.loggedIn"
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
import { Component, Vue, InjectReactive, Watch } from 'nuxt-property-decorator'
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

import { ILocationTimepoint } from '@/serializers/controller/LocationActionTimepointSerializer'
import { isTimePointForDynamicAction, isTimePointForStaticAction } from '@/utils/locationHelper'
import { currentAsUtcDateSecondsAsZeros } from '@/utils/dateHelper'

import DateTimePicker from '@/components/DateTimePicker.vue'

@Component({
  components: {
    DateTimePicker
  },
  computed: {
    ...mapState('configurations',
      [
        'configuration',
        'configurationLocationActionTimepoints',
        'selectedTimepointItem',
        'selectedLocationDate'
      ]
    ),
    ...mapGetters('configurations',
      [
        'hasMountedDevicesWithProperties',
        'hasActiveDevicesWithPropertiesForDate'
      ]
    )
  },
  methods: {
    ...mapActions('configurations', ['setSelectedTimepointItem', 'setSelectedLocationDate'])
  }
})
export default class ConfigurationShowLocationPage extends Vue {
  @InjectReactive()
    editable!: boolean

  // vuex definition for typescript check
  private configuration!: ConfigurationsState['configuration']
  private configurationLocationActionTimepoints!: ConfigurationsState['configurationLocationActionTimepoints']
  private selectedTimepointItem!: ConfigurationsState['selectedTimepointItem']
  private selectedLocationDate!: ConfigurationsState['selectedLocationDate']
  private setSelectedTimepointItem!: SetSelectedTimepointItemAction
  private setSelectedLocationDate!: SetSelectedLocationDateAction
  private hasMountedDevicesWithProperties!: HasMountedDevicesWithPropertiesGetter
  private hasActiveDevicesWithPropertiesForDate!: HasActiveDevicesWithPropertiesForDate

  created () {
    this.selectDefaultAction()
  }

  selectDefaultAction (): void {
    if (!this.hasActionParam && !this.isEditPage && !this.isNewPage) {
      if (!this.selectedDate) {
        const now = currentAsUtcDateSecondsAsZeros()
        // when the begin date of the configuration is past the current date, set the current date
        if (!this.configuration?.startDate || this.configuration?.startDate < now) {
          this.selectedDate = now
        } else {
          // otherwise set the (future) begin of the configuration as date
          this.selectedDate = this.configuration.startDate
        }
      }

      this.updateTimepointItemWhenDateSelected()
    }
  }

  get hasActionParam (): boolean {
    return 'actionId' in this.$route.params
  }

  get isEditPage (): boolean {
    return this.$route.path.match(/edit$/) !== null
  }

  get isNewPage (): boolean {
    return this.$route.path.match(/new$/) !== null
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
        return
      }
      if (isTimePointForDynamicAction(this.selectedTimepoint)) {
        this.$router.push(`/configurations/${this.configurationId}/locations/dynamic-location-actions/${this.selectedTimepoint.id}`)
        return
      }
    }
    this.$router.push(`/configurations/${this.configurationId}/locations`)
  }

  updateTimepointItemWhenDateSelected () {
    const filteredList = this.configurationLocationActionTimepoints.filter((item: ILocationTimepoint) => {
      return item.timepoint <= this.selectedDate!
    })

    if (filteredList.length > 0) {
      const recentEntry = filteredList[0]
      if (this.isEndLocationAndTimepointIsBeforeSelectedDate(recentEntry)) {
        this.selectedTimepoint = null
      } else {
        this.selectedTimepoint = recentEntry
      }
    } else {
      this.selectedTimepoint = null
    }
    this.updateRoute()
  }

  isEndLocationAndTimepointIsBeforeSelectedDate (item: ILocationTimepoint) {
    return (item.type === LocationTypes.staticEnd || item.type === LocationTypes.dynamicEnd) && item.timepoint < this.selectedDate!
  }

  @Watch('$route')
  onRouteChange () {
    this.selectDefaultAction()
  }
}
</script>

<style scoped>
.extraMarginForTooltipBtn{
  margin-left: 8px
}
</style>
