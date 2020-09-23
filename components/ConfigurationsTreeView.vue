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
      <template v-slot:prepend="{ item }">
        <v-icon v-if="nodeIsPlatform(item)">
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
 * @file provides a component to select platforms and devices for a configuration
 * @author <marc.hanisch@gfz-potsdam.de>
 */
import { Vue, Component, Prop } from 'nuxt-property-decorator'

import { ConfigurationsTree } from '@/models/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/models/ConfigurationsTreeNode'
import { PlatformNode } from '@/models/PlatformNode'

/**
 * A class component to select platforms and devices for a configuration
 * @extends Vue
 */
@Component
// @ts-ignore
export default class ConfigurationsTreeView extends Vue {
  @Prop({
    required: true,
    type: Object
  })
  // @ts-ignore
  readonly value!: ConfigurationsTree

  @Prop({
    default: null,
    type: Object
  })
  // @ts-ignore
  readonly selected: ConfigurationsTreeNode | null

  get items (): ConfigurationsTreeNode[] {
    return this.value.toArray()
  }

  get selectedNodeSingletonList (): string[] {
    if (!this.selected || !this.selected.id) {
      return []
    }
    return [this.selected.id]
  }

  set selectedNodeSingletonList (nodeIds: string[]) {
    let node: ConfigurationsTreeNode | null = null
    if (nodeIds.length) {
      node = this.value.getById(nodeIds[0])
    }
    this.$emit('select', node)
  }

  /**
   * returns whether a node is a PlatformNode or not
   *
   * @param {ConfigurationsTreeNode} node - the node to check for
   * @return {boolean} true if the node is a PlatformNode
   */
  nodeIsPlatform (node: ConfigurationsTreeNode): boolean {
    return node instanceof PlatformNode
  }
}
</script>
