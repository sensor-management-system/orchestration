export interface IConfigurationsTreeNode<T> {
  id: number | null
  name: string
  disabled: boolean

  canHaveChildren (): boolean
  unpack (): T
}
