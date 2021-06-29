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

import { DateTime } from 'luxon'

import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { DeviceUnmountAction } from '@/models/DeviceUnmountAction'
import { IMountActions } from '@/models/IMountActions'
import { Platform } from '@/models/Platform'

import { PlatformMountAction } from '@/models/PlatformMountAction'
import { PlatformUnmountAction } from '@/models/PlatformUnmountAction'

import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { DeviceNode } from '@/viewmodels/DeviceNode'
import { PlatformNode } from '@/viewmodels/PlatformNode'

import { dateTimesEqual } from '@/utils/dateHelper'

interface IWithDate {
  date: DateTime
}

export function byDateOldestFirst (a: IWithDate, b: IWithDate): number {
  if (a.date < b.date) {
    return -1
  } else if (a.date > b.date) {
    return 1
  }
  return 0
}

export function byDateOldestLast (a: IWithDate, b: IWithDate): number {
  if (a.date < b.date) {
    return 1
  } else if (a.date > b.date) {
    return -1
  }
  return 0
}

export function getActivePlatforms (
  mountActions: IMountActions,
  dateTime: DateTime
): {[idx: string]: PlatformMountAction} {
  const latestMountUnmountActionByPlatformId: {[idx: string]: PlatformMountAction | PlatformUnmountAction} = {}
  for (const platformMountAction of mountActions.platformMountActions) {
    const platformId = platformMountAction.platform.id
    if (platformId) {
      if (dateTime >= platformMountAction.date) {
        const latestDate = latestMountUnmountActionByPlatformId[platformId]?.date
        if (!latestDate || latestDate < platformMountAction.date) {
          latestMountUnmountActionByPlatformId[platformId] = platformMountAction
        }
      }
    }
  }
  for (const platformUnmountAction of mountActions.platformUnmountActions) {
    const platformId = platformUnmountAction.platform.id
    if (platformId) {
      if (dateTime >= platformUnmountAction.date) {
        const latestDate = latestMountUnmountActionByPlatformId[platformId]?.date
        if (!latestDate || latestDate < platformUnmountAction.date) {
          latestMountUnmountActionByPlatformId[platformId] = platformUnmountAction
        }
      }
    }
  }

  const activePlatforms: {[idx: string]: PlatformMountAction} = {}

  for (const platformId of Object.keys(latestMountUnmountActionByPlatformId)) {
    const lastEntry = latestMountUnmountActionByPlatformId[platformId]
    if (lastEntry.isMountAction) {
      activePlatforms[platformId] = lastEntry as PlatformMountAction
    }
  }
  return activePlatforms
}

export function getActiveDevices (
  mountActions: IMountActions,
  dateTime: DateTime
): {[idx: string]: DeviceMountAction} {
  const latestMountUnmountActionByDeviceId: {[idx: string]: DeviceMountAction | DeviceUnmountAction} = {}

  for (const deviceMountAction of mountActions.deviceMountActions) {
    const deviceId = deviceMountAction.device.id
    if (deviceId) {
      if (dateTime >= deviceMountAction.date) {
        const latestDate = latestMountUnmountActionByDeviceId[deviceId]?.date
        if (!latestDate || latestDate < deviceMountAction.date) {
          latestMountUnmountActionByDeviceId[deviceId] = deviceMountAction
        }
      }
    }
  }
  for (const deviceUnmountAction of mountActions.deviceUnmountActions) {
    const deviceId = deviceUnmountAction.device.id
    if (deviceId) {
      if (dateTime >= deviceUnmountAction.date) {
        const latestDate = latestMountUnmountActionByDeviceId[deviceId]?.date
        if (!latestDate || latestDate < deviceUnmountAction.date) {
          latestMountUnmountActionByDeviceId[deviceId] = deviceUnmountAction
        }
      }
    }
  }
  const activeDevices: {[idx: string]: DeviceMountAction} = {}

  for (const deviceId of Object.keys(latestMountUnmountActionByDeviceId)) {
    const lastEntry = latestMountUnmountActionByDeviceId[deviceId]
    if (lastEntry.isMountAction) {
      activeDevices[deviceId] = lastEntry as DeviceMountAction
    }
  }

  return activeDevices
}

