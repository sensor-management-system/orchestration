<!--
SPDX-FileCopyrightText: 2020 - 2022
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <v-row no-gutters justify="end" class="d-flex">
    <v-col class="mr-1 align-self-center text-right">
      {{ label }}
    </v-col>
    <v-col cols="3">
      <v-select
        v-model="model"
        :label="label"
        :items="items"
        class="text-right"
        dense
        flat
        single-line
        hide-details
      >
        <template #selection="{ item }">
          <v-row
            no-gutters
          >
            <v-col
              class="align-self-center text-body-2"
            >
              {{ item }}
            </v-col>
          </v-row>
        </template>
        <template #item="{ item, on, attrs }">
          <v-list-item v-bind="attrs" v-on="on">
            <v-list-item-content class="justify-end">
              {{ item }}
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-select>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'nuxt-property-decorator'

@Component
export default class PageSizeSelect extends Vue {
  /**
   * the actual number of items in a result list (page size)
   *
   */
  @Prop({
    required: true,
    type: Number
  })
  readonly value!: number

  /**
   * an array of selectable numbers
   *
   */
  @Prop({
    required: true,
    type: Array
  })
  readonly items!: number[]

  /**
   * the label of the component
   *
   */
  @Prop({
    default: 'Number of items',
    required: false,
    type: String
  })
  readonly label!: String

  get model (): number {
    return this.value
  }

  set model (value: number) {
    this.$emit('input', value)
  }
}
</script>

<style lang="scss" scoped>
.v-select__selections input {
  display: none;
}
</style>
