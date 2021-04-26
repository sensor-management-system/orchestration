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
  <v-card
    class="mb-2"
  >
    <v-card-text>
      <v-row
        dense
      >
        <v-col
          cols="12"
          md="2"
        >
          <v-text-field
            ref="keyfield"
            label="Key"
            :value="value.key"
            required
            class="required"
            :rules="[rules.required]"
            @input="update('key', $event)"
          />
        </v-col>
        <v-col
          cols="12"
          md="8"
        >
          <v-text-field
            label="Value"
            :value="value.value"
            @input="update('value', $event)"
          />
        </v-col>
        <v-col
          cols="12"
          md="2"
          class="text-right"
          align-self="center"
        >
          <slot name="actions" />
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
/**
 * @file provides a component for a custom field which consists of an key and a value
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Component, Prop, mixins } from 'nuxt-property-decorator'

import { Rules } from '@/mixins/Rules'

import { CustomTextField } from '@/models/CustomTextField'

/**
 * A class component for a custom field
 * @extends Vue
 */
@Component
// @ts-ignore
export default class CustomFieldCardForm extends mixins(Rules) {
  /**
   * a CustomTextField
   */
  @Prop({
    default: () => new CustomTextField(),
    required: true,
    type: CustomTextField
  })
  // @ts-ignore
  readonly value!: CustomTextField

  /**
   * updates a copy of the internal model at a given key and triggers an input event
   *
   * @param {string} key - a path to the property to set
   * @param {string} value - the value to set
   * @fires CustomFieldForm#input
   */
  update (key: string, value: string) {
    const newObj: CustomTextField = CustomTextField.createFromObject(this.value)

    switch (key) {
      case 'key':
        newObj.key = value
        break
      case 'value':
        newObj.value = value
        break
      default:
        throw new TypeError('key ' + key + ' is not valid')
    }

    /**
     * input event
     * @event CustomTextFieldForm#input
     * @type {CustomTextField}
     */
    this.$emit('input', newObj)
  }

  focus (): void {
    (this.$refs.keyfield as Vue & { focus: () => void }).focus()
  }
}
</script>