export function buildConfigurationTree (
  mountActions: IMountActions,
  dateTime: DateTime
): ConfigurationsTree {
  const activePlatforms = getActivePlatforms(mountActions, dateTime)
  const activeDevices = getActiveDevices(mountActions, dateTime)

  const handleNodesWithMissingParent = (tree: ConfigurationsTree, node: PlatformNode | DeviceNode) => {
    // If we don't want to include node with an already unmounted parent
    // then we can just take this like here out.
    // But for the moment, we want those to be included in the root
    // so that the user can unmount them explicitly.
    tree.push(node)
  }

  const tree = new ConfigurationsTree()

  // now we could check that all of the are valid
  // but we will skip that for now
  const platformNodeById: {[idx: string]: PlatformNode} = {}
  for (const platformId of Object.keys(activePlatforms)) {
    const platformNode = new PlatformNode(activePlatforms[platformId])
    platformNodeById[platformId] = platformNode
  }
  for (const platformId of Object.keys(activePlatforms)) {
    const platformNode = platformNodeById[platformId]
    const platformAction = activePlatforms[platformId]
    if (platformAction.parentPlatform != null && platformAction.parentPlatform.id != null) {
      const parentPlatformNode = platformNodeById[platformAction.parentPlatform.id]
      if (parentPlatformNode) {
        parentPlatformNode.children.push(platformNode)
      } else {
        handleNodesWithMissingParent(tree, platformNode)
      }
    } else {
      tree.push(platformNode)
    }
  }

  const deviceNodeById: {[idx: string]: DeviceNode} = {}
  for (const deviceId of Object.keys(activeDevices)) {
    const deviceNode = new DeviceNode(activeDevices[deviceId])
    const deviceAction = activeDevices[deviceId]
    deviceNodeById[deviceId] = deviceNode
    if (deviceAction.parentPlatform != null && deviceAction.parentPlatform.id != null) {
      const parentPlatformNode = platformNodeById[deviceAction.parentPlatform.id]
      if (parentPlatformNode) {
        parentPlatformNode.children.push(deviceNode)
      } else {
        handleNodesWithMissingParent(tree, deviceNode)
      }
    } else {
      tree.push(deviceNode)
    }
  }

  return tree
}

export function mountPlatform (
  mountActions: IMountActions,
  platform: Platform,
  offsetX: number,
  offsetY: number,
  offsetZ: number,
  contact: Contact,
  description: string,
  parentNode: ConfigurationsTreeNode | null,
  date: DateTime
): IMountActions {
  if (!parentNode) {
    mountActions.platformMountActions.push(
      PlatformMountAction.createFromObject({
        id: '',
        platform,
        parentPlatform: null,
        date,
        offsetX,
        offsetY,
        offsetZ,
        contact,
        description
      })
    )
    return mountActions
  }

  if (!parentNode.canHaveChildren()) {
    throw new Error('selected node-type cannot have children')
  }

  const parentPlatform = (parentNode as PlatformNode).unpack().platform
  mountActions.platformMountActions.push(PlatformMountAction.createFromObject({
    id: '',
    platform,
    parentPlatform,
    date,
    offsetX,
    offsetY,
    offsetZ,
    contact,
    description
  }))
  return mountActions
}

