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
    <v-autocomplete
      v-if="!readonly"
      ref="autocompletefield"
      :items="allExceptSelected"
      :item-text="(x) => x"
      :item-value="(x) => x.id"
      :label="label"
      @change="add"
    />
    <v-chip
      v-for="element in value"
      :key="element.id"
      class="ma-2"
      :color="color"
      text-color="white"
      :close="!readonly"
      @click:close="remove(element.id)"
    >
      <v-avatar v-if="avatarIcon" left>
        <v-icon>
          {{ avatarIcon }}
        </v-icon>
      </v-avatar>
      {{ element }}
    </v-chip>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component to select entities
 * @author <marc.hanisch@gfz-potsdam.de>
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { IStringId } from '@/models/IStringId'

type EntityLoaderFunction<E> = () => Promise<E[]>

/**
 * A class component to select entities
 * @extends Vue
 */
@Component
// @ts-ignore
export default class EntitySelect<E extends IStringId> extends Vue {
  private elements: E[] = []

  @Prop({
    default: () => [] as E[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value!: E[]

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

  @Prop({
    required: true,
    type: Function
  })
  readonly fetchFunction!: EntityLoaderFunction<E>

  @Prop({
    required: true,
    type: String
  })
  // @ts-ignore
  readonly label!: string

  @Prop({
    default: () => '',
    type: String
  })
  readonly avatarIcon!: string

  @Prop({
    type: String,
    required: true
  })
  readonly color!: string

  /**
   * fetches all available elements
   *
   * @async
   */
  async fetch () {
    this.elements = await this.fetchFunction()
  }

  /**
   * adds an element to the value property
   *
   * @param {string} someId - the id of the element to add
   * @fires EntitySelect#input
   */
  add (someId: string) {
    const selectedElement: E | undefined = this.elements.find(e => e.id === someId)
    if (selectedElement) {
      /**
       * Update event
       * @event EntitySelect#input
       * @type E[]
       */
      this.$emit('input', [
        ...this.value,
        selectedElement
      ] as E[])
      this.clearInputField()
    }
  }

  clearInputField () {
    // the autocompletefield is an instance of this
    // https://github.com/vuetifyjs/vuetify/blob/master/packages/vuetify/src/components/VAutocomplete/VAutocomplete.ts
    // It is necessary as it doesn't work to use a v-model and set it to null
    // (as this just updates the chosen value but not the search string;
    // and working with the search string explicitly gives us trouble as well
    // as we then have problems to handle text inputs - it hangs on the input
    // field)
    // --> We use the clear callback of the autocomplete field
    const field: any = this.$refs.autocompletefield
    field.clearableCallback()
  }

  /**
   * removes an element from the value property
   *
   * @param {number} someId - the id of the element to remove
   * @fires EntitySelect#input
   */
  remove (someId: string) {
    const elementIndex: number = this.value.findIndex(e => e.id === someId)
    if (elementIndex > -1) {
      /**
       * Update event
       * @event EntitySelect#input
       * @type E[]
       */
      const selectedElements = [...this.value] as E[]
      selectedElements.splice(elementIndex, 1)
      this.$emit('input', selectedElements)
    }
  }

  /**
   * returns all elements except the ones that have already been selected
   *
   * @return {E[]} an array of elements
   */
  get allExceptSelected (): E[] {
    return this.elements.filter(c => !this.value.find(rc => rc.id === c.id))
  }
}
</script>
