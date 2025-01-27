/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { IOffsets } from '@/utils/configurationInterfaces'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { Platform } from '@/models/Platform'
import { Device } from '@/models/Device'
import { ConfigurationMountAction } from '@/viewmodels/ConfigurationMountAction'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Configuration } from '@/models/Configuration'

/**
 * sums the offsets of all nodes in an array
 *
 * @param {ConfigurationsTreeNode[]} nodes - the nodes to calculate the offsets from
 * @returns {IOffsets} an object containing all summed offsets
 */
export function sumOffsets (nodes: ConfigurationsTreeNode[]): IOffsets {
  const result = {
    offsetX: 0,
    offsetY: 0,
    offsetZ: 0
  }
  nodes.forEach((node) => {
    result.offsetX += node.unpack().offsetX
    result.offsetY += node.unpack().offsetY
    result.offsetZ += node.unpack().offsetZ
  })
  return result
}

export function getEntityByConfigurationsTreeNode (node: ConfigurationsTreeNode): Platform|Device|Configuration|null {
  if (!node) {
    return null
  }
  if (node.isPlatform()) {
    const unpacked: PlatformMountAction = node.unpack() as PlatformMountAction
    return unpacked.platform
  }
  if (node.isDevice()) {
    const unpacked: DeviceMountAction = node.unpack() as DeviceMountAction
    return unpacked.device
  }
  if (node.isConfiguration()) {
    const unpacked: ConfigurationMountAction = node.unpack() as ConfigurationMountAction
    return unpacked.configuration
  }
  return null
}
