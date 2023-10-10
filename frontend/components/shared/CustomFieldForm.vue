<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020 - 2023
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
  <v-form
    ref="customFieldForm"
    @submit.prevent
  >
    <v-row>
      <v-col
        cols="12"
        md="3"
        align-self="center"
      >
        <v-text-field
          v-if="!keyEndpoint"
          label="Key"
          :value="value.key"
          :readonly="readonly"
          :disabled="readonly"
          required
          class="required"
          :rules="[rules.required]"
          @input="update('key', $event)"
        />
        <autocomplete-text-input
          v-else
          label="Key"
          :value="value.key"
          :readonly="readonly"
          :disabled="readonly"
          required
          class="required"
          :rules="[rules.required]"
          :endpoint="keyEndpoint"
          @input="update('key', $event)"
        />
      </v-col>
      <v-col
        cols="12"
        md="6"
      >
        <v-textarea
          v-if="!valueEndpoint"
          label="Value"
          auto-grow
          rows="1"
          :value="value.value"
          :readonly="readonly"
          :disabled="readonly"
          @input="update('value', $event)"
        />
        <autocomplete-text-input
          v-else
          label="Value"
          auto-grow
          rows="1"
          :value="value.value"
          :readonly="readonly"
          :disabled="readonly"
          :endpoint="valueEndpoint"
          @input="update('value', $event)"
        />
      </v-col>
      <v-col
        cols="12"
        md="2"
        align-self="center"
        class="text-right"
      >
        <slot name="actions" />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="9">
        <v-textarea
          :value="value.description"
          :readonly="readonly"
          :disabled="readonly"
          label="Description"
          rows="3"
          @input="update('description', $event)"
        />
      </v-col>
    </v-row>
  </v-form>
</template>

<script lang="ts">
/**
 * @file provides a component for a custom field which consists of an key and a value
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Component, Prop, mixins } from 'nuxt-property-decorator'

import { Rules } from '@/mixins/Rules'

import { CustomTextField } from '@/models/CustomTextField'
import AutocompleteTextInput from '@/components/shared/AutocompleteTextInput.vue'

/**
 * A class component for a custom field
 * @extends Vue
 */
@Component({
  components: {
    AutocompleteTextInput
  }
})
// @ts-ignore
export default class CustomFieldForm extends mixins(Rules) {
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
   * endpoint url for autocomplete API
   * Key field
   */
  @Prop({
    required: false,
    type: String
  })
  // @ts-ignore
  readonly keyEndpoint: string

  /**
   * endpoint url for autocomplete API
   * Value field
   */
  @Prop({
    required: false,
    type: String
  })
  // @ts-ignore
  readonly valueEndpoint: string

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
      case 'description':
        newObj.description = value
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

  /**
   * validates the user input
   *
   * Note: we can't use 'validate' as a method name, so I used 'validateForm'
   *
   * @return {boolean} true when input is valid, otherwise false
   */
  public validateForm (): boolean {
    return (this.$refs.customFieldForm as Vue & { validate: () => boolean }).validate()
  }
}
</script>
<style lang="scss">
@import "@/assets/styles/_forms.scss";
</style>
