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
    <v-card v-if="hasDeviceToArchive">
      <v-card-title class="headline">
        Archive device
      </v-card-title>
      <v-card-text>
        <p>Do you really want to archive the device <em>{{ deviceToArchive.shortName }}</em>?</p>
        <p>
          Achived devices can no longer be edited or used in configurations until they are restored.
        </p>
        <p>
          They are not included in the device search by default.
        </p>
        <p>You can only archive a device if it is not actively used in a configuration.</p>
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

import { Device } from '@/models/Device'
import { DevicesState, LoadDeviceMountActionsAction } from '@/store/devices'

@Component({
  computed: mapState('devices', ['deviceMountActions']),
  methods: mapActions('devices', ['loadDeviceMountActions'])
})
export default class DeviceArchiveDialog extends Vue {
  @Prop({
    required: true,
    type: Boolean
  })
  readonly value!: boolean

  @Prop({
    type: Object
  })
  readonly deviceToArchive!: Device

  loadDeviceMountActions!: LoadDeviceMountActionsAction
  deviceMountActions!: DevicesState['deviceMountActions']

  get showDialog (): boolean {
    return this.value
  }

  set showDialog (value: boolean) {
    this.$emit('input', value)
  }

  get hasDeviceToArchive () {
    return this.deviceToArchive !== null
  }

  get problemThatPreventArchiving () {
    const now = DateTime.utc()
    for (const deviceMountAction of this.deviceMountActions) {
      if (!deviceMountAction.basicData.endDate) {
        return new Error('Mount in configuration "' + deviceMountAction.configuration.label + '" without end date')
      }
      if (deviceMountAction.basicData.endDate > now) {
        return new Error('Mount in configuration "' + deviceMountAction.configuration.label + '" is still in the future')
      }
    }
    return null
  }

  get hasProblemThatPreventArchiving () {
    return !!this.problemThatPreventArchiving
  }

  @Watch('deviceToArchive', {
    immediate: true
  })
  async onDeviceChange (val: Device) {
    if (val && val.id) {
      await this.loadDeviceMountActions(val.id)
    }
  }
}
</script>

<style scoped>

</style>
