<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <EntitySelect
    v-model="wrappedValue"
    :readonly="readonly"
    :fetch-function="findAllDeviceTypes"
    :label="label"
    color="red"
  />
</template>

<script lang="ts">
/**
 * @file provides a component to select device types
 * @author <marc.hanisch@gfz-potsdam.de>
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import EntitySelect from '@/components/EntitySelect.vue'

import { DeviceType } from '@/models/DeviceType'

type DeviceTypeLoaderFunction = () => Promise<DeviceType[]>

/**
 * A class component to select device types
 * @extends Vue
 */
@Component({
  components: {
    EntitySelect
  }
})
// @ts-ignore
export default class DeviceTypeSelect extends Vue {
  /**
   * a list of DeviceTypes
   */
  @Prop({
    default: () => [] as DeviceType[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value!: DeviceType[]

  /**
   * whether the component is in readonly mode or not
   */
  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

  /**
   * the label of the component
   */
  @Prop({
    required: true,
    type: String
  })
  // @ts-ignore
  readonly label!: string

  /**
   * fetches a list of DeviceTypes
   */
  get findAllDeviceTypes (): DeviceTypeLoaderFunction {
    return () => { return this.$api.deviceTypes.findAll() }
  }

  /**
   * returns the list of DeviceTypes
   *
   * @return {DeviceType[]} a list of DeviceTypes
   */
  get wrappedValue () {
    return this.value
  }

  /**
   * triggers an input event when the list of DeviceTypes has changed
   *
   * @param {DeviceType[]} newValue - a list of DeviceTypes
   * @fires DeviceTypeSelect#input
   */
  set wrappedValue (newValue) {
    /**
     * fires an input event
     * @event DeviceTypeSelect#input
     * @type {DeviceType[]}
     */
    this.$emit('input', newValue)
  }
}
</script>
