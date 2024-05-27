<!--
SPDX-FileCopyrightText: 2020 - 2022
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Erik Pongratz <erik.pongratz@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-dialog
    v-model="showDialog"
    max-width="500"
    @click:outside="$emit('cancel-archiving')"
  >
    <v-card v-if="hasConfigurationToArchive">
      <v-card-title class="headline">
        Archive configuration
      </v-card-title>
      <v-card-text>
        <p>Do you really want to archive the configuration <em>{{ configurationToArchive.label }}</em>?</p>
        <p>
          Achived configurations can no longer be changed until they are restored.
        </p>
        <p>
          They are not included in the configuration search by default.
        </p>
        <p>You can only archive a configuration if no active mount is left.</p>
      </v-card-text>
      <v-alert v-if="hasProblemThatPreventArchiving" type="warning" text>
        <p>
          It is not possible to archive the configuration:
        </p>
        <ul>
          <li>
            {{ problemThatPreventArchiving.message }}
          </li>
        </ul>
      </v-alert>
      <v-card-actions>
        <v-btn
          text
          @click="$emit('cancel-archiving')"
        >
          No
        </v-btn>
        <v-spacer />
        <v-btn
          text
          :disabled="hasProblemThatPreventArchiving"
          @click="$emit('submit-archiving')"
        >
          <v-icon left>
            mdi-archive-lock
          </v-icon>
          Archive
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'nuxt-property-decorator'
import { mapActions, mapState } from 'vuex'
import { DateTime } from 'luxon'

import { Configuration } from '@/models/Configuration'
import { ConfigurationsState, LoadDeviceMountActionsAction, LoadLocationActionTimepointsAction, LoadPlatformMountActionsAction, LocationTypes } from '@/store/configurations'

@Component({
  computed: mapState('configurations', [
    'configurationDeviceMountActions',
    'configurationPlatformMountActions',
    'configurationLocationActionTimepoints'
  ]),
  methods: mapActions('configurations', [
    'loadDeviceMountActions',
    'loadPlatformMountActions',
    'loadLocationActionTimepoints'
  ])
})
export default class ConfigurationArchiveDialog extends Vue {
  @Prop({
    required: true,
    type: Boolean
  })
  readonly value!: boolean

  @Prop({
    type: Object
  })
  readonly configurationToArchive!: Configuration

  loadDeviceMountActions!: LoadDeviceMountActionsAction
  loadPlatformMountActions!: LoadPlatformMountActionsAction
  loadLocationActionTimepoints!: LoadLocationActionTimepointsAction
  configurationDeviceMountActions!: ConfigurationsState['configurationDeviceMountActions']
  configurationPlatformMountActions!: ConfigurationsState['configurationPlatformMountActions']
  configurationLocationActionTimepoints!: ConfigurationsState['configurationLocationActionTimepoints']

  get showDialog (): boolean {
    return this.value
  }

  set showDialog (value: boolean) {
    this.$emit('input', value)
  }

  get hasConfigurationToArchive () {
    return this.configurationToArchive !== null
  }

  get problemThatPreventArchiving () {
    const now = DateTime.utc()
    for (const deviceMountAction of this.configurationDeviceMountActions) {
      if (!deviceMountAction.endDate) {
        return new Error('Device mount "' + deviceMountAction.device.shortName + '" without end date')
      }
      if (deviceMountAction.endDate > now) {
        return new Error('End of device mount ' + deviceMountAction.device.shortName + '" is still in the future')
      }
    }
    for (const platformMountAction of this.configurationPlatformMountActions) {
      if (!platformMountAction.endDate) {
        return new Error('Platform mount for "' + platformMountAction.platform.shortName + '" without end date')
      }
      if (platformMountAction.endDate > now) {
        return new Error('End of platform mount ' + platformMountAction.platform.shortName + '" is still in the future')
      }
    }
    if (this.configurationLocationActionTimepoints) {
      const lastEntry = this.configurationLocationActionTimepoints[this.configurationLocationActionTimepoints.length - 1]
      if (lastEntry) {
        if (lastEntry.type === LocationTypes.dynamicStart || lastEntry.type === LocationTypes.staticStart) {
          return new Error('Configuration has no end of location')
        }
        if (lastEntry.timepoint > now) {
          return new Error('Configuration has a location that is still in the future')
        }
      }
    }
    return null
  }

  get hasProblemThatPreventArchiving () {
    return !!this.problemThatPreventArchiving
  }

  @Watch('configurationToArchive', {
    immediate: true
  })
  async onConfigurationChange (val: Configuration) {
    if (val && val.id) {
      await Promise.all([
        this.loadDeviceMountActions(val.id),
        this.loadPlatformMountActions(val.id),
        this.loadLocationActionTimepoints(val.id)
      ])
    }
  }
}
</script>

<style scoped>

</style>
