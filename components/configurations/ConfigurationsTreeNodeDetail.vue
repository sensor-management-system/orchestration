<template>
  <div>
    <PlatformMountListItem
      v-if="node.isPlatform()"
      :platform="node.unpack().platform"
    >
      <template #mount>
        <ConfigurationsPlatformDeviceMountData
          :mount-action="node.unpack()"
        />
      </template>
    </PlatformMountListItem>

    <DevicesMountListItem
      v-if="node.isDevice()"
      :device="node.unpack().device"
    >
      <template #mount>
        <ConfigurationsPlatformDeviceMountData
          :mount-action="node.unpack()"
        />
      </template>
    </DevicesMountListItem>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { Prop } from 'nuxt-property-decorator'
import { } from '@/models/Platform'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import PlatformMountListItem from '@/components/platforms/PlatformMountListItem.vue'
import DevicesMountListItem from '@/components/devices/DevicesMountListItem.vue'
import ConfigurationsPlatformDeviceMountData from '@/components/ConfigurationsPlatformDeviceMountData.vue'
@Component({
  components: { ConfigurationsPlatformDeviceMountData, DevicesMountListItem, PlatformMountListItem }
})
export default class ConfigurationsTreeNodeDetail extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private node!: ConfigurationsTreeNode
}
</script>

<style scoped>

</style>
