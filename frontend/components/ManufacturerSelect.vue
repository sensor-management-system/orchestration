<!--
SPDX-FileCopyrightText: 2020 - 2023
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <EntitySelect
    v-model="wrappedValue"
    :readonly="readonly"
    :fetch-function="findAllManufacturers"
    :label="label"
    color="brown"
  />
</template>

<script lang="ts">
/**
 * @file provides a component to select manufacturers
 * @author <marc.hanisch@gfz-potsdam.de>
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import EntitySelect from '@/components/EntitySelect.vue'

import { Manufacturer } from '@/models/Manufacturer'

type ManufacturersLoaderFunction = () => Promise<Manufacturer[]>

/**
 * A class component to select manufacturers
 * @extends Vue
 */
@Component({
  components: {
    EntitySelect
  }
})
// @ts-ignore
export default class ManufacturerSelect extends Vue {
  /**
   * a list of Manufacturer
   */
  @Prop({
    default: () => [] as Manufacturer[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value!: Manufacturer[]

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
   * the label of the component
   */
  @Prop({
    required: true,
    type: String
  })
  // @ts-ignore
  readonly label!: String

  /**
   * fetches a list of Manufacturer
   *
   * @return {ManufacturersLoaderFunction} a list of Manufacturer
   */
  get findAllManufacturers (): ManufacturersLoaderFunction {
    return () => { return this.$api.manufacturer.findAll() }
  }

  /**
   * returns the list of manufacturers
   *
   * @return {Manufacturer[]} a list of manufacturers
   */
  get wrappedValue () {
    return this.value
  }

  /**
   * triggers an input event when the list of manufacturers has changed
   *
   * @param {Manufacturer[]} newValue - a list of manufacturers
   * @fires ManufacturerSelect#input
   */
  set wrappedValue (newValue) {
    /**
     * fires an input event
     * @event ManufacturerSelect#input
     * @type {Manufacturer[]}
     */
    this.$emit('input', newValue)
  }
}
</script>
