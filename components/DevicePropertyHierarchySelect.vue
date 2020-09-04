<template>
  <div>
    <v-select
      :value="selectedDevice"
      :items="devices"
      :item-text="(device) => device.shortName"
      :item-value="(device) => device"
      :label="deviceSelectLabel"
      clearable
      @change="addDevice"
    />
    <v-select
      v-if="selectedDevice"
      :value="value"
      :items="propertiesOfDevice"
      :item-text="(property) => property.propertyName"
      :item-value="(property) => property"
      :label="propertySelectLabel"
      clearable
      @change="addProperty"
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

  private selectedDevice: Device | null = null

  /**
   * selects a devices that is used to display its properties
   *
   * @param {Device} device - the device whose properties should be displayed
   */
  addDevice (device?: Device) {
    this.selectedDevice = device || null

    if (device && device.properties.length === 1) {
      this.addProperty(device.properties[0])
    } else {
      this.addProperty()
    }
  }

  get propertiesOfDevice (): DeviceProperty[] {
    if (!this.selectedDevice) {
      return []
    }
    return this.selectedDevice.properties
  }

  /**
   * update the internal model at a given key
   *
   * @param {DeviceProperty} property - the device property to select
   * @fires DevicePropertyHierarchySelect#input
   */
  addProperty (property?: DeviceProperty) {
    /**
     * input event
     * @event DevicePropertyHierarchySelect#input
     * @type DeviceProperty|null
     */
    this.$emit('input', property || null)
  }
}
</script>
