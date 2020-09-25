/**
 * @file provides classes to configure platforms and devices in a tree
 * @author <marc.hanisch@gfz-potsdam.de>
 */

import { ConfigurationsTreeNode } from '@/models/ConfigurationsTreeNode'
import { DeviceNode } from '@/models/DeviceNode'
import { PlatformNode } from '@/models/PlatformNode'

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
   * returns an Array of ConfigurationsTreeNode
   *
   * @return {ConfigurationsTreeNode[]} an Array of ConfigurationsTreeNodes
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
   * returns the path to the node in the tree
   *
   * @param {ConfigurationsTreeNode} node - the node to get the path for
   * @return {string[]} an array of node names
   */
  getPath (node: ConfigurationsTreeNode): string[] {
    const getPathRecursive = (node: ConfigurationsTreeNode, nodes: ConfigurationsTree, path: string[]): boolean => {
      for (const iteratedNode of nodes) {
        if (iteratedNode === node) {
          path.push(iteratedNode.name)
          return true
        }
        if (!iteratedNode.canHaveChildren()) {
          continue
        }
        if (getPathRecursive(node, (iteratedNode as PlatformNode).getTree(), path)) {
          path.unshift(iteratedNode.name)
          return true
        }
      }
      return false
    }

    const paths: string[] = []
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
        if (iteratedNode.isPlatform() && iteratedNode.unpack().id === platformId) {
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
        if (iteratedNode.isDevice() && iteratedNode.unpack().id === deviceId) {
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
   * returns the parent of a node in the tree
   *
   * @param {ConfigurationsTreeNode} node - the node to get the parent of
   * @return {ConfigurationsTreeNode|null} the parent of the node, null if the node has not parent
   */
  getParent (node: ConfigurationsTreeNode): ConfigurationsTreeNode | null {
    const getParentRecursive = (node: ConfigurationsTreeNode, parentNode: ConfigurationsTreeNode | null, nodes: ConfigurationsTree): ConfigurationsTreeNode | null => {
      for (const iteratedNode of nodes) {
        if (node === iteratedNode) {
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
}
