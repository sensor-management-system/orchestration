/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2021
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

/**
 * @file provides classes to configure platforms and devices in a tree
 * @author <marc.hanisch@gfz-potsdam.de>
 */

import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { DeviceNode } from '@/viewmodels/DeviceNode'
import { PlatformNode } from '@/viewmodels/PlatformNode'
import { ConfigurationNode } from '@/viewmodels/ConfigurationNode'

/**
 * a class to iterate over the direct children of a ConfigurationsTree
 *
 * @example
 * // a ConfigurationsTree can used in a for .. of loop like so:
 * const tree = new ConfigurationsTree()
 * for (const node of tree) {
 *   // do something with node
 * }
 */
export class ConfigurationsTreeIterator implements Iterator<ConfigurationsTreeNode> {
  // We know that we define this class one step later
  // eslint-disable-next-line no-use-before-define
  private tree: ConfigurationsTree
  private index: number = 0

  constructor (tree: ConfigurationsTree) {
    this.tree = tree
  }

  next (): IteratorResult<ConfigurationsTreeNode> {
    if (this.index < this.tree.length) {
      return {
        done: false,
        value: this.tree.at(this.index++)
      }
    } else {
      return {
        done: true,
        value: null
      }
    }
  }
}

/**
 * a class to configure platforms and devices in a tree
 */
export class ConfigurationsTree implements Iterable<ConfigurationsTreeNode> {
  private tree: ConfigurationsTreeNode[] = [] as ConfigurationsTreeNode[]

  /**
   * creates a new instance from an Array of ConfigurationsTreeNodes
   *
   * @static
   * @param {ConfigurationsTreeNode[]} nodes - the Array of nodes to create the instance from
   * @return {ConfigurationsTree} a ConfigurationsTree instance
   */
  static fromArray (nodes: ConfigurationsTreeNode[]): ConfigurationsTree {
    const result = new ConfigurationsTree()
    for (const node of nodes) {
      result.push(node)
    }
    return result
  }

  /**
   * returns an (nested) Array of ConfigurationsTreeNodes
   *
   * @return {ConfigurationsTreeNode[]} an (nested) Array of ConfigurationsTreeNodes
   */
  toArray (): ConfigurationsTreeNode[] {
    return this.tree
  }

  static createFromObject (someObject: ConfigurationsTree): ConfigurationsTree {
    return ConfigurationsTree.fromArray(
      someObject.toArray().map((e) => {
        if (e.isPlatform()) {
          return PlatformNode.createFromObject(e as PlatformNode)
        }
        if (e.isConfiguration()) {
          return ConfigurationNode.createFromObject(e as ConfigurationNode)
        }
        return DeviceNode.createFromObject(e as DeviceNode)
      })
    )
  }

  [Symbol.iterator] (): Iterator<ConfigurationsTreeNode> {
    return new ConfigurationsTreeIterator(this)
  }

  get length (): number {
    return this.tree.length
  }

  get root (): ConfigurationsTreeNode {
    return this.tree[0]
  }

  /**
   * checks wether an index is valid or not
   *
   * @param {number} index - the index to check for
   * @return {boolean} true when the index is valid, otherwise false
   */
  isValidIndex (index: number): boolean {
    return index >= 0 && index < this.length
  }

  /**
   * returns a ConfigurationsTreeNode at the given index
   *
   * @param {number} index - index of the ConfigurationsTreeNode to return
   * @return {ConfigurationsTreeNode} the ConfigurationsTreeNode at the given index
   */
  at (index: number): ConfigurationsTreeNode {
    if (!this.isValidIndex(index)) {
      throw new RangeError('index out of range')
    }
    return this.tree[index]
  }

  /**
   * adds a ConfigurationsTreeNode to the tree
   *
   * @param {ConfigurationsTreeNode} node - the ConfigurationsTreeNode to add
   * @return {number} the length of the tree after the node was added
   */
  push (node: ConfigurationsTreeNode): number {
    return this.tree.push(node)
  }

  /**
   * removes a ConfigurationsTreeNode at the given index
   *
   * @param {number} index - the index of the ConfigurationsTreeNode to remove from
   * @return {ConfigurationsTreeNode} the removed ConfigurationsTreeNode
   */
  removeAt (index: number): ConfigurationsTreeNode {
    if (!this.isValidIndex(index)) {
      throw new RangeError('index out of range')
    }
    return this.tree.splice(index, 1)[0]
  }

