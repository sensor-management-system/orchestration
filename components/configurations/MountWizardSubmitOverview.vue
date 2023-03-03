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
    <v-row>
      <v-col>
        <v-subheader>Mounting information</v-subheader>
        <v-simple-table>
          <tbody>
            <tr><td>Date range</td><td>{{ dateRangeString }}</td></tr>
            <tr>
              <td>Selected parent platform</td>
              <td v-if="selectedNode && selectedNode.isPlatform()">
                {{ selectedNode.unpack().platform.shortName }}
              </td>
              <td v-if="selectedNode && selectedNode.isConfiguration()">
                {{ selectedNode.unpack().label }} (Configuration root)
              </td>
            </tr>
          </tbody>
        </v-simple-table>
      </v-col>
    </v-row>

    <v-row v-if="devicesToMount.length > 0 || platformsToMount.length > 0">
      <v-col>
        <v-subheader>Devices and Platforms</v-subheader>

        <v-simple-table dense>
          <template #default>
            <thead>
              <tr>
                <th class="text-left">
                  Name
                </th>
                <th class="text-left">
                  Offsets (X | Y | Z)
                </th>
                <th class="text-left">
                  Absolute offsets (X | Y | Z)
                  <v-tooltip
                    right
                  >
                    <template #activator="{ on, attrs }">
                      <v-icon
                        class="pl-2"
                        small
                        v-bind="attrs"
                        v-on="on"
                      >
                        mdi-help-circle
                      </v-icon>
                    </template>
                    The offsets of the nodes are included.
                  </v-tooltip>
                </th>
                <th class="text-left">
                  Description
                </th>
                <th class="text-left">
                  Contact
                </th>
                <th v-if="selectedEndDate !== null" class="text-left table-border-left">
                  End description
                </th>
                <th v-if="selectedEndDate !== null" class="text-left">
                  End contact
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="platformsToMount.length !== 0 && devicesToMount.length > 0">
                <td colspan="7" class="font-weight-bold">
                  Devices
                </td>
              </tr>
              <tr
                v-for="(item, index) in devicesToMount"
                :key="'device-'+index"
              >
                <td>{{ item.entity.shortName }}</td>
                <td>({{ item.mountInfo.offsetX }} | {{ item.mountInfo.offsetY }} | {{ item.mountInfo.offsetZ }})</td>
                <td>({{ getAbsoluteOffsets(item.mountInfo).offsetX }} | {{ getAbsoluteOffsets(item.mountInfo).offsetY }} | {{ getAbsoluteOffsets(item.mountInfo).offsetZ }})</td>
                <td>
                  {{ item.mountInfo.beginDescription | shortenRight(14, '...') | orDefault }}
                </td>
                <td>
                  {{ fullNameOfBeginContact(item.mountInfo) | orDefault }}
                </td>
                <td v-if="selectedEndDate !== null && item.mountInfo.endDescription !== null" class="table-border-left">
                  {{ item.mountInfo.endDescription | shortenRight(14, '...') | orDefault }}
                </td>
                <td v-if="selectedEndDate !== null && item.mountInfo.endContact !== null">
                  {{ item.mountInfo.endContact.fullName | orDefault }}
                </td>
              </tr>
              <tr v-if="devicesToMount.length !== 0 && platformsToMount.length > 0">
                <td colspan="7" class="font-weight-bold">
                  Platforms
                </td>
              </tr>
              <tr
                v-for="(item, index) in platformsToMount"
                :key="'platform-'+index"
              >
                <td>{{ item.entity.shortName }}</td>
                <td>({{ item.mountInfo.offsetX }} | {{ item.mountInfo.offsetY }} | {{ item.mountInfo.offsetZ }})</td>
                <td>({{ getAbsoluteOffsets(item.mountInfo).offsetX }} | {{ getAbsoluteOffsets(item.mountInfo).offsetY }} | {{ getAbsoluteOffsets(item.mountInfo).offsetZ }})</td>
                <td>
                  {{ item.mountInfo.beginDescription | shortenRight(14, '...') | orDefault }}
                </td>
                <td>{{ fullNameOfBeginContact(item.mountInfo) | orDefault }}</td>
                <td v-if="selectedEndDate !== null && item.mountInfo.endDescription !== null" class="table-border-left">
                  {{ item.mountInfo.endDescription | shortenRight(14, '...') | orDefault }}
                </td>
                <td v-if="selectedEndDate !== null && item.mountInfo.endContact !== null">
                  {{ item.mountInfo.endContact.fullName | orDefault }}
                </td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop, PropSync, InjectReactive } from 'nuxt-property-decorator'

import { DateTime } from 'luxon'

import { Device } from '@/models/Device'
import { MountAction } from '@/models/MountAction'
import { Platform } from '@/models/Platform'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'

import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'
import { IOffsets } from '@/utils/configurationInterfaces'

@Component({
  filters: { dateToDateTimeStringHHMM }
})
export default class MountWizardSubmitOverview extends Vue {
  @PropSync('devicesToMount', {
    required: false,
    type: Array
  })
    syncedDevicesToMount!: { entity: Device, mountInfo: MountAction }[]

  @PropSync('platformsToMount', {
    required: false,
    type: Array
  })
    syncedPlatformsToMount!: { entity: Platform, mountInfo: MountAction }[]

  @Prop({
    default: (): IOffsets => ({ offsetX: 0, offsetY: 0, offsetZ: 0 }),
    required: false,
    type: Object
  })
  readonly parentOffsets!: IOffsets

  @InjectReactive() selectedDate!: DateTime
  @InjectReactive() selectedEndDate!: DateTime | null
  @InjectReactive() selectedNode!: ConfigurationsTreeNode | null

  get dateRangeString (): string {
    const start = `From ${dateToDateTimeStringHHMM(this.selectedDate)}`
    const end = (this.selectedEndDate === null) ? ' with open end' : ` until ${dateToDateTimeStringHHMM(this.selectedEndDate)}`
    return start + end
  }

  fullNameOfBeginContact (mountInfo: MountAction): string | undefined {
    return mountInfo.beginContact?.fullName
  }

  getAbsoluteOffsets (mountInfo: MountAction): IOffsets {
    return {
      offsetX: this.parentOffsets.offsetX + mountInfo.offsetX,
      offsetY: this.parentOffsets.offsetY + mountInfo.offsetY,
      offsetZ: this.parentOffsets.offsetZ + mountInfo.offsetZ
    }
  }
}
</script>

<style scoped>
.table-border-left {
  border-left: 1px solid #dddddd;
}
</style>
