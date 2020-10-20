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
  <v-form ref="customFieldsForm">
    <v-btn
      v-if="!readonly"
      small
      color="primary"
      data-role="add-field"
      @click="addField"
    >
      add Custom Field
    </v-btn>
    <br><br>
    <template
      v-for="(item, index) in value"
    >
      <v-card
        :key="'customfield-' + index"
      >
        <v-card-text>
          <CustomFieldForm
            v-model="value[index]"
            :readonly="readonly"
          >
            <template v-slot:actions>
              <v-btn
                v-if="!readonly"
                icon
                color="error"
                data-role="delete-field"
                @click="removeField(index)"
              >
                <v-icon>
                  mdi-delete
                </v-icon>
              </v-btn>
            </template>
          </CustomFieldForm>
        </v-card-text>
      </v-card>
      <br
        :key="'br-' + index"
      >
    </template>
  </v-form>
</template>

<script lang="ts">
/**
 * @file provides a component for collections of CustomFieldForms
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import CustomFieldForm from '@/components/CustomFieldForm.vue'

import { CustomTextField } from '@/models/CustomTextField'

/**
 * A class component that lists CustomFieldForms as Cards
 * @extends Vue
 */
@Component({
  components: { CustomFieldForm }
})
// @ts-ignore
export default class CustomFieldCards extends Vue {
  /**
   * a list of CustomTextFields
   */
  @Prop({
    default: () => [] as CustomTextField[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value!: CustomTextField[]

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
   * adds a new CustomTextField instance and triggers an event
   *
   * @fires CustomFieldCards#input
   */
  addField () {
    /**
     * fires an input event
     * @event CustomFieldCards#input
     * @type {CustomTextField[]}
     */
    this.$emit('input', [
      ...this.value,
      new CustomTextField()
    ] as CustomTextField[])
  }

  /**
   * removes a CustomTextField instance and triggers an event
   *
   * @param {CustomTextField} index - the index of the property to remove
   * @fires CustomFieldCards#input
   */
  removeField (index: number) {
    if (this.value[index]) {
      const properties = [...this.value] as CustomTextField[]
      properties.splice(index, 1)
      /**
      * Update event
      * @event CustomFieldCards#input
      * @type {CustomTextField[]}
      */
      this.$emit('input', properties)
    }
  }
}
</script>
