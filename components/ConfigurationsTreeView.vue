<!--
Web client of the Sensor Management System software developed within the
Helmholtz DataHub Initiative by GFZ and UFZ.

Copyright (C) 2022
- Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
- Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
- Tim Eder (UFZ, tim.eder@ufz.de)
- Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
- Helmholtz Centre Potsdam - GFZ German Research Centre for
  Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ
  (UFZ, https://www.ufz.de)

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
      :activatable="activatable"
      :hoverable="activatable"
      rounded
      open-all
      :open.sync="openNodes"
      return-object
    >
      <template #label="{item}">
        <div v-if="item.isDevice()">
          Device - {{ item.unpack().device.shortName }}
        </div>
        <div v-if="item.isPlatform()">
          Platform - {{ item.unpack().platform.shortName }}
        </div>
        <div v-if="item.isConfiguration()">
          Configuration - {{ getConfigurationLabel(item.unpack().configuration) }}
        </div>
      </template>
      <template #prepend="{ item }">
        <v-icon v-if="item.isPlatform()">
          mdi-rocket-outline
        </v-icon>
        <v-icon v-if="item.isDevice()">
          mdi-network-outline
        </v-icon>
        <v-icon v-if="item.isConfiguration()">
          mdi-file-cog
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
import { Vue, Component, Prop, Watch } from 'nuxt-property-decorator'

import { Configuration } from '@/models/Configuration'
import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'

import { dateToString } from '@/utils/dateHelper'

/**
 * A class component to display platforms and devices in a tree
 * @extends Vue
 */
@Component({
  computed: {
  }
})
export default class ConfigurationsTreeView extends Vue {
  private openNodes: ConfigurationsTreeNode[] = []

  /**
   * the selected node
   */
  @Prop({
    required: true
  })
  readonly value!: ConfigurationsTreeNode | null

  /**
   * the tree
   */
  @Prop({
    required: true,
    type: Object
  })
  readonly tree!: ConfigurationsTree

  /**
   * activatable nodes
   */
  @Prop({
    default: true,
    required: false,
    type: Boolean
  })
  readonly activatable!: boolean

  created (): void {
    this.initializeOpenNodes()
  }

  initializeOpenNodes (): void {
    if (this.tree) {
      this.openNodes = this.tree.getAllNodesAsList().filter(i => i.canHaveChildren() && 'children' in i && i.children.length > 0)
    } else {
      this.openNodes = []
    }
  }

  /**
   * returns the tree as a flat array of nodes
   *
   * @return {ConfigurationsTreeNode[]} an Array of nodes
   */
  get items (): ConfigurationsTreeNode[] {
    return this.tree.toArray()
  }

  /**
   * returns a list of selected nodes
   *
   * notice that in this component the selection of only one node is supported
   * so this method returns an array with 0 or 1 items
   *
   * @return {string[]} an empty array or an Array with the id of exactly one selected node
   */
  get selectedNodeSingletonList (): ConfigurationsTreeNode[] {
    if (this.value === null) {
      return []
    }
    return [this.value]
  }

  /**
   * sets the selected nodes, triggers a select event
   *
   * notice that in this component the selection of only one node is supported
   * so this method sets the first item of the argument array
   *
   * @fires ConfigurationsTreeView#select
   */
  set selectedNodeSingletonList (nodesArray: ConfigurationsTreeNode[]) {
    const node: ConfigurationsTreeNode | null = nodesArray[0] ?? null
    this.$emit('input', node)
  }

  getConfigurationLabel (config: Configuration): string {
    let label = config.label
    if (config.startDate) {
      label += ' (' + dateToString(config.startDate)
      if (config.endDate) {
        label += ' - ' + dateToString(config.endDate)
      }
      label += ')'
    }
    return label
  }

  @Watch('tree', {
    immediate: true,
    deep: true
  })
  onTreeChanged () {
    this.initializeOpenNodes()
  }
}
</script>

<style scoped>
.disabled {
  text-decoration: line-through;
}
</style>
