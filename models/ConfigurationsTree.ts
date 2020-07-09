import { ConfigurationsTreeNode } from './ConfigurationsTreeNode'
import { PlatformNode } from './PlatformNode'

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

export class ConfigurationsTree implements Iterable<ConfigurationsTreeNode> {
  private tree: ConfigurationsTreeNode[] = [] as ConfigurationsTreeNode[]

  static fromArray (nodes: ConfigurationsTreeNode[]): ConfigurationsTree {
    const result = new ConfigurationsTree()
    for (const node of nodes) {
      result.push(node)
    }
    return result
  }

  toArray (): ConfigurationsTreeNode[] {
    return this.tree
  }

  [Symbol.iterator] (): Iterator<ConfigurationsTreeNode> {
    return new ConfigurationsTreeIterator(this)
  }

  get length (): number {
    return this.tree.length
  }

  isValidIndex (index: number): boolean {
    return index >= 0 && index < this.length
  }

  at (index: number): ConfigurationsTreeNode {
    if (!this.isValidIndex(index)) {
      throw new RangeError('index out of range')
    }
    return this.tree[index]
  }

  push (node: ConfigurationsTreeNode): number {
    return this.tree.push(node)
  }

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
        const aNode: ConfigurationsTreeNode = nodes.at(i)
        if (aNode === node) {
          nodes.removeAt(i)
          return true
        }
        if (!aNode.canHaveChildren()) {
          continue
        }
        const removed = removeRecursive(node, (aNode as PlatformNode).getTree())
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
   * returns the path in the tree to the node
   *
   * @param {number} nodeId - the node to get the path for
   * @return {string[]} an array of node names
   */
  getPath (nodeId: number): string[] {
    const getPathRecursive = (nodeId: number, nodes: ConfigurationsTree, path: string[]): boolean => {
      for (const node of nodes) {
        if (node.id === nodeId) {
          path.push(node.name)
          return true
        }
        if (!node.canHaveChildren()) {
          continue
        }
        if (getPathRecursive(nodeId, (node as PlatformNode).getTree(), path)) {
          path.unshift(node.name)
          return true
        }
      }
      return false
    }

    const paths: string[] = []
    getPathRecursive(nodeId, this, paths)
    return paths
  }

  /**
   * finds a node in the tree by its id
   *
   * @param {number} nodeId - the id of the node to search
   * @return {ConfigurationsTreeNode|null} the found node, null if it was not found
   */
  getById (nodeId: number): ConfigurationsTreeNode | null {
    const getByIdRecursive = (nodeId: number, nodes: ConfigurationsTree): ConfigurationsTreeNode | null => {
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
   * returns the parent of a node in the tree
   *
   * @param {ConfigurationsTreeNode} node - the node to get the parent of
   * @return {ConfigurationsTreeNode|null} the parent of the node, null if the node has not parent
   */
  getParent (node: ConfigurationsTreeNode): ConfigurationsTreeNode | null {
    const getParentRecursive = (node: ConfigurationsTreeNode, parentNode: ConfigurationsTreeNode | null, nodes: ConfigurationsTree): ConfigurationsTreeNode | null => {
      for (const aNode of nodes) {
        if (node === aNode) {
          return parentNode
        }
        if (!aNode.canHaveChildren()) {
          continue
        }
        const found = getParentRecursive(node, aNode, (aNode as PlatformNode).getTree())
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
