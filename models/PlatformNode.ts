import { IConfigurationsTreeNode } from '@/models/IConfigurationsTreeNode'
import { DeviceNode } from '@/models/DeviceNode'
import Platform from '@/models/Platform'

export class PlatformNode implements IConfigurationsTreeNode<Platform> {
  private node: Platform
  private children: Array<PlatformNode|DeviceNode> = []

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

  setChildren (children: Array<PlatformNode|DeviceNode>) {
    this.children = children
  }

  getChildren (): Array<PlatformNode|DeviceNode> {
    return this.children
  }
}
