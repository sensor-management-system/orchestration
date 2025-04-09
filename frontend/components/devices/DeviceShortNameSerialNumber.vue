<!--
 SPDX-FileCopyrightText: 2020 - 2025

SPDX-License-Identifier: EUPL-1.2
 -->
<template>
  <div>
    {{ value.shortName }}
    <v-tooltip v-if="value.serialNumber" bottom>
      <template #activator="{ on, attrs }">
        <span
          v-bind="attrs"
          class="text--disabled pl-1"
          v-on="on"
        >
          ({{ value.serialNumber }})
        </span>
      </template>
      <span>Serial number</span>
    </v-tooltip>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'
import { Device } from '@/models/Device'

@Component
export default class DeviceShortNameSerialNumber extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  private value!: Device
}
</script>

<style scoped>

</style>
