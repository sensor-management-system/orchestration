<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Tim Eder <tim.eder@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-container>
    <v-row>
      <v-col>
        <v-list>
          <v-list-item
            v-for="deviceWithActions in listOfDevicesAndTheirDeviceMountActions"
            :key="`deviceWithActions-${deviceWithActions.device.id}`"
          >
            <v-list-item-content>
              <ExtendedItemName :value="deviceWithActions.device" />
              <v-list>
                <v-list-item
                  v-for="action in deviceWithActions.actions"
                  :key="`deviceWithActions-${deviceWithActions.device.id}-action-${action.id}`"
                >
                  <v-list-item-content>
                    {{ getItemLabel(action) }}
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-btn
                      color="primary"
                      @click="emitSelect(action)"
                    >
                      Apply
                    </v-btn>
                  </v-list-item-action>
                </v-list-item>
              </v-list>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'nuxt-property-decorator'
import { mapState } from 'vuex'
import { DateTime } from 'luxon'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Device } from '@/models/Device'
import { dateToDateTimeString } from '@/utils/dateHelper'
import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'
import { ConfigurationsState } from '@/store/configurations'

@Component({
  components: { ExtendedItemName },
  computed: {
    ...mapState('configurations', ['deviceMountActionsIncludingDeviceInformation'])
  }
})
export default class AvailableDateRanges extends Vue {
  // vuex definition for typescript check
  deviceMountActionsIncludingDeviceInformation!: ConfigurationsState['deviceMountActionsIncludingDeviceInformation']

  get listOfDevicesAndTheirDeviceMountActions () {
    return this.deviceMountActionsIncludingDeviceInformation.reduce((acc: {
      device: Device,
      actions: DeviceMountAction[]
    }[], currentValue: DeviceMountAction) => {
      const found = acc.find((el) => {
        return el.device.id === currentValue.device.id
      })
      if (found) {
        found.actions.push(currentValue)
      } else {
        acc.push(
          {
            device: currentValue.device,
            actions: [currentValue]
          }
        )
      }
      return acc
    }, [])
  }

  parseDate (date: DateTime | null) {
    if (!date) {
      return '—'
    }
    return dateToDateTimeString(date)
  }

  getItemLabel (action: DeviceMountAction) {
    return `From: ${this.parseDate(action.beginDate)} | To: ${this.parseDate(action.endDate)}`
  }

  emitSelect (action: DeviceMountAction) {
    this.$emit('selected', action)
  }
}
</script>

<style scoped>

</style>
