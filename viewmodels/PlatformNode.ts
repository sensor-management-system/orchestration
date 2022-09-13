/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
 */

/**
 * @file provides a wrapper class for a platform in a tree
 * @author <marc.hanisch@gfz-potsdam.de>
 */

import { IConfigurationsTreeNodeWithChildren } from '@/viewmodels/IConfigurationsTreeNode'
import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { PlatformMountAction } from '@/models/PlatformMountAction'

/**
 * a class that wraps a Platform instance for the usage in a ConfigurationsTree
 */
export class PlatformNode implements IConfigurationsTreeNodeWithChildren<PlatformMountAction> {
  private node: PlatformMountAction
  private tree: ConfigurationsTree = new ConfigurationsTree()
  private _disabled: boolean = false
  private _id: string | null = ''

  static readonly ID_PREFIX = 'PlatformNode-'

  constructor (node: PlatformMountAction) {
    this.node = node
    this._id = PlatformNode.ID_PREFIX + node.platform.id
  }

  get id (): string | null {
    return this._id
  }

  get elementId (): string | null {
    if (!this.node.platform.id) {
      return null
    }
    return this.node.platform.id
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
    return this.node.platform.shortName
  }

  get disabled (): boolean {
    return this._disabled
  }

  set disabled (isDisabled: boolean) {
    this._disabled = isDisabled
  }

  canHaveChildren (): this is IConfigurationsTreeNodeWithChildren<PlatformMountAction> {
    return true
  }

  isPlatform (): this is PlatformNode {
    return true
  }

  isDevice (): boolean {
    return false
  }

  isConfiguration (): boolean {
    return false
  }

  unpack (): PlatformMountAction {
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

  static createFromObject (someObject: PlatformNode): PlatformNode {
    const newObject = new PlatformNode(someObject.unpack())
    newObject.setTree(ConfigurationsTree.createFromObject(someObject.getTree()))
    return newObject
  }
}
