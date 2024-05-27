<!--
SPDX-FileCopyrightText: 2020 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <EntitySelect
    v-model="wrappedValue"
    :readonly="readonly"
    :fetch-function="findAllPlatformTypes"
    :label="label"
    color="red"
  />
</template>

<script lang="ts">
/**
 * @file provides a component to select platform types
 * @author <marc.hanisch@gfz-potsdam.de>
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import EntitySelect from '@/components/EntitySelect.vue'

import { PlatformType } from '@/models/PlatformType'

type PlatformTypeLoaderFunction = () => Promise<PlatformType[]>

/**
 * A class component to select platform types
 * @extends Vue
 */
@Component({
  components: {
    EntitySelect
  }
})
// @ts-ignore
export default class PlatformTypeSelect extends Vue {
  /**
   * a list of PlatformTypes
   */
  @Prop({
    default: () => [] as PlatformType[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value!: PlatformType[]

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
  readonly label!: string

  /**
   * fetches all PlatformTypes from the API
   *
   * @return {PlatformTypeLoaderFunction} a function that returns a promise which returns a list of PlatformTypes
   */
  get findAllPlatformTypes (): PlatformTypeLoaderFunction {
    return () => { return this.$api.platformTypes.findAll() }
  }

  /**
   * returns the list of platformtypes
   *
   * @return {PlatformType[]} a list of PlatformTypes
   */
  get wrappedValue () {
    return this.value
  }

  /**
   * triggers an input event when the list of PlatformTypes has changed
   *
   * @param {PlatformType[]} newValue - a list of PlatformTypes
   * @fires PlatformTypeSelect#input
   */
  set wrappedValue (newValue) {
    /**
     * fires an input event
     * @event PlatformTypeSelect#input
     * @type {PlatformType[]}
     */
    this.$emit('input', newValue)
  }
}
</script>
