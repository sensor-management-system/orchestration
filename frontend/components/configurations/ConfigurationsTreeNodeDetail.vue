<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <PlatformMountListItem
      v-if="node.isPlatform()"
      :platform="node.unpack().platform"
    >
      <template #mount>
        <base-mount-info
          :mount-action="node.unpack()"
          :editable="editable"
          :deletable="deletable"
          :disabled="node.unpack().platform.archived"
          :warning="node.unpack().platform.archived ? 'Platform is archived. Restore it to edit the mount.' : ''"
          @delete="$emit('delete')"
        />
      </template>
    </PlatformMountListItem>

    <DevicesMountListItem
      v-if="node.isDevice()"
      :device="node.unpack().device"
    >
      <template #mount>
        <base-mount-info
          :mount-action="node.unpack()"
          :editable="editable"
          :deletable="deletable"
          :disabled="node.unpack().device.archived"
          :warning="node.unpack().device.archived ? 'Device is archived. Restore it to edit the mount.' : ''"
          @delete="$emit('delete')"
        />
      </template>
    </DevicesMountListItem>
    <template v-if="node.isConfiguration()">
      <div>
        <v-divider class="pb-4" />
        <configurations-basic-data :value="node.unpack().configuration" />
      </div>
    </template>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'

import PlatformMountListItem from '@/components/platforms/PlatformMountListItem.vue'
import DevicesMountListItem from '@/components/devices/DevicesMountListItem.vue'
import ConfigurationsBasicData from '@/components/configurations/ConfigurationsBasicData.vue'
import BaseMountInfo from '@/components/shared/BaseMountInfo.vue'

@Component({
  components: { DevicesMountListItem, PlatformMountListItem, BaseMountInfo, ConfigurationsBasicData }
})
export default class ConfigurationsTreeNodeDetail extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private node!: ConfigurationsTreeNode

  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  private editable!: boolean

  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  private deletable!: boolean
}
</script>

<style scoped>

</style>
