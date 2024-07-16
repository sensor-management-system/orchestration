<!--
SPDX-FileCopyrightText: 2022 - 2024
- Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
- Marc Hanisch <marc.hanisch@gfz-potsdam.de>
- Tim Eder <tim.eder@ufz.de>
- Tobias Kuhnert <tobias.kuhnert@ufz.de>
- Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
- Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)

SPDX-License-Identifier: EUPL-1.2
-->
<template>
  <div>
    <v-treeview
      :active.sync="selectedNodeSingletonList"
      :items="items"
      :activatable="activatable"
      :hoverable="activatable"
      :disable-per-node="disablePerNode"
      rounded
      open-all
      :open.sync="openNodes"
      return-object
    >
      <template #label="{item}">
        <div v-if="item.isDevice()">
          {{ item.typeName }} -&nbsp;
          <extended-item-name
            :value="item.unpack().device"
            :extended="showDetailedNames || (showDetailedName && item === value)"
          />
          <div v-if="item.label" class="text-caption grey--text text--darken-2">
            {{ item.label }}
          </div>
        </div>
        <div v-if="item.isPlatform()">
          {{ item.typeName }} -&nbsp;
          <extended-item-name
            :value="item.unpack().platform"
            :extended="showDetailedNames || (showDetailedName && item === value)"
          />
          <div v-if="item.label" class="text-caption grey--text text--darken-2">
            {{ item.label }}
          </div>
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

import ExtendedItemName from '@/components/shared/ExtendedItemName.vue'

/**
 * A class component to display platforms and devices in a tree
 * @extends Vue
 */
@Component({
  components: {
    ExtendedItemName
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

  /**
   * whether disabling a parent node disables children nodes as well
   */
  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  readonly disablePerNode!: boolean

  /**
   * show detailed name for the selected node
   */
  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  readonly showDetailedName!: boolean

  /**
   * show detailed names for all nodes
   */
  @Prop({
    default: false,
    required: false,
    type: Boolean
  })
  readonly showDetailedNames!: boolean

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
   * @fires ConfigurationsTreeView#input
   */
  set selectedNodeSingletonList (nodesArray: ConfigurationsTreeNode[]) {
    const node: ConfigurationsTreeNode | null = nodesArray[0] ?? null
    this.$emit('input', node)
  }

  getConfigurationLabel (config: Configuration): string {
    let label = this.$options.filters?.shortenMiddle(config.label, 30)
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
