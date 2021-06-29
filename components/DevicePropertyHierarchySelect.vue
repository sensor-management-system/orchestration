<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
    <v-select
      :value="device"
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
      v-if="device"
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
 * @file provides a component to select a property from a list of devices
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { Device } from '@/models/Device'
import { DeviceProperty } from '@/models/DeviceProperty'

/**
 * A class component to select a property from a list of devices
 * @extends Vue
 */
@Component
// @ts-ignore
export default class DevicePropertyHierarchySelect extends Vue {
  /**
   * the list of devices
   */
  @Prop({
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly devices!: Device[]

  /**
   * the label of the device select
   */
  @Prop({
    default: 'Select a device',
    type: String
  })
  // @ts-ignore
  readonly deviceSelectLabel: string

  /**
   * the label of the property select
   */
  @Prop({
    default: 'Select a property',
    type: String
  })
  // @ts-ignore
  readonly propertySelectLabel: string

  /**
   * a DeviceProperty
   */
  @Prop({
    default: null,
    type: Object
  })
  // @ts-ignore
  readonly value: DeviceProperty

  /**
   * whether the component is in readonly mode or not
   */
  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

  private selectedDevice: Device | null = null

  get device (): Device | null {
    if (this.selectedDevice) {
      return this.selectedDevice
    }
    if (this.value && this.value.id) {
      for (const device of this.devices) {
        const devicePropertyIndex = device.properties.findIndex(p => p.id === this.value.id)
        if (devicePropertyIndex > -1) {
          this.selectedDevice = device
          return this.selectedDevice
        }
      }
    }
    return null
  }

  mounted () {
    // Lets check if we have already an property
    if (this.selectedDevice == null && this.value != null) {
      // and if we can find the device of it, so that
      // it is prefilled when we open this component...
      for (const device of this.devices) {
        for (const property of device.properties) {
          const propertyId = property.id
          if (propertyId === this.value.id) {
            this.selectedDevice = device
            break
          }
        }
      }
    }
  }

  /**
   * selects a devices that is used to display its properties
   *
   * when no device parameter is given, the currently selected device is set to null
   * when another device than the selected device is given, the selected property is set to null
   * when the device has only one property, it is automatically selected
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

  /**
   * returns a list of Properties for the selected device
   *
   * @return {DeviceProperty[]} a list of Properties
   */
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
     * @type {DeviceProperty|null}
     */
    this.$emit('input', property)
  }
}
</script>
