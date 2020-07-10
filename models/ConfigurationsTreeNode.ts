/**
 * @file provides an union type of Platform- and DeviceNodes
 * @author <marc.hanisch@gfz-potsdam.de>
 */

import { PlatformNode } from './PlatformNode'
import { DeviceNode } from './DeviceNode'

export type ConfigurationsTreeNode = PlatformNode | DeviceNode
