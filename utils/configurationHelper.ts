import { DateTime } from 'luxon'
import { Configuration } from '@/models/Configuration'
import { IActionDateWithText } from '@/utils/configurationInterfaces'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'
import { PlatformNode } from '@/viewmodels/PlatformNode'
import { DeviceNode } from '@/viewmodels/DeviceNode'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'
export default {
  getActionDatesWithTextsByConfiguration (configuration: Configuration, selectedDate: DateTime): IActionDateWithText[] {
    const datesWithTexts = []
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
    datesWithTexts.push({
      date: selectedDate,
      isSelected: true
    })
    datesWithTexts.push({
      date: DateTime.utc(),
      isNow: true
    })

    const byDates: { [idx: number]: any[] } = {}
    for (const dateObject of datesWithTexts) {
      const key: number = dateObject.date.toMillis()
      if (!byDates[key]) {
        byDates[key] = [dateObject]
      } else {
        byDates[key].push(dateObject)
      }
    }
    const allDates: number[] = [...Object.keys(byDates)].map(x => parseFloat(x))
    allDates.sort()

    const result = []
    for (const key of allDates) {
      const value: any[] = byDates[key]
      const texts = value.filter(e => e.text).map(e => e.text)
      const isNow = value.filter(e => e.isNow).length > 0
      const isSelected = value.filter(e => e.isSelected).length > 0

      let text = dateToDateTimeStringHHMM(value[0].date) + ' - '

      if (isNow) {
        text += 'Now'

        if (texts.length > 0) {
          text += ' + ' + texts.length + ' more mount/unmount'
          if (texts.length > 1) {
            text += ' actions'
          } else {
            text += ' action'
          }
        }
      } else if (texts.length > 0) {
        text += texts[0]

        if (texts.length > 1) {
          text += ' + ' + (texts.length - 1) + ' more mount/unmount'
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
    }
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

  getHierarchyNodeNamesByTreeAndSelectedNode (tree:ConfigurationsTree, selectedNode: ConfigurationsTreeNode|null): Object[] {
    if (!selectedNode) {
      return []
    }

    const openInNewTab = true
    return tree.getPathObjects(selectedNode).map((selectedNode:ConfigurationsTreeNode) => {
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
