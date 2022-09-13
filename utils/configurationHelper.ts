/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Erik Pongratz (UFZ, erik.pongratz@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
 *   (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *   (UFZ, https://www.ufz.de)
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
import { Configuration } from '@/models/Configuration'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { PlatformNode } from '@/viewmodels/PlatformNode'
import { DeviceNode } from '@/viewmodels/DeviceNode'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'

export default {
  overwriteExistingMountAction (node: ConfigurationsTreeNode, newSettings: any) {
    if (node.isPlatform()) {
      const platformNode = node as PlatformNode
      const platformMountAction = platformNode.unpack()
      platformMountAction.offsetX = newSettings.offsetX
      platformMountAction.offsetY = newSettings.offsetY
      platformMountAction.offsetZ = newSettings.offsetZ
      platformMountAction.beginContact = newSettings.beginContact
      platformMountAction.beginDescription = newSettings.beginDescription
    } else if (node.isDevice()) {
      const deviceNode = node as DeviceNode
      const deviceMountAction = deviceNode.unpack()
      deviceMountAction.offsetX = newSettings.offsetX
      deviceMountAction.offsetY = newSettings.offsetY
      deviceMountAction.offsetZ = newSettings.offsetZ
      deviceMountAction.beginContact = newSettings.beginContact
      deviceMountAction.beginDescription = newSettings.beginDescription
    }
  },

  addNewMountAction (
    node: ConfigurationsTreeNode,
    newSettings: any,
    configuration: Configuration,
    selectedDate: DateTime,
    selectedNode: ConfigurationsTreeNode|null
  ) {
    if (!selectedNode) {
      return null
    }

    if (node.isPlatform()) {
      const platformNode = node as PlatformNode
      const platformMountAction = PlatformMountAction.createFromObject(platformNode.unpack())
      platformMountAction.offsetX = newSettings.offsetX
      platformMountAction.offsetY = newSettings.offsetY
      platformMountAction.offsetZ = newSettings.offsetZ
      platformMountAction.beginContact = newSettings.beginContact
      platformMountAction.beginDescription = newSettings.beginDescription
      platformMountAction.beginDate = selectedDate
      configuration.platformMountActions.push(platformMountAction)
      selectedNode = new PlatformNode(platformMountAction)
    } else if (node.isDevice()) {
      const deviceNode = node as DeviceNode
      const deviceMountAction = DeviceMountAction.createFromObject(deviceNode.unpack())
      deviceMountAction.offsetX = newSettings.offsetX
      deviceMountAction.offsetY = newSettings.offsetY
      deviceMountAction.offsetZ = newSettings.offsetZ
      deviceMountAction.beginContact = newSettings.beginContact
      deviceMountAction.beginDescription = newSettings.beginDescription
      deviceMountAction.beginDate = selectedDate
      configuration.deviceMountActions.push(deviceMountAction)
      selectedNode = new DeviceNode(deviceMountAction)
    }

    return selectedNode
  },

  getHierarchyNodeNamesByTreeAndSelectedNode (tree: ConfigurationsTree, selectedNode: ConfigurationsTreeNode|null): Object[] {
    if (!selectedNode) {
      return []
    }

    const openInNewTab = true
    return tree.getPathObjects(selectedNode).map((selectedNode: ConfigurationsTreeNode) => {
      // we not only handle the names here, but we also allow to have links to our
      // platforms and devices
      const subRoute = selectedNode.isPlatform() ? 'platforms' : 'devices'
      const id = selectedNode.elementId
      const path = subRoute + '/' + id

      let partTarget = {}
      let partLink = {}
      if (openInNewTab) {
        partTarget = {
          target: '_blank'
        }
        partLink = {
          href: path
        }
      } else {
        partLink = {
          to: path
        }
      }

      return {
        text: selectedNode.nameWithoutOffsets,
        ...partLink,
        ...partTarget
      }
    })
  }
}