export function mountDevice (
  mountActions: IMountActions,
  device: Device,
  offsetX: number,
  offsetY: number,
  offsetZ: number,
  contact: Contact,
  description: string,
  parentNode: ConfigurationsTreeNode | null,
  date: DateTime
): IMountActions {
  if (!parentNode) {
    mountActions.deviceMountActions.push(DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: null,
      date,
      offsetX,
      offsetY,
      offsetZ,
      contact,
      description
    }))
    return mountActions
  }

  if (!parentNode.canHaveChildren()) {
    throw new Error('selected node-type cannot have children')
  }

  const platform = (parentNode as PlatformNode).unpack().platform
  mountActions.deviceMountActions.push(DeviceMountAction.createFromObject({
    id: '',
    device,
    parentPlatform: platform,
    date,
    offsetX,
    offsetY,
    offsetZ,
    contact,
    description
  }))
  return mountActions
}

export function unmount (
  mountActions: IMountActions,
  node: ConfigurationsTreeNode,
  date: DateTime,
  contact: Contact,
  description: string
) : IMountActions {
  let platformIdsToRemoveActions = new Set<string>()
  let deviceIdsToRemoveActions = new Set<string>()

  if (node.isDevice()) {
    // if we just remove a device it is easy
    // we just want to remove it as it is
    const deviceNode = node as DeviceNode
    const deviceMountAction = deviceNode.unpack()
    const device = deviceMountAction.device
    const deviceId = device.id
    if (deviceId) {
      deviceIdsToRemoveActions.add(deviceId)
    }
  } else {
    // if we have a platform however, then the stuff is going to be
    // complex:
    // - we need to remove all the stuff that is currently active
    // - and we need to remove all the stuff that will be active in the
    //   future and effects this platform - even those that only
    //   will be mounted & unmounted in the future
    //
    // So we will check all of our childs
    // and in that case we can't rely on the tree
    const platformsByDirectParentPlatformId = extractDirectPlatformsByParentPlatformId(mountActions)
    const devicesByDirectParentPlatformId = extractDirectDevicesByParentPlatformId(mountActions)

    const platformsByHierarchyParentPlatformId: {[idx: string]: Set<string>} = {}
    const devicesByHierarchyParentPlatformId: {[idx: string]: Set<string>} = {}

    for (const parentPlatformId of Object.keys(devicesByDirectParentPlatformId)) {
      devicesByDirectParentPlatformId[parentPlatformId].forEach((deviceId: string) => {
        if (!devicesByHierarchyParentPlatformId[parentPlatformId]) {
          devicesByHierarchyParentPlatformId[parentPlatformId] = new Set()
        }
        devicesByHierarchyParentPlatformId[parentPlatformId].add(deviceId)
      })
    }

    for (const parentPlatformId of Object.keys(platformsByDirectParentPlatformId)) {
      const subListsToCheck = [platformsByDirectParentPlatformId[parentPlatformId]]
      while (subListsToCheck.length > 0) {
        for (const list of subListsToCheck[0]) {
          for (const childPlatformId of list) {
            if (!platformsByHierarchyParentPlatformId[parentPlatformId]) {
              platformsByHierarchyParentPlatformId[parentPlatformId] = new Set()
            }
            platformsByHierarchyParentPlatformId[parentPlatformId].add(childPlatformId)
            if (platformsByDirectParentPlatformId[childPlatformId]) {
              subListsToCheck.push(platformsByDirectParentPlatformId[childPlatformId])
            }
            if (devicesByDirectParentPlatformId[childPlatformId]) {
              for (const childDeviceId of devicesByDirectParentPlatformId[childPlatformId]) {
                if (!devicesByHierarchyParentPlatformId[parentPlatformId]) {
                  devicesByHierarchyParentPlatformId[parentPlatformId] = new Set()
                }
                devicesByHierarchyParentPlatformId[parentPlatformId].add(childDeviceId)
              }
            }
          }
        }
        subListsToCheck.shift()
      }
    }
    const platformNode = node as PlatformNode
    const platformMountAction = platformNode.unpack()
    const platform = platformMountAction.platform
    const platformId = platform.id
    if (platformId) {
      deviceIdsToRemoveActions = devicesByHierarchyParentPlatformId[platformId] || new Set()
      platformIdsToRemoveActions = platformsByHierarchyParentPlatformId[platformId] || new Set()
      platformIdsToRemoveActions.add(platformId)
    }
  }

  const activeDevices = getActiveDevices(mountActions, date)
  const activePlatforms = getActivePlatforms(mountActions, date)

  mountActions.platformMountActions = mountActions.platformMountActions.filter((pma: PlatformMountAction) => {
    return !(pma.date >= date && pma.platform.id && platformIdsToRemoveActions.has(pma.platform.id))
  })
  mountActions.platformUnmountActions = mountActions.platformUnmountActions.filter((pua: PlatformUnmountAction) => {
    return !(pua.date >= date && pua.platform.id && platformIdsToRemoveActions.has(pua.platform.id))
  })
  mountActions.deviceMountActions = mountActions.deviceMountActions.filter((dma: DeviceMountAction) => {
    return !(dma.date >= date && dma.device.id && deviceIdsToRemoveActions.has(dma.device.id))
  })
  mountActions.deviceUnmountActions = mountActions.deviceUnmountActions.filter((dua: DeviceUnmountAction) => {
    return !(dua.date >= date && dua.device.id && deviceIdsToRemoveActions.has(dua.device.id))
  })

  // for those entries that are currently active, we want to
  // add anmount actions
  platformIdsToRemoveActions.forEach((platformId: string) => {
    const activeEntry = activePlatforms[platformId]
    if (activeEntry && !dateTimesEqual(activeEntry.date, date)) {
      // if it is the very same date as the mount, then we don't want to
      // add an unmount
      // we just remove the mount - which is already done in the filtering
      const platformUnmountAction = PlatformUnmountAction.createFromObject({
        id: '',
        platform: activeEntry.platform,
        contact,
        date,
        description
      })
      mountActions.platformUnmountActions.push(platformUnmountAction)
    }
  })
  deviceIdsToRemoveActions.forEach((deviceId: string) => {
    const activeEntry = activeDevices[deviceId]
    if (activeEntry && !dateTimesEqual(activeEntry.date, date)) {
      const deviceUnmountAction = DeviceUnmountAction.createFromObject({
        id: '',
        device: activeEntry.device,
        contact,
        date,
        description
      })
      mountActions.deviceUnmountActions.push(deviceUnmountAction)
    }
  })

  return mountActions
}

