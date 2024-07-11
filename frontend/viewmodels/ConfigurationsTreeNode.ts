/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2021
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

/**
 * @file provides an union type of Platform- and DeviceNodes
 * @author <marc.hanisch@gfz-potsdam.de>
 */

import { PlatformNode } from '@/viewmodels/PlatformNode'
import { DeviceNode } from '@/viewmodels/DeviceNode'
import { ConfigurationNode } from '@/viewmodels/ConfigurationNode'

export type ConfigurationsTreeNode = PlatformNode | DeviceNode | ConfigurationNode
