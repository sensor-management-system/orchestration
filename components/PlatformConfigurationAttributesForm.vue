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
  <v-row>
    <v-col
      cols="12"
      md="2"
    >
      <v-text-field
        :value="value.offsetX"
        label="Offset (x)"
        type="number"
        :readonly="readonly"
        :disabled="readonly"
        @change="update('offsetX', $event)"
      />
    </v-col>
    <v-col
      cols="12"
      md="2"
    >
      <v-text-field
        :value="value.offsetY"
        label="Offset (y)"
        type="number"
        :readonly="readonly"
        :disabled="readonly"
        @change="update('offsetY', $event)"
      />
    </v-col>
    <v-col
      cols="12"
      md="2"
    >
      <v-text-field
        :value="value.offsetZ"
        label="Offset (z)"
        type="number"
        :readonly="readonly"
        :disabled="readonly"
        @change="update('offsetZ', $event)"
      />
    </v-col>
  </v-row>
</template>

<script lang="ts">
/**
 * @file provides a component for platform configuration attributes
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { PlatformConfigurationAttributes } from '@/models/PlatformConfigurationAttributes'
import { parseFloatOrDefault } from '@/utils/numericsHelper'

/**
 * A class component for platform configuration attributes
 * @extends Vue
 */
@Component
// @ts-ignore
export default class PlatformConfigurationAttributesForm extends Vue {
  /**
   * the PlatformConfigurationAttributes
   */
  @Prop({
    required: true,
    type: PlatformConfigurationAttributes
  })
  // @ts-ignore
  readonly value!: PlatformConfigurationAttributes

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
   * update copy of the internal model at a given key and triggers an event
   *
   * @param {string} key - a path to the property to set
   * @param {any} value - the value to set
   * @fires PlatformConfigurationAttributesForm#input
   */
  update (key: string, value: any) {
    const newObj: PlatformConfigurationAttributes = PlatformConfigurationAttributes.createFromObject(this.value)

    switch (key) {
      case 'offsetX':
        newObj.offsetX = parseFloatOrDefault(value, 0)
        break
      case 'offsetY':
        newObj.offsetY = parseFloatOrDefault(value, 0)
        break
      case 'offsetZ':
        newObj.offsetZ = parseFloatOrDefault(value, 0)
        break
      default:
        throw new TypeError('key ' + key + ' is not valid')
    }

    /**
     * input event
     * @event PlatformConfigurationAttributes#input
     * @type {PlatformConfigurationAttributes}
     */
    this.$emit('input', newObj)
  }
}
</script>
