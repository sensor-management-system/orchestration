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
      :item-value="(x) => x"
      :label="label"
      @change="add"
    />
    <v-chip
      v-for="element in value"
      :key="element"
      class="ma-2"
      :color="color"
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
