/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

/**
 * @file provides a wrapper class for a configuration in a tree
 * @author <marc.hanisch@gfz-potsdam.de>
 */

import { ConfigurationMountAction } from '@/viewmodels/ConfigurationMountAction'
import { IConfigurationsTreeNodeWithChildren } from '@/viewmodels/IConfigurationsTreeNode'
import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'

/**
 * a class that wraps a Configuration instance for the usage in a ConfigurationsTree
 */
export class ConfigurationNode implements IConfigurationsTreeNodeWithChildren<ConfigurationMountAction> {
  private node: ConfigurationMountAction
  private tree: ConfigurationsTree = new ConfigurationsTree()
  private _disabled: boolean = false
  private _id: string | null = ''

  static readonly ID_PREFIX = 'ConfigurationNode-'

  constructor (node: ConfigurationMountAction) {
    this.node = node
    this._id = ConfigurationNode.ID_PREFIX + this.node.id
  }

  get id (): string | null {
    return this._id
  }

  get elementId (): string | null {
    if (!this.node.id) {
      return null
    }
    return this.node.id
  }

  get name (): string {
    return this.node.configuration.label
  }

  get nameWithoutOffsets (): string {
    return this.name
  }

  get disabled (): boolean {
    return this._disabled
  }

  set disabled (isDisabled: boolean) {
    this._disabled = isDisabled
  }

  get label (): string {
    return this.node.label
  }

  canHaveChildren (): this is IConfigurationsTreeNodeWithChildren<ConfigurationMountAction> {
    return true
  }

  isPlatform (): boolean {
    return false
  }

  isDevice (): boolean {
    return false
  }

  isConfiguration (): this is ConfigurationNode {
    return true
  }

  unpack (): ConfigurationMountAction {
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

  static createFromObject (someObject: ConfigurationNode): ConfigurationNode {
    const newObject = new ConfigurationNode(someObject.unpack())
    newObject.setTree(ConfigurationsTree.createFromObject(someObject.getTree()))
    return newObject
  }
}
