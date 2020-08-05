/**
 * @file provides a wrapper class for a platform in a tree
 * @author <marc.hanisch@gfz-potsdam.de>
 */

import { IConfigurationsTreeNode } from '@/models/IConfigurationsTreeNode'
import { ConfigurationsTree } from '@/models/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/models/ConfigurationsTreeNode'
import Platform from '@/models/Platform'

/**
 * a class that wraps a Platform instance for the usage in a ConfigurationsTree
 */
export class PlatformNode implements IConfigurationsTreeNode<Platform> {
  private node: Platform
  private tree: ConfigurationsTree = new ConfigurationsTree()

  constructor (node: Platform) {
    this.node = node
  }

  get id (): number | null {
    return this.node.id
  }

  get name (): string {
    return this.node.shortName
  }

  get disabled (): boolean {
    return false
  }

  canHaveChildren (): boolean {
    return true
  }

  unpack (): Platform {
    return this.node
  }

  setTree (tree: ConfigurationsTree) {
    this.tree = tree
  }

  getTree (): ConfigurationsTree {
    return this.tree
  }

  set children (children: ConfigurationsTreeNode[]) {
    this.tree = ConfigurationsTree.fromArray(children)
  }

  get children (): ConfigurationsTreeNode[] {
    return this.tree.toArray()
  }
}
