<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <template v-if="!readonly">
      <v-select
        :value="device"
        :items="devices"
        :item-text="(device) => device.shortName"
        :item-value="(device) => device"
        :label="deviceSelectLabel"
        :rules="deviceSelectRules"
        clearable
        no-data-text="No devices available for the selected date range"
        :disabled="disabled"
        @change="selectDevice"
      >
        <template v-if="unselectableDevices.length > 0" #append-item>
          <v-divider />
          <v-list>
            <v-list-item v-for="(value,index) in unselectableDevices" :key="index">
              <v-label disabled>
                {{ value.device.shortName }}
              </v-label>
              <v-spacer />
              <v-tooltip left>
                <template #activator="{ on, attrs }">
                  <v-icon
                    v-bind="attrs"
                    color="warning"
                    v-on="on"
                  >
                    mdi-alert
                  </v-icon>
                </template>
                <span>{{ value.invalidReason }}</span>
              </v-tooltip>
            </v-list-item>
          </v-list>
        </template>
      </v-select>
      <v-select
        v-if="device"
        :value="value"
        :items="propertiesOfDevice"
        :item-text="(property) => generatePropertyName(property)"
        :item-value="(property) => property"
        :label="propertySelectLabel"
        :rules="propertySelectRules"
        clearable
        :disabled="disabled"
        @change="selectProperty"
      />
    </template>
    <template v-else>
      <v-row>
        <v-col>
          <label>{{ deviceSelectLabel }}</label>
          {{ deviceName }}
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <label>{{ propertySelectLabel }}</label>
          {{ propertyName }}
        </v-col>
      </v-row>
    </template>
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
   * the list of devices which are unselectable for a specific reason
   */
  @Prop({
    required: false,
    type: Array,
    default: () => []
  })
  // @ts-ignore
  readonly unselectableDevices!: {device: Device, invalidReason: string}[]

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

  /**
   * whether the component is disabled or not
   */
  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly disabled: boolean

  @Prop({ default: () => [], type: Array }) readonly deviceSelectRules!: []
  @Prop({ default: () => [], type: Array }) readonly propertySelectRules!: []

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

  get deviceName (): string {
    let deviceName: string = ''
    // only show the device name when a property was selected
    if (this.value && this.device) {
      deviceName = this.device.shortName
    }
    return this.$options.filters?.orDefault(deviceName)
  }

  get propertyName (): string {
    return this.$options.filters?.orDefault(this.generatePropertyName(this.value))
  }

  generatePropertyName (value: DeviceProperty) {
    if (value) {
      const propertyName = value.propertyName ?? ''
      const label = value.label ?? ''
      const unit = value.unitName ?? ''
      return `${propertyName} ${label ? `- ${label}` : ''} ${unit ? `(${unit})` : ''}`
    }
    return ''
  }
}
</script>
