/**
 * @file provides an interface for node classes of a tree
 * @author <marc.hanisch@gfz-potsdam.de>
 */

/**
 * an interface to implement wrapper classes for the usage in a ConfigurationsTreeNode
 */
export interface IConfigurationsTreeNode<T> {
  id: number | null
  name: string
  disabled: boolean

  canHaveChildren (): boolean
  unpack (): T
}
