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
    :fetch-function="findAllStates"
    :label="label"
    color="green"
  />
</template>

<script lang="ts">
/**
 * @file provides a component to select states
 * @author <marc.hanisch@gfz-potsdam.de>
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import EntitySelect from '@/components/EntitySelect.vue'

import { Status } from '@/models/Status'

type StatesLoaderFunction = () => Promise<Status[]>

/**
 * A class component to select states
 * @extends Vue
 */
@Component({
  components: {
    EntitySelect
  }
})
// @ts-ignore
export default class StatusSelect extends Vue {
  /**
   * a list of states
   */
  @Prop({
    default: () => [] as Status[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value!: Status[]

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
  readonly label!: string

  /**
   * fetches all states from the API
   *
   * @return {StatesLoaderFunction} a function that returns a promise which returns a list of states
   */
  get findAllStates (): StatesLoaderFunction {
    return () => { return this.$api.states.findAll() }
  }

  /**
   * returns the list of states
   *
   * @return {Status[]} a list of states
   */
  get wrappedValue () {
    return this.value
  }

  /**
   * triggers an input event when the list of states has changed
   *
   * @param {Status[]} newValue - a list of states
   * @fires StatusSelect#input
   */
  set wrappedValue (newValue) {
    /**
     * fires an input event
     * @event StatusSelect#input
     * @type {States[]}
     */
    this.$emit('input', newValue)
  }
}
</script>
