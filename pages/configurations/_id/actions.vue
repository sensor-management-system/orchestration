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
  PlatformUnmountTimelineAction
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

  get configuration () {
    return this.value
  }

  get timelineActions (): ITimelineAction[] {
    const result = []
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

    result.sort(byDateOldestLast)
    return result
  }
}
</script>

<style scoped>

</style>
