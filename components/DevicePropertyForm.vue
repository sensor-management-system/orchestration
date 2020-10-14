<template>
  <div>
    <p>
      {{ value.compartmentName }}
      {{ value.compartmentUri }}
    </p>
    <v-row>
      <v-col cols="12" md="3">
        <v-combobox
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
          label="Sampling media"
          :items="samplingMediaNames"
          :value="valueSamplingMediaName"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('samplingMediaName', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
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
          label="Measuring range min"
          :value="value.measuringRange.min"
          :readonly="readonly"
          :disabled="readonly"
          type="number"
          @input="update('measuringRange.min', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          label="Measuring range max"
          :value="value.measuringRange.max"
          :readonly="readonly"
          :disabled="readonly"
          type="number"
          @input="update('measuringRange.max', $event)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <v-text-field
          label="Accuracy"
          :value="value.accuracy"
          :readonly="readonly"
          :disabled="readonly"
          type="number"
          @input="update('accuracy', $event)"
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-text-field
          label="Failure value"
          :value="value.failureValue"
          :readonly="readonly"
          :disabled="readonly"
          type="number"
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

import { Compartment } from '@/models/Compartment'
import { Property } from '@/models/Property'
import { SamplingMedia } from '@/models/SamplingMedia'
import { Unit } from '@/models/Unit'
import { DeviceProperty } from '@/models/DeviceProperty'
import { parseFloatOrNull } from '@/utils/numericsHelper'

interface INameAndUri {
  name: string
  uri: string
}

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
  readonly value!: DeviceProperty

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

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

    const getUriValue = (name: string, value: string) => {
      let valueToSet = ''

      const elementsByName: { [name: string]: { elements: INameAndUri[] } } = {
        compartmentName: {
          elements: this.compartments
        },
        unitName: {
          elements: this.units
        },
        samplingMediaName: {
          elements: this.samplingMedias
        },
        propertyName: {
          elements: this.properties
        }
      }
      if (!elementsByName[name]) {
        return valueToSet
      }
      // the comoboboxes may set the value to null,
      // but we don't want to work further with nulls
      //
      // all of the comboboxes see the empty string as the
      // "no value" choice
      if (value === null) {
        value = ''
      }
      const index = elementsByName[name].elements.findIndex(x => x.name === value)
      if (index > -1) {
        valueToSet = elementsByName[name].elements[index].uri
      }
      return valueToSet
    }

    switch (key) {
      case 'label':
        newObj.label = value
        break
      case 'compartmentName':
        newObj.compartmentName = value
        newObj.compartmentUri = getUriValue('compartmentName', value)
        break
      case 'unitName':
        newObj.unitName = value
        newObj.unitUri = getUriValue('unitName', value)
        break
      case 'samplingMediaName':
        newObj.samplingMediaName = value
        newObj.samplingMediaUri = getUriValue('samplingMediaName', value)
        break
      case 'propertyName':
        newObj.propertyName = value
        newObj.propertyUri = getUriValue('propertyName', value)
        break
      case 'measuringRange.min':
        newObj.measuringRange.min = parseFloatOrNull(value)
        break
      case 'measuringRange.max':
        newObj.measuringRange.max = parseFloatOrNull(value)
        break
      case 'accuracy':
        newObj.accuracy = parseFloatOrNull(value)
        break
      case 'failureValue':
        newObj.failureValue = parseFloatOrNull(value)
        break
      default:
        throw new TypeError('key ' + key + ' is not valid')
    }

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
    const compartmentIndex = this.compartments.findIndex(c => c.uri === this.value.compartmentUri)
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
