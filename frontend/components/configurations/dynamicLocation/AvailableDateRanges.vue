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
