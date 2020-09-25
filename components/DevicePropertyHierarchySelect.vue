<template>
  <div>
    <v-select
      :value="selectedDevice"
      :items="devices"
      :item-text="(device) => device.shortName"
      :item-value="(device) => device"
      :label="deviceSelectLabel"
      clearable
      :readonly="readonly"
      :disabled="readonly"
      @change="selectDevice"
    />
    <v-select
      v-if="selectedDevice"
      :value="value"
      :items="propertiesOfDevice"
      :item-text="(property) => property.propertyName"
      :item-value="(property) => property"
      :label="propertySelectLabel"
      clearable
      :readonly="readonly"
      :disabled="readonly"
      @change="selectProperty"
    />
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component for an attachment
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import Device from '@/models/Device'
import { DeviceProperty } from '@/models/DeviceProperty'

/**
 * A class component that displays a single attached file
 * @extends Vue
 */
@Component
// @ts-ignore
export default class DevicePropertyHierarchySelect extends Vue {
  @Prop({
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly devices!: Device[]

  @Prop({
    default: 'Select a device',
    type: String
  })
  // @ts-ignore
  readonly deviceSelectLabel: string

  @Prop({
    default: 'Select a property',
    type: String
  })
  // @ts-ignore
  readonly propertySelectLabel: string

  @Prop({
    default: null,
    type: Object
  })
  // @ts-ignore
  readonly value: DeviceProperty

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

  private selectedDevice: Device | null = null

  /**
   * selects a devices that is used to display its properties
   *
   * @param {Device} device - the device whose properties should be displayed
   */
  selectDevice (device?: Device) {
    const oldState = this.selectedDevice
    this.selectedDevice = device || null

    if (device && device.properties.length === 1) {
      this.selectProperty(device.properties[0])
    } else if (oldState !== null) {
      this.selectProperty(null)
    }
  }

  get propertiesOfDevice (): DeviceProperty[] {
    if (!this.selectedDevice) {
      return []
    }
    return this.selectedDevice.properties
  }

  /**
   * triggers the selected property
   *
   * @param {DeviceProperty} property - the device property which is selected
   * @fires DevicePropertyHierarchySelect#input
   */
  selectProperty (property: DeviceProperty | null = null) {
    /**
     * input event
     * @event DevicePropertyHierarchySelect#input
     * @type DeviceProperty|null
     */
    this.$emit('input', property)
  }
}
</script>
