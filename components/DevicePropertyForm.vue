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
    <v-form
      ref="propertyForm"
      @submit.prevent
    >
      <v-row>
        <v-col cols="12" md="3">
          <v-text-field
            ref="label"
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
            clearable
            :items="compartmentItems"
            item-name="name"
            :value="valueCompartmentItem"
            :readonly="readonly"
            :disabled="readonly"
            @input="updateCompartment"
          >
            <template #append-outer>
              <v-tooltip
                v-if="itemHasDefinition(valueCompartmentItem)"
                right
              >
                <template #activator="{ on, attrs }">
                  <v-icon
                    color="primary"
                    small
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-help-circle-outline
                  </v-icon>
                </template>
                <span>{{ valueCompartmentItem.definition }}</span>
              </v-tooltip>
            </template>
            <template #item="data">
              <template v-if="(typeof data.item) !== 'object'">
                <v-list-item-content>{{ data.item }}</v-list-item-content>
              </template>
              <template v-else>
                <v-list-item-content>
                  <v-list-item-title>
                    {{ data.item.name }}
                    <v-tooltip
                      v-if="data.item.definition"
                      bottom
                    >
                      <template #activator="{ on, attrs }">
                        <v-icon
                          color="primary"
                          small
                          v-bind="attrs"
                          v-on="on"
                        >
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>{{ data.item.definition }}</span>
                    </v-tooltip>
                  </v-list-item-title>
                </v-list-item-content>
              </template>
            </template>
          </v-combobox>
        </v-col>
        <v-col cols="12" md="3">
          <v-combobox
            label="Sampling media"
            clearable
            :items="samplingMediaItems"
            item-text="name"
            :value="valueSamplingMediaItem"
            :readonly="readonly"
            :disabled="readonly"
            @input="updateSamplingMedia"
          >
            <template #append-outer>
              <v-tooltip
                v-if="itemHasDefinition(valueSamplingMediaItem)"
                right
              >
                <template #activator="{ on, attrs }">
                  <v-icon
                    color="primary"
                    small
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-help-circle-outline
                  </v-icon>
                </template>
                <span>{{ valueSamplingMediaItem.definition }}</span>
              </v-tooltip>
            </template>
            <template #item="data">
              <template v-if="(typeof data.item) !== 'object'">
                <v-list-item-content>{{ data.item }}</v-list-item-content>
              </template>
              <template v-else>
                <v-list-item-content>
                  <v-list-item-title>
                    {{ data.item.name }}
                    <v-tooltip
                      v-if="data.item.definition"
                      bottom
                    >
                      <template #activator="{ on, attrs }">
                        <v-icon
                          color="primary"
                          small
                          v-bind="attrs"
                          v-on="on"
                        >
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>{{ data.item.definition }}</span>
                    </v-tooltip>
                  </v-list-item-title>
                </v-list-item-content>
              </template>
            </template>
          </v-combobox>
        </v-col>
        <v-col cols="12" md="3">
          <v-combobox
            label="Measured Quantity"
            class="required"
            :rules="[rules.required]"
            clearable
            :items="propertyItems"
            item-text="name"
            :value="valuePropertyItem"
            :readonly="readonly"
            :disabled="readonly"
            @input="updateProperty"
            @change="onMeasuredQuantityChanged"
          >
            <template #append-outer>
              <v-tooltip
                v-if="itemHasDefinition(valuePropertyItem)"
                right
              >
                <template #activator="{ on, attrs }">
                  <v-icon
                    color="primary"
                    small
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-help-circle-outline
                  </v-icon>
                </template>
                <span>{{ valuePropertyItem.definition }}</span>
              </v-tooltip>
            </template>
            <template #item="data">
              <template v-if="(typeof data.item) !== 'object'">
                <v-list-item-content>{{ data.item }}</v-list-item-content>
              </template>
              <template v-else>
                <v-list-item-content>
                  <v-list-item-title>
                    {{ data.item.name }}
                    <v-tooltip
                      v-if="data.item.definition"
                      bottom
                    >
                      <template #activator="{ on, attrs }">
                        <v-icon
                          color="primary"
                          small
                          v-bind="attrs"
                          v-on="on"
                        >
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>{{ data.item.definition }}</span>
                    </v-tooltip>
                  </v-list-item-title>
                </v-list-item-content>
              </template>
            </template>
          </v-combobox>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="3">
          <v-combobox
            label="Unit"
            clearable
            :items="measuredQuantityUnitItems"
            item-text="name"
            :value="valueUnitItem"
            :readonly="readonly"
            :disabled="readonly"
            @input="updateUnit"
            @change="onMeasuredQuantityChanged"
          >
            <template #append-outer>
              <v-tooltip
                v-if="itemHasDefinition(valueUnitItem)"
                right
              >
                <template #activator="{ on, attrs }">
                  <v-icon
                    color="primary"
                    small
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-help-circle-outline
                  </v-icon>
                </template>
                <span>{{ valueUnitItem.definition }}</span>
              </v-tooltip>
            </template>
            <template #item="data">
              <template v-if="(typeof data.item) !== 'object'">
                <v-list-item-content>{{ data.item }}</v-list-item-content>
              </template>
              <template v-else>
                <v-list-item-content>
                  <v-list-item-title>
                    {{ data.item.name }}
                    <v-tooltip
                      v-if="data.item.definition"
                      bottom
                    >
                      <template #activator="{ on, attrs }">
                        <v-icon
                          color="primary"
                          small
                          v-bind="attrs"
                          v-on="on"
                        >
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>{{ data.item.definition }}</span>
                    </v-tooltip>
                  </v-list-item-title>
                </v-list-item-content>
              </template>
            </template>
          </v-combobox>
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field
            label="Measuring range min"
            :value="value.measuringRange.min"
            :readonly="readonly"
            :disabled="readonly"
            type="number"
            step="any"
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
            step="any"
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
            step="any"
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
            step="any"
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
            step="any"
            @input="update('resolution', $event)"
            @wheel.prevent
          />
        </v-col>
        <v-col cols="12" md="3">
          <v-combobox
            label="Unit of Resolution"
            :items="unitItems"
            item-text="name"
            :value="valueResolutionUnitItem"
            :readonly="readonly"
            :disabled="readonly"
            @input="updateResolutionUnit"
          >
            <template #append-outer>
              <v-tooltip
                v-if="itemHasDefinition(valueResolutionUnitItem)"
                right
              >
                <template #activator="{ on, attrs }">
                  <v-icon
                    color="primary"
                    small
                    v-bind="attrs"
                    v-on="on"
                  >
                    mdi-help-circle-outline
                  </v-icon>
                </template>
                <span>{{ valueResolutionUnitItem.definition }}</span>
              </v-tooltip>
            </template>
            <template #item="data">
              <template v-if="(typeof data.item) !== 'object'">
                <v-list-item-content>{{ data.item }}</v-list-item-content>
              </template>
              <template v-else>
                <v-list-item-content>
                  <v-list-item-title>
                    {{ data.item.name }}
                    <v-tooltip
                      v-if="data.item.definition"
                      bottom
                    >
                      <template #activator="{ on, attrs }">
                        <v-icon
                          color="primary"
                          small
                          v-bind="attrs"
                          v-on="on"
                        >
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>{{ data.item.definition }}</span>
                    </v-tooltip>
                  </v-list-item-title>
                </v-list-item-content>
              </template>
            </template>
          </v-combobox>
        </v-col>
      </v-row>
    </v-form>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component that renders a form for a device property
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop, mixins } from 'nuxt-property-decorator'

