/**
 * @file provides an interface for node classes of a tree
 * @author <marc.hanisch@gfz-potsdam.de>
 */

/**
 * an interface to implement wrapper classes for the usage in a ConfigurationsTreeNode
 */
export interface IConfigurationsTreeNode<T> {
  id: string | null
  name: string
  disabled: boolean

  canHaveChildren (): boolean
  isPlatform (): boolean
  isDevice (): boolean
  unpack (): T
}
