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

import { DeviceMountAction } from '@/models/DeviceMountAction'
import { IMountActions } from '@/models/IMountActions'

import { PlatformMountAction } from '@/models/PlatformMountAction'

import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { DeviceNode } from '@/viewmodels/DeviceNode'
import { PlatformNode } from '@/viewmodels/PlatformNode'

export interface IWithDate {
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

function getActivePlatforms (
  mountActions: IMountActions,
  dateTime: DateTime
): {[idx: string]: PlatformMountAction} {
  const latestMountActions: {[idx: string]: PlatformMountAction} = {}
  for (const platformMountAction of mountActions.platformMountActions) {
    const platformId = platformMountAction.platform.id
    if (platformId) {
      if (dateTime >= platformMountAction.beginDate && (!platformMountAction.endDate || dateTime <= platformMountAction.endDate)) {
        latestMountActions[platformId] = platformMountAction
      }
    }
  }

  const activePlatforms: {[idx: string]: PlatformMountAction} = {}

  for (const platformId of Object.keys(latestMountActions)) {
    const lastEntry = latestMountActions[platformId]
    if (lastEntry.isPlatformMountAction()) {
      activePlatforms[platformId] = lastEntry
    }
  }
  return activePlatforms
}

function getActiveDevices (
  mountActions: IMountActions,
  dateTime: DateTime
): {[idx: string]: DeviceMountAction} {
  const latestMountActions: {[idx: string]: DeviceMountAction} = {}

  for (const deviceMountAction of mountActions.deviceMountActions) {
    const deviceId = deviceMountAction.device.id
    if (deviceId) {
      if (dateTime >= deviceMountAction.beginDate && (!deviceMountAction.endDate || dateTime <= deviceMountAction.endDate)) {
        latestMountActions[deviceId] = deviceMountAction
      }
    }
  }
  const activeDevices: {[idx: string]: DeviceMountAction} = {}

  for (const deviceId of Object.keys(latestMountActions)) {
    const lastEntry = latestMountActions[deviceId]
    if (lastEntry.isDeviceMountAction()) {
      activeDevices[deviceId] = lastEntry
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
