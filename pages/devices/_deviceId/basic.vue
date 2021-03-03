<template>
  <NuxtChild
    v-model="device"
  />
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

import { Device } from '@/models/Device'

@Component
export default class DeviceBasicPage extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  readonly value!: Device

  get device (): Device {
    return this.value
  }

  set device (value: Device) {
    this.$emit('input', value)
  }
}
</script>