  /**
   * removes a node from the tree
   *
   * @param {ConfigurationsTreeNode} node - the node to remove
   * @return {boolean} whether the node was removed or not
   */
  remove (node: ConfigurationsTreeNode): boolean {
    const removeRecursive = (node: ConfigurationsTreeNode, nodes: ConfigurationsTree): boolean => {
      for (let i: number = 0; i < nodes.length; i++) {
        const iteratedNode: ConfigurationsTreeNode = nodes.at(i)
        if (iteratedNode === node) {
          nodes.removeAt(i)
          return true
        }
        if (!iteratedNode.canHaveChildren()) {
          continue
        }
        const removed = removeRecursive(node, (iteratedNode as PlatformNode).getTree())
        if (!removed) {
          continue
        }
        return true
      }
      return false
    }
    return removeRecursive(node, this)
  }

  /**
   * replaces a ConfigurationsTreeNode at the given index
   *
   * If the node to replace has children, they get appended to the children of
   * the new node.
   *
   * @param {number} index - the index of the ConfigurationsTreeNode to replace
   * @param {ConfigurationsTreeNode} node - the new ConfigurationsTreeNode
   * @return {ConfigurationsTreeNode} the replaced ConfigurationsTreeNode
   */
  replaceAt (index: number, node: ConfigurationsTreeNode): ConfigurationsTreeNode {
    if (!this.isValidIndex(index)) {
      throw new RangeError('index out of range')
    }
    const oldNode = this.tree[index]
    if (oldNode.canHaveChildren() && node.canHaveChildren()) {
      node.children = [
        ...node.children,
        ...oldNode.children
      ]
    }
    this.tree[index] = node
    return node
  }

  /**
   * replaces a node in the tree
   *
   * @param {ConfigurationsTreeNode} node - the node to replace
   * @param {ConfigurationsTreeNode} newNode - the new node
   * @return {boolean} whether the node was replaced or not
   */
  replace (node: ConfigurationsTreeNode, newNode: ConfigurationsTreeNode): boolean {
    const replaceRecursive = (node: ConfigurationsTreeNode, newNode: ConfigurationsTreeNode, nodes: ConfigurationsTree): boolean => {
      for (let i: number = 0; i < nodes.length; i++) {
        const iteratedNode: ConfigurationsTreeNode = nodes.at(i)
        if (iteratedNode.id === node.id) {
          nodes.replaceAt(i, newNode)
          return true
        }
        if (!iteratedNode.canHaveChildren()) {
          continue
        }
        const replaced = replaceRecursive(node, newNode, (iteratedNode as PlatformNode).getTree())
        if (!replaced) {
          continue
        }
        return true
      }
      return false
    }
    return replaceRecursive(node, newNode, this)
  }

  /**
   * returns the path to the node in the tree
   *
   * @param {ConfigurationsTreeNode} node - the node to get the path for
   * @return {string[]} an array of node names
   */
  getPath (node: ConfigurationsTreeNode): string[] {
    return this.getPathObjects(node).map((treeNode: ConfigurationsTreeNode) => treeNode.name)
  }

  /**
   * returns the path to the node in the tree
   *
   * @param {ConfigurationsTreeNode} node - the node to get the path for
   * @return {string[]} an array of node names
   */
  getPathObjects (node: ConfigurationsTreeNode): ConfigurationsTreeNode[] {
    const getPathRecursive = (node: ConfigurationsTreeNode, nodes: ConfigurationsTree, path: ConfigurationsTreeNode[]): boolean => {
      for (const iteratedNode of nodes) {
        if (iteratedNode?.id === node?.id) {
          path.push(iteratedNode)
          return true
        }
        if (!iteratedNode.canHaveChildren()) {
          continue
        }
        if (getPathRecursive(node, (iteratedNode as PlatformNode).getTree(), path)) {
          path.unshift(iteratedNode)
          return true
        }
      }
      return false
    }

    const paths: ConfigurationsTreeNode[] = []
    getPathRecursive(node, this, paths)
    return paths
  }

  /**
   * finds a node in the tree by its id
   *
   * @param {string} nodeId - the id of the node to search
   * @return {ConfigurationsTreeNode|null} the found node, null if it was not found
   */
  getById (nodeId: string): ConfigurationsTreeNode | null {
    const getByIdRecursive = (nodeId: string, nodes: ConfigurationsTree): ConfigurationsTreeNode | null => {
      for (const node of nodes) {
        if (node.id === nodeId) {
          return node
        }
        if (!node.canHaveChildren()) {
          continue
        }
        const found = getByIdRecursive(nodeId, (node as PlatformNode).getTree())
        if (!found) {
          continue
        }
        return found
      }
      return null
    }
    return getByIdRecursive(nodeId, this)
  }

