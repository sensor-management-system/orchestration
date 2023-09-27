<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2022
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