export function extractDirectPlatformsByParentPlatformId (mountActions: IMountActions): {[idx: string]: Set<string>} {
  const platformsByDirectParentPlatformId: {[idx: string]: Set<string>} = {}

  for (const platformMountAction of mountActions.platformMountActions) {
    if (platformMountAction.parentPlatform) {
      const platformId = platformMountAction.platform.id
      const parentPlatform = platformMountAction.parentPlatform
      const parentPlatformId = parentPlatform.id
      if (platformId && parentPlatformId) {
        if (!platformsByDirectParentPlatformId[parentPlatformId]) {
          platformsByDirectParentPlatformId[parentPlatformId] = new Set()
        }
        platformsByDirectParentPlatformId[parentPlatformId].add(platformId)
      }
    }
  }

  return platformsByDirectParentPlatformId
}

export function extractDirectDevicesByParentPlatformId (mountActions: IMountActions): {[idx: string]: Set<string>} {
  const devicesByDirectParentPlatformId: {[idx: string]: Set<string>} = {}

  for (const deviceMountAction of mountActions.deviceMountActions) {
    if (deviceMountAction.parentPlatform) {
      const deviceId = deviceMountAction.device.id
      const parentPlatform = deviceMountAction.parentPlatform
      const parentPlatformId = parentPlatform.id
      if (deviceId && parentPlatformId) {
        if (!devicesByDirectParentPlatformId[parentPlatformId]) {
          devicesByDirectParentPlatformId[parentPlatformId] = new Set()
        }
        devicesByDirectParentPlatformId[parentPlatformId].add(deviceId)
      }
    }
  }
  return devicesByDirectParentPlatformId
}