  /**
   * finds a platform node in the tree by its id
   *
   * @param {string} nodeId - the id of the node to search
   * @return {PlatformNode|null} the found node, null if it was not found
   */
  getPlatformById (platformId: string): PlatformNode | null {
    const getByIdRecursive = (platformId: string, nodes: ConfigurationsTree): PlatformNode | null => {
      for (const iteratedNode of nodes) {
        if (iteratedNode.isPlatform() && iteratedNode.elementId === platformId) {
          return iteratedNode as PlatformNode
        }
        if (!iteratedNode.canHaveChildren()) {
          continue
        }
        const found = getByIdRecursive(platformId, (iteratedNode as PlatformNode).getTree())
        if (!found) {
          continue
        }
        return found
      }
      return null
    }
    return getByIdRecursive(platformId, this)
  }

  /**
   * finds a device node in the tree by its id
   *
   * @param {string} nodeId - the id of the node to search
   * @return {DeviceNode|null} the found node, null if it was not found
   */
  getDeviceById (deviceId: string): DeviceNode | null {
    const getByIdRecursive = (deviceId: string, nodes: ConfigurationsTree): DeviceNode | null => {
      for (const iteratedNode of nodes) {
        if (iteratedNode.isDevice() && iteratedNode.elementId === deviceId) {
          return iteratedNode as DeviceNode
        }
        if (!iteratedNode.canHaveChildren()) {
          continue
        }
        const found = getByIdRecursive(deviceId, (iteratedNode as PlatformNode).getTree())
        if (!found) {
          continue
        }
        return found
      }
      return null
    }
    return getByIdRecursive(deviceId, this)
  }

  /**
   * returns a flat list with all the nodes in the tree.
   * IMPORTANT: the tree gets traversed in pre-order (NLR), parents appear always before their children in the resulting list
   * @returns {ConfigurationTreeNode[]} the flat list of all the nodes in the hierarchy
   */
  getAllNodesAsList (): ConfigurationsTreeNode[] {
    const result: ConfigurationsTreeNode[] = []
    const visitAndAddToResult = (node: ConfigurationsTreeNode) => {
      result.push(node)
      if (node.canHaveChildren() && 'children' in node) {
        for (const innerNode of node.children) {
          visitAndAddToResult(innerNode)
        }
      }
    }
    for (const node of this) {
      visitAndAddToResult(node)
    }
    return result
  }

  /**
   * returns a list with all the device nodes in the tree.
   * @returns {DeviceNode[]} the flat list of all the device nodes in the hierarchy
   */
  getAllDeviceNodesAsList (): DeviceNode[] {
    const result: DeviceNode[] = this.getAllNodesAsList().filter(i => i.isDevice()) as DeviceNode[]
    return result
  }

  /**
   * returns a list with all the platform nodes in the tree.
   * @returns {PlatformNode[]} the flat list of all the platform nodes in the hierarchy
   */
  getAllPlatformNodesAsList (): PlatformNode[] {
    const result: PlatformNode[] = this.getAllNodesAsList().filter(i => i.isPlatform()) as PlatformNode[]
    return result
  }

  /**
   * returns the parent of a node in the tree
   *
   * @param {ConfigurationsTreeNode} node - the node to get the parent of
   * @return {ConfigurationsTreeNode|null} the parent of the node, null if the node has not parent
   */
  getParent (node: ConfigurationsTreeNode): ConfigurationsTreeNode | null {
    const getParentRecursive = (node: ConfigurationsTreeNode, parentNode: ConfigurationsTreeNode | null, nodes: ConfigurationsTree): ConfigurationsTreeNode | null => {
      for (const iteratedNode of nodes) {
        if (node.id === iteratedNode.id) {
          return parentNode
        }
        if (!iteratedNode.canHaveChildren()) {
          continue
        }
        const found = getParentRecursive(node, iteratedNode, (iteratedNode as PlatformNode).getTree())
        if (!found) {
          continue
        }
        return found
      }
      return null
    }
    return getParentRecursive(node, null, this)
  }

  /**
   * returns all parents of a node in the tree
   *
   * @param {ConfigurationsTreeNode} node - the node to get the parents of
   * @return {ConfigurationsTreeNode} the all parents of the node, empty array if the node has not parent
   */
  getParents (node: ConfigurationsTreeNode): ConfigurationsTreeNode[] {
    const parents: ConfigurationsTreeNode[] = []
    let parent = this.getParent(node)
    while (parent !== null) {
      parents.push(parent)
      parent = this.getParent(parent)
    }
    return parents
  }
}
