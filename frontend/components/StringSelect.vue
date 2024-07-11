<!--
SPDX-FileCopyrightText: 2020 - 2023
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
      :item-value="(x) => x"
      :label="label"
      @change="add"
    />
    <v-chip
      v-for="element in value"
      :key="element"
      class="ma-2"
      :color="color"
      :small="small"
      text-color="white"
      :close="!readonly"
      @click:close="remove(element)"
    >
      {{ element }}
    </v-chip>
  </div>
</template>
<script lang="ts">
import { Vue, Component, Prop } from 'nuxt-property-decorator'

@Component
export default class StringSelect extends Vue {
  @Prop({
    default: () => [] as string[],
    required: true,
    type: Array
  })
  readonly value!: string[]

  @Prop({
    default: () => [] as string[],
    required: true,
    type: Array
  })
  readonly items!: string[]

  @Prop({
    default: false,
    type: Boolean
  })
  // @ts-ignore
  readonly readonly: boolean

  @Prop({
    required: true,
    type: String
  })
  readonly label!: string

  @Prop({
    type: String,
    required: true
  })
  readonly color!: string

  @Prop({
    type: Boolean,
    default: false
  })
  readonly small!: boolean

  add (entry: string) {
    const selectedItem = this.items.find(e => e === entry)
    if (selectedItem) {
      this.$emit('input', [
        ...this.value,
        selectedItem
      ])
      this.clearInputField()
    }
  }

  clearInputField () {
    const field: any = this.$refs.autocompletefield
    field.clearableCallback()
  }

  remove (someEntry: string) {
    const elementIndex: number = this.value.findIndex(e => e === someEntry)
    if (elementIndex > -1) {
      const seletedItems = [...this.value] as string[]
      seletedItems.splice(elementIndex, 1)
      this.$emit('input', seletedItems)
    }
  }

  get allExceptSelected (): string[] {
    return this.items.filter(e1 => !this.value.find(e2 => e1 === e2))
  }
}
</script>
