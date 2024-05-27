/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2021
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { IDeviceMountAction } from '@/models/DeviceMountAction'
import { IMountAction } from '@/models/MountAction'
import { IPlatformMountAction } from '@/models/PlatformMountAction'

import { IConfigurationMountAction } from '@/viewmodels/ConfigurationMountAction'

/**
 * @file provides an interface for node classes of a tree
 * @author <marc.hanisch@gfz-potsdam.de>
 */

/**
 * an interface to implement wrapper classes for the usage in a ConfigurationsTreeNode
 */
export interface IConfigurationsTreeNode<T extends IMountAction> {
  id: string | null
  name: string
  nameWithoutOffsets: string
  disabled: boolean

  canHaveChildren (): boolean
  isPlatform (): boolean
  isDevice (): boolean
  isConfiguration (): boolean
  unpack (): T
}

export interface IConfigurationsTreeNodeWithChildren<T extends IMountAction> extends IConfigurationsTreeNode<T> {
  children: IConfigurationsTreeNode<IPlatformMountAction|IDeviceMountAction|IConfigurationMountAction>[]
}
