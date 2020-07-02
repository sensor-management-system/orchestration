<template>
  <div>
    <v-autocomplete
      v-if="!readonly"
      :items="allExceptSelected"
      :item-text="(x) => x"
      :item-value="(x) => x.id"
      :label="addLabel"
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
import { INumericId } from '../models/INumericId'

type EntityLoaderFunction<E> = () => Promise<E[]>

/**
 * A class component to select entities
 * @extends Vue
 */
@Component
// @ts-ignore
export default class EntitySelect<E extends INumericId> extends Vue {
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
    default: () => 'Add',
    type: String
  })
  // @ts-ignore
  readonly addLabel: string

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
    const selectedElement: E | undefined = this.elements.find(e => e.id === parseInt(someId))
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
    }
  }

  /**
   * removes an element from the value property
   *
   * @param {number} someId - the id of the element to remove
   * @fires EntitySelect#input
   */
  remove (someId: number) {
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
