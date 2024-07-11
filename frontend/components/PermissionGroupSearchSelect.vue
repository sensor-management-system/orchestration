<!--
SPDX-FileCopyrightText: 2020 - 2022
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <EntitySelect
    v-model="wrappedValue"
    :readonly="readonly"
    :fetch-function="findAllPermissionGroups"
    :label="label"
    color="orange"
  />
</template>

<script lang="ts">
/**
 * @file provides a component to select permission groups
 * @author <marc.hanisch@gfz-potsdam.de>
 * @author <nils.brinckmann@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import EntitySelect from '@/components/EntitySelect.vue'

import { PermissionGroup } from '@/models/PermissionGroup'

type PermissionGroupLoaderFunction = () => Promise<PermissionGroup[]>

/**
 * A class component to select permission groups
 * @extends Vue
 */
@Component({
  components: {
    EntitySelect
  }
})
// @ts-ignore
export default class PermissionGroupSearchSelect extends Vue {
  /**
   * a list of permission groups
   */
  @Prop({
    default: () => [] as PermissionGroup[],
    required: true,
    type: Array
  })
  // @ts-ignore
  readonly value!: PermissionGroup[]

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
   * fetches all permission groups from the API
   *
   * @return {PermissionGroupLoaderFunction} a function that returns a promise which returns a list of permission groups
   */
  get findAllPermissionGroups (): PermissionGroupLoaderFunction {
    return () => { return this.$api.permissionGroupApi.findAll() }
  }

  /**
   * returns the list of permission groups
   *
   * @return {PermissionGroup[]} a list of permission groups
   */
  get wrappedValue () {
    return this.value
  }

  /**
   * triggers an input event when the list of permission groups has changed
   *
   * @param {PermissionGroup[]} newValue - a list of permission groups
   * @fires PermissionGroupSearchSelect#input
   */
  set wrappedValue (newValue) {
    /**
     * fires an input event
     * @event PermissionGroupSearchSelect#input
     * @type {PermissionGroup[]}
     */
    this.$emit('input', newValue)
  }
}
</script>
