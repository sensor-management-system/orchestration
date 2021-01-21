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
    <p>
      {{ value.compartmentName }}
      {{ value.compartmentUri }}
    </p>
    <v-row>
      <v-col cols="12" md="3">
        <v-combobox
          label="Measured Quantity"
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
          @wheel.prevent
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
          @wheel.prevent
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
          @wheel.prevent
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
          @wheel.prevent
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="3">
        <v-text-field
          label="Resolution"
          :value="value.resolution"
          :readonly="readonly"
          :disabled="readonly"
          type="number"
          @input="update('resolution', $event)"
          @wheel.prevent
        />
      </v-col>
      <v-col cols="12" md="3">
        <v-combobox
          label="Unit of Resolution"
          :items="unitNames"
          :value="valueResolutionUnitName"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('resolutionUnitName', $event)"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component that renders a form for a device property
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
 * A class component that renders a form for a device property
 * @extends Vue
 */
@Component
// @ts-ignore
export default class DevicePropertyForm extends Vue {
  /**
   * a DeviceProperty
   */
  @Prop({
    default: () => new DeviceProperty(),
    required: true,
    type: DeviceProperty
  })
  // @ts-ignore
  readonly value!: DeviceProperty

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
   * a list of Compartments
   */
  @Prop({
    default: () => [] as Compartment[],
    required: true,
    type: Array
  })
  compartments!: Compartment[]

  /**
   * a list of SamplingMedias
   */
  @Prop({
    default: () => [] as SamplingMedia[],
    required: true,
    type: Array
  })
  samplingMedias!: SamplingMedia[]

  /**
   * a list of Properties
   */
  @Prop({
    default: () => [] as Property[],
    required: true,
    type: Array
  })
  properties!: Property[]

  /**
   * a list of Units
   */
  @Prop({
    default: () => [] as Unit[],
    required: true,
    type: Array
  })
  units!: Unit[]

  /**
   * update a copy of the internal model at a given key and trigger an event
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
      case 'resolution':
        newObj.resolution = parseFloatOrNull(value)
        break
      case 'resolutionUnitName':
        newObj.resolutionUnitName = value
        newObj.resolutionUnitUri = getUriValue('unitName', value)
        break
      default:
        throw new TypeError('key ' + key + ' is not valid')
    }

    /**
     * input event
     * @event DevicePropertyForm#input
     * @type {DeviceProperty}
     */
    this.$emit('input', newObj)
  }

  /**
   * return a list of compartment names
   *
   * @return {string[]} list of compartment names
   */
  get compartmentNames () : string[] {
    return this.compartments.map(c => c.name)
  }

  /**
   * returns the name of a compartment based on the compartment URI
   *
   * @return {string} the name of the compartment
   */
  get valueCompartmentName (): string {
    const compartmentIndex = this.compartments.findIndex(c => c.uri === this.value.compartmentUri)
    if (compartmentIndex > -1) {
      return this.compartments[compartmentIndex].name
    }
    return this.value.compartmentName
  }

  /**
   * returns a list of unit names
   *
   * @return {string[]} list of unit names
   */
  get unitNames (): string[] {
    return this.units.map(u => u.name)
  }

  /**
   * returns the name of a unit based on the unit URI
   *
   * @return {string} the name of the unit
   */
  get valueUnitName (): string {
    const unitIndex = this.units.findIndex(u => u.uri === this.value.unitUri)
    if (unitIndex > -1) {
      return this.units[unitIndex].name
    }
    return this.value.unitName
  }

  /**
   * returns the name of a unit based on the unit URI
   *
   * @return {string} the name of the unit
   */
  get valueResolutionUnitName (): string {
    const unitIndex = this.units.findIndex(u => u.uri === this.value.resolutionUnitUri)
    if (unitIndex > -1) {
      return this.units[unitIndex].name
    }
    return this.value.resolutionUnitName
  }

  /**
   * returns a list of samplingMedia names
   *
   * @return {string[]} list of samplingMedia names
   */
  get samplingMediaNames (): string[] {
    return this.samplingMedias.map(s => s.name)
  }

  /**
   * returns the name of a samplingMedia based on the samplingMedia URI
   *
   * @return {string} the name of the samplingMedia
   */
  get valueSamplingMediaName (): string {
    const samplingMediaIndex = this.samplingMedias.findIndex(s => s.uri === this.value.samplingMediaUri)
    if (samplingMediaIndex > -1) {
      return this.samplingMedias[samplingMediaIndex].name
    }
    return this.value.samplingMediaName
  }

  /**
   * returns a list of property names
   *
   * @return {string[]} list of property names
   */
  get propertyNames (): string[] {
    return this.properties.map(p => p.name)
  }

  /**
   * returns the name of a property based on the property URI
   *
   * @return {string} the name of the property
   */
  get valuePropertyName (): string {
    const propertyIndex = this.properties.findIndex(p => p.uri === this.value.propertyUri)
    if (propertyIndex > -1) {
      return this.properties[propertyIndex].name
    }
    return this.value.propertyName
  }
}
</script>
