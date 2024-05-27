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
