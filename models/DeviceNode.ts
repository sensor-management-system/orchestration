/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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
  private _disabled: boolean = false

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
    return this._disabled
  }

  set disabled (isDisabled: boolean) {
    this._disabled = isDisabled
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
