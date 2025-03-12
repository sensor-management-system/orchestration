<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-list>
    <template v-for="(device, index) in devices">
      <v-list-item
        :key="device.id"
      >
        <v-list-item-content>
          <v-list-item-title :class="{'text--disabled': isDeviceUsedInTree(device)}">
            <extended-item-name :value="device" />
          </v-list-item-title>
        </v-list-item-content>
        <v-list-item-action v-if="!isDeviceUsedInTree(device)">
          <v-btn
            v-if="isAvailable(device) && canModifyEntity(device)"
            depressed
            color="primary"
            @click="emitSelectedDevice(device)"
          >
            Select
          </v-btn>
          <v-tooltip
            v-else
            top
          >
            <template #activator="{ on }">
              <v-btn icon v-on="on" @click.stop>
                <v-icon color="warning">
                  mdi-alert
                </v-icon>
              </v-btn>
            </template>
            <span v-if="!isAvailable(device)">{{ availabilityReason(getAvailability(device)) }}</span>
            <span v-else-if="!canModifyEntity(device)">No permission to select <em>{{ device.shortName }}</em>.</span>
          </v-tooltip>
        </v-list-item-action>
      </v-list-item>
      <v-divider
        v-if="index < devices.length - 1"
        :key="`reuse-device-exchange--${index}`"
      />
    </template>
  </v-list>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { mapGetters, mapState } from 'vuex'
import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'
import { Device } from '@/models/Device'
import { Availability } from '@/models/Availability'
import { DevicesState } from '@/store/devices'
import { CanModifyEntityGetter } from '@/store/permissions'
import { availabilityReason } from '@/utils/mountHelper'

@Component({
  methods: { availabilityReason },
  components: { ExtendedItemName },
  computed: {
    ...mapState('devices', ['devices', 'deviceAvailabilities']),
    ...mapGetters('permissions', ['canModifyEntity'])
  }
})
export default class ReuseDeviceExchangeList extends Vue {
  @Prop({
    required: true
  })
  readonly devicesUsedInTree!: Device[]

  deviceAvailabilities!: DevicesState['deviceAvailabilities']
  canModifyEntity!: CanModifyEntityGetter

  isDeviceUsedInTree (device: Device) {
    const found = this.devicesUsedInTree.find(el => el.id === device.id)
    if (found) {
      return true
    }
    return false
  }

  isAvailable (entity: Device): boolean {
    return this.getAvailability(entity)?.available || false
  }

  getAvailability (entity: Device): Availability | undefined {
    return this.deviceAvailabilities.find(availability => availability.id === entity.id)
  }

  emitSelectedDevice (device: Device) {
    this.$emit('selected', device)
  }
}
</script>

<style scoped>

</style>
