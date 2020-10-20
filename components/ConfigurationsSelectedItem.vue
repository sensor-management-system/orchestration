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
  <v-card
    v-if="value"
    outlined
  >
    <v-breadcrumbs :items="breadcrumbs" divider=">" />
    <v-card-text>
      <template v-if="description">
        {{ description }}
      </template>
      <template v-else-if="value.isPlatform()">
        <span class="text--disabled">The selected platform has no description.</span>
      </template>
      <template v-else-if="value.isDevice()">
        <span class="text--disabled">The selected device has no description.</span>
      </template>
    </v-card-text>
    <v-card-actions
      v-if="!readonly"
    >
      <v-btn
        v-if="value"
        color="red"
        text
        data-role="remove-node"
        @click="remove"
      >
        remove
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
/**
* @file provides a component to display information about a selected tree node
* @author <marc.hanisch@gfz-potsdam.de>
*/
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { ConfigurationsTreeNode } from '@/models/ConfigurationsTreeNode'

/**
* A class component to display information about a selected tree node
* @extends Vue
*/
@Component
// @ts-ignore
export default class ConfigurationsSelectedItem extends Vue {
  /**
   * the selected node
   */
  @Prop({
    default: null,
    type: Object
  })
  // @ts-ignore
  readonly value: ConfigurationsTreeNode | null

  /**
   * the breadcrumbs string array
   */
  @Prop({
    default: () => [],
    type: Array
  })
  // @ts-ignore
  readonly breadcrumbs: string[]

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
   * returns the description of a node
   *
   * @return {string} the description
   */
  get description (): string {
    if (!this.value) {
      return ''
    }
    return this.value.unpack().description
  }

  /**
   * triggers a remove event for a node
   *
   * @fires ConfigurationsSelectedItem#remove
   */
  remove () {
    /**
     * fires an input event
     * @event ConfigurationsSelectedItem#remove
     * @type {ConfigurationsTreeNode}
     */
    this.$emit('remove', this.value)
  }
}
</script>
