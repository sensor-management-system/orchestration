/**
 * @file provides a wrapper class for a device in a tree
 * @author <marc.hanisch@gfz-potsdam.de>
 */

import { IConfigurationsTreeNode } from '@/models/IConfigurationsTreeNode'
import Device from '@/models/Device'

/**
 * a class that wraps a Device instance for the usage in a ConfigurationsTree
 */
export class DeviceNode implements IConfigurationsTreeNode<Device> {
  private node: Device

  static readonly ID_PREFIX = 'DeviceNode-'

  constructor (node: Device) {
    this.node = node
  }

  get id (): string | null {
    if (!this.node.id) {
      return null
    }
    return DeviceNode.ID_PREFIX + this.node.id
  }

  get name (): string {
    return this.node.shortName
  }

  get disabled (): boolean {
    return false
  }

  canHaveChildren (): boolean {
    return false
  }

  isPlatform (): boolean {
    return false
  }

  isDevice (): boolean {
    return true
  }

  unpack (): Device {
    return this.node
  }

  static createFromObject (someObject: DeviceNode): DeviceNode {
    const newObject = new DeviceNode(someObject.unpack())
    return newObject
  }
}