import { Compartment } from '@/models/Compartment'
import { Property } from '@/models/Property'
import { SamplingMedia } from '@/models/SamplingMedia'
import { Unit } from '@/models/Unit'
import { MeasuredQuantityUnit } from '@/models/MeasuredQuantityUnit'
import { DeviceProperty } from '@/models/DeviceProperty'
import { ICvSelectItem, hasDefinition } from '@/models/CvSelectItem'

import { parseFloatOrNull } from '@/utils/numericsHelper'

import { Rules } from '@/mixins/Rules'

interface INameAndUri {
  name: string
  uri: string
}

type CompartmentComboboxValue = Compartment | string | undefined
type SamplingMediaComboboxValue = SamplingMedia | string | undefined
type PropertyComboboxValue = Property | string | undefined
type UnitComboboxValue = MeasuredQuantityUnit | string | undefined

/**
 * A class component that renders a form for a device property
 * @extends Vue
 */
@Component
export default class DevicePropertyForm extends mixins(Rules) {
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
  readonly compartments!: Compartment[]

  /**
   * a list of SamplingMedias
   */
  @Prop({
    default: () => [] as SamplingMedia[],
    required: true,
    type: Array
  })
  readonly samplingMedias!: SamplingMedia[]

  /**
   * a list of Properties
   */
  @Prop({
    default: () => [] as Property[],
    required: true,
    type: Array
  })
  readonly properties!: Property[]

