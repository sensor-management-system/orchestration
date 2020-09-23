/**
 * @file provides an union type of Platform- and DeviceNodes
 * @author <marc.hanisch@gfz-potsdam.de>
 */

import { PlatformNode } from '@/models/PlatformNode'
import { DeviceNode } from '@/models/DeviceNode'

export type ConfigurationsTreeNode = PlatformNode | DeviceNode
