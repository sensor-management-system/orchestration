<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2020-2021
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
    <v-treeview
      :active.sync="selectedNodeSingletonList"
      :items="items"
      activatable
      hoverable
      rounded
      open-all
    >
      <template #prepend="{ item }">
        <v-icon v-if="item.isPlatform()">
          mdi-rocket-outline
        </v-icon>
        <v-icon v-else>
          mdi-network-outline
        </v-icon>
      </template>
    </v-treeview>
  </div>
</template>

<script lang="ts">
/**
 * @file provides a component to display platforms and devices in a tree
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'

/**
 * A class component to display platforms and devices in a tree
 * @extends Vue
 */
@Component
// @ts-ignore
export default class ConfigurationsTreeView extends Vue {
  /**
   * the tree
   */
  @Prop({
    required: true,
    type: Object
  })
  // @ts-ignore
  readonly value!: ConfigurationsTree

  /**
   * the selected node
   */
  @Prop({
    default: null,
    type: Object
  })
  // @ts-ignore
  readonly selected: ConfigurationsTreeNode | null

  /**
   * returns the tree as a flat array of nodes
   *
   * @return {ConfigurationsTreeNode[]} an Array of nodes
   */
  get items (): ConfigurationsTreeNode[] {
    return this.value.toArray()
  }

  /**
   * returns a list of selected notes
   *
   * notice that in this component the selection of only one node is supported
   * so this method returns an array with 0 or 1 items
   *
   * @return {string[]} an empty array or an Array with the id of exactly one selected node
   */
  get selectedNodeSingletonList (): string[] {
    if (!this.selected || !this.selected.id) {
      return []
    }
    return [this.selected.id]
  }

  /**
   * sets the selected nodes, triggers a select event
   *
   * notice that in this component the selection of only one node is supported
   * so this method sets the first item of the argument array
   *
   * @param {string[]} nodeIds - an Array with the ids of the selected nodes
   * @fires ConfigurationsTreeView#select
   */
  set selectedNodeSingletonList (nodeIds: string[]) {
    let node: ConfigurationsTreeNode | null = null
    if (nodeIds.length) {
      node = this.value.getById(nodeIds[0])
    }
    /**
     * fires a select event
     * @event ConfigurationsTreeView#select
     * @type {ConfigurationsTreeNode}
     */
    this.$emit('select', node)
  }
}
</script>
