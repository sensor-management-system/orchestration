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

  constructor (node: Device) {
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
    return false
  }

  unpack (): Device {
    return this.node
  }
}
