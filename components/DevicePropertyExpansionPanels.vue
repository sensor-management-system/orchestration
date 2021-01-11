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
  <v-form ref="propertiesForm">
    <v-btn
      v-if="!readonly"
      small
      color="primary"
      data-role="add-property"
      @click="addProperty"
    >
      add Property
    </v-btn>
    <br><br>
    <v-expansion-panels
      v-model="openedPanels"
      multiple
    >
      <v-expansion-panel
        v-for="(item, index) in value"
        :key="index"
      >
        <v-expansion-panel-header>
          <v-row no-gutters>
            <v-col cols="11">
              Property {{ index+1 }} {{ item.label ? ' - ' + item.label : '' }}
            </v-col>
            <v-col
              cols="1"
              align-self="end"
              class="text-right"
            >
              <v-menu
                v-if="!readonly"
                right
                offset-y
              >
                <template v-slot:activator="{ on }">
                  <v-btn
                    data-role="property-menu"
                    icon
                    small
                    v-on="on"
                  >
                    <v-icon
                      dense
                      small
                    >
                      mdi-dots-vertical
                    </v-icon>
                  </v-btn>
                </template>

                <v-list
                  dense
                >
                  <v-list-item
                    data-role="copy-property"
                    @click="copyProperty(index)"
                  >
                    <v-list-item-title>
                      <v-icon
                        left
                        small
                      >
                        mdi-content-copy
                      </v-icon>
                      Copy
                    </v-list-item-title>
                  </v-list-item>
                  <v-list-item
                    dense
                    data-role="delete-property"
                    @click="removeProperty(index)"
                  >
                    <v-list-item-title
                      class="red--text"
                    >
                      <v-icon
                        left
                        small
                        color="red"
                      >
                        mdi-delete
                      </v-icon>
                      Delete
                    </v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
            </v-col>
          </v-row>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <DevicePropertyForm
            v-model="value[index]"
            :readonly="readonly"
            :compartments="compartments"
            :sampling-medias="samplingMedias"
            :properties="properties"
            :units="units"
          />
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-form>
</template>

<script lang="ts">
/**
 * @file provides a component for collections of DevicePropertyForms
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import DevicePropertyForm from '@/components/DevicePropertyForm.vue'

import { Compartment } from '@/models/Compartment'
import { Property } from '@/models/Property'
import { SamplingMedia } from '@/models/SamplingMedia'
import { Unit } from '@/models/Unit'
import { DeviceProperty } from '@/models/DeviceProperty'

/**
 * A class component that lists DevicePropertyForms as ExpansionPanels
 * @extends Vue
 */
@Component({
  components: { DevicePropertyForm }
})
// @ts-ignore
export default class DevicePropertyExpansionPanels extends Vue {
  private openedPanels: number[] = []

  /**
   * a list of DeviceProperty
   */
  @Prop({
    default: () => [] as DeviceProperty[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value!: DeviceProperty[]

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
   * adds a new DeviceProperty instance and triggers an input event
   *
   * @fires DevicePropertyExpansionPanels#input
   */
  addProperty () {
    /**
     * Update event
     * @event DevicePropertyExpansionPanels#input
     * @type {DeviceProperty[]}
     */
    this.$emit('input', [
      ...this.value,
      new DeviceProperty()
    ] as DeviceProperty[])

    this.openedPanels.push(this.value.length)
    // @TODO: scroll to new property with this.$vuetify.goTo()
  }

  /**
   * removes a DeviceProperty instance and triggers an input event
   *
   * @param {DeviceProperty} index - the index of the property to remove
   * @fires DevicePropertyExpansionPanels#input
   */
  removeProperty (index: number) {
    if (this.value[index]) {
      const properties = [...this.value] as DeviceProperty[]
      properties.splice(index, 1)
      /**
      * Update event
      * @event DevicePropertyExpansionPanels#input
      * @type {DeviceProperty[]}
      */
      this.$emit('input', properties)
    }
  }

  /**
   * copies a DeviceProperty instance and triggers an input event
   *
   * @param {DeviceProperty} index - the index of the property to copy
   * @fires DevicePropertyExpansionPanels#input
   */
  copyProperty (index: number) {
    if (this.value[index]) {
      const newProperty = DeviceProperty.createFromObject(this.value[index])
      newProperty.label += ' (copy)'

      /**
       * Update event
       * @event DevicePropertyExpansionPanels#input
       * @type {DeviceProperty[]}
       */
      this.$emit('input', [
        ...this.value,
        newProperty
      ] as DeviceProperty[])
    }
  }
}
</script>
