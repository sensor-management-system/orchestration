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
import { IActionDateWithTextItem } from '@/utils/configurationInterfaces'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { PlatformNode } from '@/viewmodels/PlatformNode'
import { DeviceNode } from '@/viewmodels/DeviceNode'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'

interface IActionDatesWithTextSetting {
  useMounts: boolean | undefined
  useLoctions: boolean | undefined
}
export default {
  getActionDatesWithTextsByConfiguration (configuration: Configuration, selectedDate: DateTime, setting: IActionDatesWithTextSetting): IActionDateWithTextItem[] {
    const datesWithTexts: IActionDateWithTextItem[] = []
    if (setting.useMounts) {
      for (const platformMountAction of configuration.platformMountActions) {
        datesWithTexts.push({
          date: platformMountAction.date,
          text: 'Mount ' + platformMountAction.platform.shortName
        })
      }
      for (const platformUnmountAction of configuration.platformUnmountActions) {
        datesWithTexts.push({
          date: platformUnmountAction.date,
          text: 'Unmount ' + platformUnmountAction.platform.shortName
        })
      }
      for (const deviceMountAction of configuration.deviceMountActions) {
        datesWithTexts.push({
          date: deviceMountAction.date,
          text: 'Mount ' + deviceMountAction.device.shortName
        })
      }
      for (const deviceUnmountAction of configuration.deviceUnmountActions) {
        datesWithTexts.push({
          date: deviceUnmountAction.date,
          text: 'Unmount ' + deviceUnmountAction.device.shortName
        })
      }
    }
    if (setting.useLoctions) {
      for (const staticLocationBeginAction of configuration.staticLocationBeginActions) {
        if (staticLocationBeginAction.beginDate) {
          datesWithTexts.push({
            date: staticLocationBeginAction.beginDate,
            text: 'Static location begin'
          })
        }
      }
      for (const staticLocationEndAction of configuration.staticLocationEndActions) {
        if (staticLocationEndAction.endDate) {
          datesWithTexts.push({
            date: staticLocationEndAction.endDate,
            text: 'Static location end'
          })
        }
      }
      for (const dynamicLocationBeginAction of configuration.dynamicLocationBeginActions) {
        if (dynamicLocationBeginAction.beginDate) {
          datesWithTexts.push({
            date: dynamicLocationBeginAction.beginDate,
            text: 'Dynamic location begin'
          })
        }
      }
      for (const dynamicLocationEndAction of configuration.dynamicLocationEndActions) {
        if (dynamicLocationEndAction.endDate) {
          datesWithTexts.push({
            date: dynamicLocationEndAction.endDate,
            text: 'Dynamic location end'
          })
        }
      }
    }
    datesWithTexts.push({
      text: '',
      date: selectedDate,
      isSelected: true
    })
    datesWithTexts.push({
      text: '',
      date: DateTime.utc(),
      isNow: true
    })

    // sort by date
    // we can use native comparision on luxon objects
    datesWithTexts.sort((a, b) => {
      if (a.date < b.date) {
        return -1
      }
      if (a.date > b.date) {
        return 1
      }
      return 0
    })

    // group by date
    const dateIndex: { [idx: number]: number } = {}
    const itemsGroupedByDate: IActionDateWithTextItem[][] = []
    for (const dateObject of datesWithTexts) {
      const key: number = dateObject.date.toMillis()
      if (!dateIndex[key]) {
        dateIndex[key] = itemsGroupedByDate.length
        itemsGroupedByDate.push([dateObject])
      } else {
        const index = dateIndex[key]
        itemsGroupedByDate[index].push(dateObject)
      }
    }

    const result: IActionDateWithTextItem[] = []

    itemsGroupedByDate.forEach((value) => {
      const texts = value.filter(e => e.text).map(e => e.text)
      const isNow = value.filter(e => e.isNow).length > 0
      const isSelected = value.filter(e => e.isSelected).length > 0

      let text = dateToDateTimeStringHHMM(value[0].date) + ' - '

      if (isNow) {
        text += 'Now'

        if (texts.length > 0) {
          text += ' + ' + texts.length + ' more'
          if (texts.length > 1) {
            text += ' actions'
          } else {
            text += ' action'
          }
        }
      } else if (texts.length > 0) {
        text += texts[0]

        if (texts.length > 1) {
          text += ' + ' + (texts.length - 1) + ' more'
          if (texts.length > 2) {
            text += ' actions'
          } else {
            text += ' action'
          }
        }
      } else if (isSelected) {
        text += 'Selected'
      }

      result.push({
        date: value[0].date,
        text
      })
    })
    return result
  },

  overwriteExistingMountAction (node: ConfigurationsTreeNode, newSettings: any) {
    if (node.isPlatform()) {
      const platformNode = node as PlatformNode
      const platformMountAction = platformNode.unpack()
      platformMountAction.offsetX = newSettings.offsetX
      platformMountAction.offsetY = newSettings.offsetY
      platformMountAction.offsetZ = newSettings.offsetZ
      platformMountAction.contact = newSettings.contact
      platformMountAction.description = newSettings.description
    } else if (node.isDevice()) {
      const deviceNode = node as DeviceNode
      const deviceMountAction = deviceNode.unpack()
      deviceMountAction.offsetX = newSettings.offsetX
      deviceMountAction.offsetY = newSettings.offsetY
      deviceMountAction.offsetZ = newSettings.offsetZ
      deviceMountAction.contact = newSettings.contact
      deviceMountAction.description = newSettings.description
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
      platformMountAction.contact = newSettings.contact
      platformMountAction.description = newSettings.description
      platformMountAction.date = selectedDate
      configuration.platformMountActions.push(platformMountAction)
      selectedNode = new PlatformNode(platformMountAction)
    } else if (node.isDevice()) {
      const deviceNode = node as DeviceNode
      const deviceMountAction = DeviceMountAction.createFromObject(deviceNode.unpack())
      deviceMountAction.offsetX = newSettings.offsetX
      deviceMountAction.offsetY = newSettings.offsetY
      deviceMountAction.offsetZ = newSettings.offsetZ
      deviceMountAction.contact = newSettings.contact
      deviceMountAction.description = newSettings.description
      deviceMountAction.date = selectedDate
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
