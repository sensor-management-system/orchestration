<template>
  <div>
    <v-row>
      <v-col cols="12" md="3">
        <v-combobox
          label="Compartment"
          :items="compartmentNames"
          :value="valueCompartmentName"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('compartmentName', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-combobox
          label="Unit"
          :items="unitNames"
          :value="valueUnitName"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('unitName', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          label="Accuracy"
          :value="value.accuracy"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('accuracy', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <v-combobox
          label="Sampling media"
          :items="samplingMediaNames"
          :value="valueSamplingMediaName"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('samplingMediaName', $event)"
        />
      </v-col>
      <v-col cols="12" md="1">
        <v-text-field
          label="Measuring range min"
          :value="value.measuringRange.min"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('measuringRange.min', $event)"
        />
      </v-col>
      <v-col cols="12" md="1">
        <v-text-field
          label="Measuring range max"
          :value="value.measuringRange.max"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('measuringRange.max', $event)"
        />
      </v-col>
      <v-col cols="12" md="3" offset="1">
        <v-text-field
          label="Label"
          :value="value.label"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('label', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <v-select
          label="Property"
          :items="propertyNames"
          :value="valuePropertyName"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('propertyName', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          label="Failure value"
          :value="value.failureValue"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('failureValue', $event)"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component for a device property
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'
import { DeviceProperty } from '../models/DeviceProperty'

import Compartment from '../models/Compartment'
import SamplingMedia from '../models/SamplingMedia'
import Property from '../models/Property'
import Unit from '../models/Unit'

/**
 * A class component for a device property
 * @extends Vue
 */
@Component
// @ts-ignore
export default class DevicePropertyForm extends Vue {
  @Prop({
    default: () => new DeviceProperty(),
    required: true,
    type: DeviceProperty
  })
  // @ts-ignore
  value!: DeviceProperty

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly: boolean

  @Prop({
    default: () => [] as Compartment[],
    required: true,
    type: Array
  })
  compartments!: Compartment[]

  @Prop({
    default: () => [] as SamplingMedia[],
    required: true,
    type: Array
  })
  samplingMedias!: SamplingMedia[]

  @Prop({
    default: () => [] as Property[],
    required: true,
    type: Array
  })
  properties!: Property[]

  @Prop({
    default: () => [] as Unit[],
    required: true,
    type: Array
  })
  units!: Unit[]

  /**
   * update the internal model at a given key
   *
   * @param {string} key - a path to the property to set
   * @param {string} value - the value to set
   * @fires DevicePropertyForm#input
   */
  update (key: string, value: string) {
    const newObj: DeviceProperty = DeviceProperty.createFromObject(this.value)

    if (key === 'compartmentName') {
      const compartmentIndex = this.compartments.findIndex(c => c.name === value)
      if (compartmentIndex > -1) {
        newObj.setPath('compartmentUri', this.compartments[compartmentIndex].uri)
      } else {
        newObj.setPath('compartmentUri', '')
      }
    }

    if (key === 'unitName') {
      const unitIndex = this.units.findIndex(u => u.name === value)
      if (unitIndex > -1) {
        newObj.setPath('unitUri', this.units[unitIndex].uri)
      } else {
        newObj.setPath('unitUri', '')
      }
    }

    if (key === 'samplingMediaName') {
      const samplingMediaIndex = this.samplingMedias.findIndex(s => s.name === value)
      if (samplingMediaIndex > -1) {
        newObj.setPath('samplingMediaUri', this.samplingMedias[samplingMediaIndex].uri)
      } else {
        newObj.setPath('samplingMediaUri', '')
      }
    }

    if (key === 'propertyName') {
      const propertyIndex = this.properties.findIndex(p => p.name === value)
      if (propertyIndex > -1) {
        newObj.setPath('propertyUri', this.properties[propertyIndex].uri)
      } else {
        newObj.setPath('propertyUri', '')
      }
    }

    newObj.setPath(key, value)

    /**
     * input event
     * @event DevicePropertyForm#input
     * @type DeviceProperty
     */
    this.$emit('input', newObj)
  }

  get compartmentNames () : string[] {
    return this.compartments.map(c => c.name)
  }

  get valueCompartmentName (): string {
    const compartmentIndex = this.compartments.findIndex(c => c.uri === this.value.compartmentName)
    if (compartmentIndex > -1) {
      return this.compartments[compartmentIndex].name
    }
    return this.value.compartmentName
  }

  get unitNames (): string[] {
    return this.units.map(u => u.name)
  }

  get valueUnitName (): string {
    const unitIndex = this.units.findIndex(u => u.uri === this.value.unitUri)
    if (unitIndex > -1) {
      return this.units[unitIndex].name
    }
    return this.value.unitName
  }

  get samplingMediaNames (): string[] {
    return this.samplingMedias.map(s => s.name)
  }

  get valueSamplingMediaName (): string {
    const samplingMediaIndex = this.samplingMedias.findIndex(s => s.uri === this.value.samplingMediaUri)
    if (samplingMediaIndex > -1) {
      return this.samplingMedias[samplingMediaIndex].name
    }
    return this.value.samplingMediaName
  }

  get propertyNames (): string[] {
    return this.properties.map(p => p.name)
  }

  get valuePropertyName (): string {
    const propertyIndex = this.properties.findIndex(p => p.uri === this.value.propertyUri)
    if (propertyIndex > -1) {
      return this.properties[propertyIndex].name
    }
    return this.value.propertyName
  }
}
</script>
