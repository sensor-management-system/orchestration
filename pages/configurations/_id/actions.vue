<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020, 2021
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Erik Pongratz (UFZ, erik.pongratz@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
  <v-card
    flat
  >
    <v-card-text>
      <div v-if="timelineActions.length === 0">
        <p class="text-center">
          There are no actions for this configuration yet.
        </p>
      </div>
      <v-timeline v-else dense>
        <v-timeline-item
          v-for="action in timelineActions"
          :key="action.key"
          :color="action.color"
          :icon="action.icon"
          class="mb-4"
          small
        >
          <ConfigurationsTimelineActionCard
            :action="action"
          />
        </v-timeline-item>
      </v-timeline>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'nuxt-property-decorator'

import { Configuration } from '@/models/Configuration'
import {
  DeviceMountTimelineAction,
  DeviceUnmountTimelineAction,
  ITimelineAction,
  PlatformMountTimelineAction,
  PlatformUnmountTimelineAction,
  StaticLocationBeginTimelineAction,
  StaticLocationEndTimelineAction,
  DynamicLocationBeginTimelineAction,
  DynamicLocationEndTimelineAction
} from '@/utils/configurationInterfaces'

import { byDateOldestLast } from '@/modelUtils/mountHelpers'
import { dateToDateTimeString } from '@/utils/dateHelper'

import ConfigurationsTimelineActionCard from '@/components/configurations/ConfigurationsTimelineActionCard.vue'

@Component({
  components: { ConfigurationsTimelineActionCard },
  filters: {
    dateToDateTimeString
  }
})
export default class ConfigurationActions extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: Configuration

  head () {
    return {
      titleTemplate: 'Actions - %s'
    }
  }

  get configuration () {
    return this.value
  }

  get timelineActions (): ITimelineAction[] {
    const devices = this.configuration.deviceMountActions.map(a => a.device)
    const result: ITimelineAction[] = []
    for (const platformMountAction of this.configuration.platformMountActions) {
      result.push(new PlatformMountTimelineAction(platformMountAction))
    }
    for (const deviceMountAction of this.configuration.deviceMountActions) {
      result.push(new DeviceMountTimelineAction(deviceMountAction))
    }
    for (const platformUnmountAction of this.configuration.platformUnmountActions) {
      result.push(new PlatformUnmountTimelineAction(platformUnmountAction))
    }
    for (const deviceUnmountAction of this.configuration.deviceUnmountActions) {
      result.push(new DeviceUnmountTimelineAction(deviceUnmountAction))
    }
    for (const action of this.configuration.staticLocationBeginActions) {
      result.push(new StaticLocationBeginTimelineAction(action))
    }
    for (const action of this.configuration.staticLocationEndActions) {
      result.push(new StaticLocationEndTimelineAction(action))
    }
    for (const action of this.configuration.dynamicLocationBeginActions) {
      result.push(new DynamicLocationBeginTimelineAction(action, devices))
    }
    for (const action of this.configuration.dynamicLocationEndActions) {
      result.push(new DynamicLocationEndTimelineAction(action))
    }

    result.sort(byDateOldestLast)
    return result
  }
}
</script>

<style scoped>

</style>
