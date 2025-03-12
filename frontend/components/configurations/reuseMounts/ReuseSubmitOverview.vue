<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Maximilian Schaldach <maximilian.schaldach@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-card flat>
      <v-card-title>
        Date range
      </v-card-title>
      <v-card-subtitle>
        {{ dateRangeString }}
      </v-card-subtitle>
    </v-card>

    <v-simple-table>
      <tbody>
        <tr><td>Date range</td><td>{{ dateRangeString }}</td></tr>
      </tbody>
    </v-simple-table>
    <v-simple-table dense>
      <template #default>
        <thead>
          <tr>
            <th class="text-left">
              Name
            </th>
            <th class="text-left">
              Label
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
              Coordinates (X | Y | Z)
            </th>
            <th class="text-left">
              Mount description
            </th>
            <th class="text-left">
              Mount contact
            </th>
            <th v-if="endDate !== null" class="text-left table-border-left">
              Unmount description
            </th>
            <th v-if="endDate !== null" class="text-left">
              Unmount contact
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in treeWithoutConfigrationNode" :key="itemKey(item)">
            <td>
              <extended-item-name
                :value="getEntity(item)"
              />
            </td>
            <td>{{ item.unpack().label | orDefault }}</td>
            <td>({{ item.unpack().offsetX }} | {{ item.unpack().offsetY }} | {{ item.unpack().offsetZ }})</td>
            <td>{{ getAbsoluteOffsets(item) }}</td>
            <td v-if="item.unpack().x !== null || item.unpack().y !== null || item.unpack().z !== null">
              ({{ item.unpack().x }} | {{ item.unpack().y }} | {{ item.unpack().z }})
            </td>
            <!-- For the very same default value we show if the other fields are not set -->
            <td v-else>
              {{ null | orDefault }}
            </td>
            <td>
              {{ item.unpack().beginDescription | shortenRight(14, '...') | orDefault }}
            </td>
            <td>{{ fullNameOfBeginContact(item.unpack()) | orDefault }}</td>
            <td v-if="endDate !== null && item.unpack().endDescription !== null" class="table-border-left">
              {{ item.unpack().endDescription | shortenRight(14, '...') | orDefault }}
            </td>
            <td v-if="endDate !== null && item.unpack().endContact !== null">
              {{ item.unpack().endContact.fullName | orDefault }}
            </td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { DateTime } from 'luxon'
import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { AddDeviceMountActionAction, AddPlatformMountActionAction } from '@/store/configurations'
import { Configuration } from '@/models/Configuration'
import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { MountAction } from '@/models/MountAction'
import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'
import { sumOffsets } from '@/utils/configurationsTreeHelper'
import { round } from '@/utils/numericsHelper'
import { PlatformNode } from '@/viewmodels/PlatformNode'
import { DeviceNode } from '@/viewmodels/DeviceNode'

@Component({
  components: { ExtendedItemName }
})
export default class ReuseSubmitOverview extends Vue {
  @Prop({
    required: true,
    type: Object
  })
    selectedMountTree!: ConfigurationsTree

  @Prop({
    required: true,
    type: Object
  })
    selectedConfiguration!: Configuration

  @Prop({
    default: null,
    required: true,
    type: Object
  })
    beginDate!: DateTime

  @Prop({
    default: null,
    required: true
  })
    endDate!: DateTime | null

  addDeviceMountAction!: AddDeviceMountActionAction
  addPlatformMountAction!: AddPlatformMountActionAction

  itemKey (item: PlatformNode | DeviceNode): string {
    return `item-${item.id}`
  }

  get treeWithoutConfigrationNode () {
    return this.selectedMountTree.at(0).getTree().getAllNodesAsList()
  }

  get dateRangeString (): string {
    const start = `From ${dateToDateTimeStringHHMM(this.beginDate)}`
    const end = (this.endDate === null) ? ' with open end' : ` until ${dateToDateTimeStringHHMM(this.endDate)}`
    return start + end
  }

  get configurationId (): string {
    return this.$route.params.configurationId
  }

  getEntity (node: ConfigurationsTreeNode) {
    if (node.isDevice()) {
      return node.unpack().device
    }

    if (node.isPlatform()) {
      return node.unpack().platform
    }
  }

  getAbsoluteOffsets (node: ConfigurationsTreeNode): string {
    if (node.isConfiguration()) {
      return ''
    }

    const mountInfo = node.unpack()
    const parents = this.selectedMountTree.getParents(node)
    const parentOffsets = sumOffsets([...parents])
    const absoluteOffsets = {
      offsetX: parentOffsets.offsetX + mountInfo.offsetX,
      offsetY: parentOffsets.offsetY + mountInfo.offsetY,
      offsetZ: parentOffsets.offsetZ + mountInfo.offsetZ
    }

    return `${round(absoluteOffsets.offsetX, 6)} |
    ${round(absoluteOffsets.offsetY, 6)} |
    ${round(absoluteOffsets.offsetZ, 6)}`
  }

  fullNameOfBeginContact (mountInfo: MountAction): string | undefined {
    return mountInfo.beginContact?.fullName
  }
}
</script>

<style scoped>

</style>