  /**
   * a list of Units
   */
  @Prop({
    default: () => [] as Unit[],
    required: true,
    type: Array
  })
  readonly units!: Unit[]

  /**
   * a list of MeasuredQuantityUnits
   */
  @Prop({
    default: () => [] as MeasuredQuantityUnit[],
    required: true,
    type: Array
  })
  readonly measuredQuantityUnits!: MeasuredQuantityUnit[]

  onMeasuredQuantityChanged () {
    if (!this.isNewPropertyPage) {
      this.$store.commit('snackbar/setWarning', 'Warning! Changes are time-independent and affect the entire history of the device and configurations. ')
    }
  }

  get deviceId () {
    return this.$route.params.deviceId
  }

  get isNewPropertyPage (): boolean {
    return this.$route.path === '/devices/' + this.deviceId + '/measuredquantities/new'
  }

  /**
   * returns the URI of an value
   *
   * @param {string} name - the name of the dictionary to look in
   * @param {string} value - the value to look the URI for
   * @returns {string} the URI or an empty string
   */
  private getUriByValue (name: string, value: string): string {
    let valueToSet = ''

    const elementsByName: { [name: string]: { elements: INameAndUri[] } } = {
      compartmentName: {
        elements: this.compartments
      },
      unitName: {
        elements: this.units
      },
      measuredQuantityUnitName: {
        elements: this.measuredQuantityUnits
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

  /**
   * updates the compartment
   *
   * @param {CompartmentComboboxValue} value - an object as provided by the combobox
   * @fires DevicePropertyForm#input
   */
  updateCompartment (value: CompartmentComboboxValue): void {
    const newObj: DeviceProperty = DeviceProperty.createFromObject(this.value)

    if (value) {
      if (typeof value === 'string') {
        newObj.compartmentName = value
        newObj.compartmentUri = this.getUriByValue('compartmentName', value)
      } else {
        newObj.compartmentName = value.name
        newObj.compartmentUri = value.uri
      }
    } else {
      newObj.compartmentName = ''
      newObj.compartmentUri = ''
    }
    if (this.value.compartmentUri !== newObj.compartmentUri) {
      newObj.samplingMediaName = ''
      newObj.samplingMediaUri = ''
      newObj.propertyName = ''
      newObj.propertyUri = ''
      newObj.unitName = ''
      newObj.unitUri = ''
    }
    /**
     * input event
     * @event DevicePropertyForm#input
     * @type {DeviceProperty}
     */
    this.$emit('input', newObj)
  }

  /**
   * updates the sampling media
   *
   * @param {SamplingMediaComboboxValue} value - an object as provided by the combobox
   * @fires DevicePropertyForm#input
   */
  updateSamplingMedia (value: SamplingMediaComboboxValue): void {
    const newObj: DeviceProperty = DeviceProperty.createFromObject(this.value)

    if (value) {
      if (typeof value === 'string') {
        newObj.samplingMediaName = value
        newObj.samplingMediaUri = this.getUriByValue('samplingMediaName', value)
      } else {
        newObj.samplingMediaName = value.name
        newObj.samplingMediaUri = value.uri
      }
    } else {
      newObj.samplingMediaName = ''
      newObj.samplingMediaUri = ''
    }
    if (this.value.samplingMediaUri !== newObj.samplingMediaUri) {
    // ok, we also want to update the compartment here
      const samplineMediaIndex = this.samplingMedias.findIndex(s => s.uri === newObj.samplingMediaUri)
      if (samplineMediaIndex > -1) {
        const samplingMediaItem = this.samplingMedias[samplineMediaIndex]
        const compartmentId = samplingMediaItem.compartmentId
        const compartmentIndex = this.compartmentItems.findIndex(c => c.id === compartmentId)
        if (compartmentIndex > -1) {
          const compartmentItem = this.compartmentItems[compartmentIndex]
          if (compartmentItem.uri !== newObj.compartmentUri || compartmentItem.name !== newObj.compartmentName) {
            newObj.compartmentUri = compartmentItem.uri
            newObj.compartmentName = compartmentItem.name
          }
        }
      }
      newObj.propertyName = ''
      newObj.propertyUri = ''
      newObj.unitName = ''
      newObj.unitUri = ''
    }
    /**
     * input event
     * @event DevicePropertyForm#input
     * @type {DeviceProperty}
     */
    this.$emit('input', newObj)
  }

  /**
   * updates the property (measured quantity)
   *
   * @param {PropertyComboboxValue} value - an object as provided by the combobox
   * @fires DevicePropertyForm#input
   */
  updateProperty (value: PropertyComboboxValue): void {
    const newObj: DeviceProperty = DeviceProperty.createFromObject(this.value)

    if (value) {
      if (typeof value === 'string') {
        newObj.propertyName = value
        newObj.propertyUri = this.getUriByValue('propertyName', value)
      } else {
        newObj.propertyName = value.name
        newObj.propertyUri = value.uri
      }
    } else {
      newObj.propertyName = ''
      newObj.propertyUri = ''
    }
    if (this.value.propertyUri !== newObj.propertyUri) {
    // and here we want to check both the sampling media & the compartment
      const propertyIndex = this.properties.findIndex(p => p.uri === newObj.propertyUri)
      if (propertyIndex > -1) {
        const propertyItem = this.properties[propertyIndex]
        const samplineMediaId = propertyItem.samplingMediaId
        const samplineMediaIndex = this.samplingMedias.findIndex(s => s.id === samplineMediaId)
        if (samplineMediaIndex > -1) {
          const samplingMediaItem = this.samplingMedias[samplineMediaIndex]
          if (samplingMediaItem.uri !== newObj.samplingMediaUri || samplingMediaItem.name !== newObj.samplingMediaName) {
            newObj.samplingMediaUri = samplingMediaItem.uri
            newObj.samplingMediaName = samplingMediaItem.name
            const compartmentId = samplingMediaItem.compartmentId
            const compartmentIndex = this.compartmentItems.findIndex(c => c.id === compartmentId)
            if (compartmentIndex > -1) {
              const compartmentItem = this.compartmentItems[compartmentIndex]
              if (compartmentItem.uri !== newObj.compartmentUri || compartmentItem.name !== newObj.compartmentName) {
                newObj.compartmentUri = compartmentItem.uri
                newObj.compartmentName = compartmentItem.name
              }
            }
          }
        }
      }
      newObj.unitName = ''
      newObj.unitUri = ''
    }
    /**
     * input event
     * @event DevicePropertyForm#input
     * @type {DeviceProperty}
     */
    this.$emit('input', newObj)
  }

  /**
   * updates the unit
   *
   * Note: although we display a list of measuredQuantityUnits, the actual URI
   * to be saved is the URI of the original unit
   *
   * @param {UnitComboboxValue} value - an object as provided by the combobox
   * @fires DevicePropertyForm#input
   */
  updateUnit (value: UnitComboboxValue): void {
    const newObj: DeviceProperty = DeviceProperty.createFromObject(this.value)

    if (value) {
      if (typeof value === 'string') {
        newObj.unitName = value
        newObj.unitUri = this.getUriByValue('unitName', value)
      } else {
        newObj.unitName = value.name
        newObj.unitUri = this.getUriByValue('unitName', value.name)
        // if the unit has numerical default values, apply them to measuringRange min and max
        if (value.defaultLimitMin !== null) {
          newObj.measuringRange.min = parseFloatOrNull(value.defaultLimitMin)
        } else {
          newObj.measuringRange.min = null
        }
        if (value.defaultLimitMax !== null) {
          newObj.measuringRange.max = parseFloatOrNull(value.defaultLimitMax)
        } else {
          newObj.measuringRange.max = null
        }
      }
    } else {
      newObj.unitName = ''
      newObj.unitUri = ''
      newObj.measuringRange.min = null
      newObj.measuringRange.max = null
    }
    /**
     * input event
     * @event DevicePropertyForm#input
     * @type {DeviceProperty}
     */
    this.$emit('input', newObj)
  }

  /**
   * updates the resolutionUnit
   *
   * @param {UnitComboboxValue} value - an object as provided by the combobox
   * @fires DevicePropertyForm#input
   */
  updateResolutionUnit (value: UnitComboboxValue): void {
    const newObj: DeviceProperty = DeviceProperty.createFromObject(this.value)

    if (value) {
      if (typeof value === 'string') {
        newObj.resolutionUnitName = value
        newObj.resolutionUnitUri = this.getUriByValue('unitName', value)
      } else {
        newObj.resolutionUnitName = value.name
        newObj.resolutionUnitUri = value.uri
      }
    } else {
      newObj.resolutionUnitName = ''
      newObj.resolutionUnitUri = ''
    }
    /**
     * input event
     * @event DevicePropertyForm#input
     * @type {DeviceProperty}
     */
    this.$emit('input', newObj)
  }

  /**
   * update a copy of the internal model at a given key and trigger an event
   *
   * @param {string} key - a path to the property to set
   * @param {string} value - the value to set
   * @fires DevicePropertyForm#input
   */
  update (key: string, value: string) {
    const newObj: DeviceProperty = DeviceProperty.createFromObject(this.value)

    switch (key) {
      case 'label':
        newObj.label = value
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
   * return a list of compartments
   *
   * @returns {Compartment[]} list of compartments
   */
  get compartmentItems (): Compartment[] {
    return this.compartments
  }

  /**
   * returns an item to be used as the value of a combobox
   *
   * Checks whether value.propertyName and value.propertyUri can be found in
   * the list of CV properties. Returns the found property, otherwise
   * constructs one from the name and the uri. Returns null if both fields are
   * empty.
   *
   * @returns {ICvSelectItem|null} the property, a constructed one or null
   */
  get valueCompartmentItem (): ICvSelectItem | null {
    if (!this.value.compartmentName && !this.value.compartmentUri) {
      return null
    }
    const compartment = this.compartments.find(c => c.uri === this.value.compartmentUri)
    if (compartment) {
      return compartment
    }
    return {
      name: this.value.compartmentName,
      uri: this.value.compartmentUri,
      definition: ''
    }
  }

  /**
   * returns a list of sampling medias
   *
   * When the compartment exists, restricts the list of sampling medias to
   * those that have a relation to the selected compartment
   *
   * @returns {SamplingMedia[]} list of samplingMedia names
   */
  get samplingMediaItems (): SamplingMedia[] {
    let samplingMedias = this.samplingMedias
    // if a compartment is choosen, restrict the list of samplingMedias
    if (this.value.compartmentUri !== '') {
      samplingMedias = samplingMedias.filter(s => s.compartmentId === '' || this.checkUriEndsWithId(this.value.compartmentUri, s.compartmentId))
    }
    return samplingMedias
  }

  /**
   * returns an item to be used as the value of a combobox
   *
   * Checks whether value.propertyName and value.propertyUri can be found in
   * the list of CV properties. Returns the found property, otherwise
   * constructs one from the name and the uri. Returns null if both fields are
   * empty.
   *
   * @returns {ICvSelectItem|null} the property, a constructed one or null
   */
  get valueSamplingMediaItem (): ICvSelectItem | null {
    if (!this.value.samplingMediaName && !this.value.samplingMediaUri) {
      return null
    }
    const samplingMedia = this.samplingMedias.find(m => m.uri === this.value.samplingMediaUri)
    if (samplingMedia) {
      return samplingMedia
    }
    return {
      name: this.value.samplingMediaName,
      uri: this.value.samplingMediaUri,
      definition: ''
    }
  }

  /**
   * returns a list of properties
   *
   * When the samplingMedia exists, restricts the list of properties to those
   * that have a relation to the selected samplingMedia
   *
   * @returns {Property[]} list of properties
   */
  get propertyItems (): Property[] {
    let properties = this.properties
    // if a samplingMedia is choosen, restrict the list of properties
    if (this.value.samplingMediaUri !== '') {
      properties = properties.filter(p => p.samplingMediaId === '' || this.checkUriEndsWithId(this.value.samplingMediaUri, p.samplingMediaId))
    } else if (this.value.compartmentUri !== '') {
    // in case we have only a compartment, then we also just want
    // to select those properties that are hierachically
    // within the compartment
    // In case that we have the compartment, then the
    // getter for the samlingMediaItems is already pre-filtered
      const samplingMediaItems = this.samplingMediaItems
      const samplingMediaIds = new Set<string>()
      for (const sm of samplingMediaItems) {
        samplingMediaIds.add(sm.id)
      }
      properties = properties.filter(p => p.samplingMediaId === '' || samplingMediaIds.has(p.samplingMediaId))
    }
    return properties
  }

  /**
   * returns an item to be used as the value of a combobox
   *
   * Checks whether value.propertyName and value.propertyUri can be found in
   * the list of CV properties. Returns the found property, otherwise
   * constructs one from the name and the uri. Returns null if both fields are
   * empty.
   *
   * @returns {ICvSelectItem|null} the property, a constructed one or null
   */
  get valuePropertyItem (): ICvSelectItem | null {
    if (!this.value.propertyName && !this.value.propertyUri) {
      return null
    }
    const property = this.properties.find(p => p.uri === this.value.propertyUri)
    if (property) {
      return property
    }
    return {
      name: this.value.propertyName,
      uri: this.value.propertyUri,
      definition: ''
    }
  }

  /**
   * returns a list of unit objects
   *
   * @returns {Unit[]} list of units
   */
  get unitItems (): Unit[] {
  // restrict the list of measuredQuantityUnits based on the choosen property
    return this.units
  }

  /**
   * returns a list of unit objects
   *
   * When the property exists, restricts the list of units to those that have a
   * relation to the selected property
   *
   * @returns {MeasuredQuantityUnit[]} list of units
   */
  get measuredQuantityUnitItems (): MeasuredQuantityUnit[] {
  // restrict the list of measuredQuantityUnits based on the choosen property
    return this.measuredQuantityUnits.filter(u => this.checkUriEndsWithId(this.value.propertyUri, u.measuredQuantityId))
  }

  /**
   * returns an item to be used as the value of a combobox
   *
   * Checks whether value.unitName and value.unitUri can be found in the list
   * of CV units. Returns the found unit, otherwise constructs one from the
   * name and the uri. Returns null if both fields are empty.
   *
   * @returns {ICvSelectItem|null} the unit, a constructed one or null
   */
  get valueUnitItem (): ICvSelectItem | null {
    if (!this.value.unitName && !this.value.unitUri) {
      return null
    }
    const unit = this.units.find(u => u.uri === this.value.unitUri)
    if (unit) {
      return unit
    }
    return {
      name: this.value.unitName,
      uri: this.value.unitUri,
      definition: ''
    }
  }

  /**
   * returns an item to be used as the value of a combobox
   *
   * Checks whether value.resolutionUnitName and value.resolutionUnitUri can be
   * found in the list of CV units. Returns the found unit, otherwise
   * constructs one from the name and the uri. Returns null if both fields are
   * empty.
   *
   * @returns {ICvSelectItem|null} the unit, a constructed one or null
   */
  get valueResolutionUnitItem (): ICvSelectItem | null {
    if (!this.value.resolutionUnitName && !this.value.resolutionUnitUri) {
      return null
    }
    const unit = this.units.find(u => u.uri === this.value.resolutionUnitUri)
    if (unit) {
      return unit
    }
    return {
      name: this.value.resolutionUnitName,
      uri: this.value.resolutionUnitUri,
      definition: ''
    }
  }

  /**
   * checks if an URI ends with a specific id
   *
   * @param {string} uri - the URI to check the id for
   * @param {string} id - the id
   * @returns {boolean} returns true when the id was found, otherwise false
   */
  private checkUriEndsWithId (uri: string, id: string): boolean {
    return uri.match(new RegExp('^.+/' + id + '/?$')) !== null
  }

  /**
   * checks wheter the item has a non-empty definition property
   *
   * @param {ICvSelectItem} item - the item to check for
   * @returns {boolean} returns true when the definition property exists and is not falsy
   */
  itemHasDefinition (item: ICvSelectItem): boolean {
    return hasDefinition(item)
  }

  focus (): void {
    (this.$refs.label as Vue & { focus: () => void }).focus()
  }

  /**
   * validates the user input
   *
   * Note: we can't use 'validate' as a method name, so I used 'validateForm'
   *
   * @return {boolean} true when input is valid, otherwise false
   */
  public validateForm (): boolean {
    return (this.$refs.propertyForm as Vue & { validate: () => boolean }).validate()
  }
}
</script>
<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>
