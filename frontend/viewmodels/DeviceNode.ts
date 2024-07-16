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
 * @file provides a wrapper class for a device in a tree
 * @author <marc.hanisch@gfz-potsdam.de>
 */

import { IConfigurationsTreeNode, IConfigurationsTreeNodeWithChildren } from '@/viewmodels/IConfigurationsTreeNode'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { ConfigurationsTree } from '@/viewmodels//ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'

import { coalesce } from '@/utils/stringHelpers'

/**
 * a class that wraps a Device instance for the usage in a ConfigurationsTree
 */
export class DeviceNode implements IConfigurationsTreeNode<DeviceMountAction> {
  private node: DeviceMountAction
  private tree: ConfigurationsTree = new ConfigurationsTree()
  private _disabled: boolean = false
  private _id: string | null = ''

  static readonly ID_PREFIX = 'DeviceNode-'

  constructor (node: DeviceMountAction) {
    this.node = node
    this._id = DeviceNode.ID_PREFIX + this.node.device.id
  }

  get id (): string | null {
    return this._id
  }

  get elementId (): string | null {
    if (!this.node.device.id) {
      return null
    }
    return this.node.device.id
  }

  get name (): string {
    const partsOffsets = []
    if (this.node.offsetX !== 0.0) {
      partsOffsets.push('x=' + this.node.offsetX + 'm')
    }
    if (this.node.offsetY !== 0.0) {
      partsOffsets.push('y=' + this.node.offsetY + 'm')
    }
    if (this.node.offsetZ !== 0.0) {
      partsOffsets.push('z=' + this.node.offsetZ + 'm')
    }
    const offsetText = partsOffsets.join(', ')
    if (offsetText) {
      return this.nameWithoutOffsets + ' (' + offsetText + ')'
    }
    return this.nameWithoutOffsets
  }

  get nameWithoutOffsets (): string {
    return this.node.device.shortName
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

  canHaveChildren (): this is IConfigurationsTreeNodeWithChildren<DeviceMountAction> {
    return true
  }

  isPlatform (): boolean {
    return false
  }

  isDevice (): this is DeviceNode {
    return true
  }

  isConfiguration (): boolean {
    return false
  }

  unpack (): DeviceMountAction {
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

  get typeName (): string {
    const device = this.node.device
    return coalesce(device.deviceTypeName, 'Device')
  }

  static createFromObject (someObject: DeviceNode): DeviceNode {
    const newObject = new DeviceNode(someObject.unpack())
    newObject.setTree(ConfigurationsTree.createFromObject(someObject.getTree()))
    return newObject
  }
}
