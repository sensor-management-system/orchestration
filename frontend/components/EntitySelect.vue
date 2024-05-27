<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
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
      class="mr-1 mb-1"
      small
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

  /**
   * a list of Entities
   */
  @Prop({
    default: () => [] as E[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value!: E[]

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
   * a function to fetch the entities
   */
  @Prop({
    required: true,
    type: Function
  })
  // @ts-ignore
  readonly fetchFunction!: EntityLoaderFunction<E>

  /**
   * the label of the component
   */
  @Prop({
    required: true,
    type: String
  })
  // @ts-ignore
  readonly label!: string

  /**
   * an icon for the selected entities
   */
  @Prop({
    default: () => '',
    type: String
  })
  readonly avatarIcon!: string

  /**
   * a color for the selected entities
   */
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
   * adds an element to the value property and triggers an event
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
       * @type {E[]}
       */
      this.$emit('input', [
        ...this.value,
        selectedElement
      ] as E[])
      this.clearInputField()
    }
  }

  /**
   * clears the input field
   *
   */
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
   * removes an element from the value property and triggers an event
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
