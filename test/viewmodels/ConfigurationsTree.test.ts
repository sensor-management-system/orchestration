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
import { Platform } from '@/models/Platform'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { DeviceNode } from '@/viewmodels/DeviceNode'
import { PlatformNode } from '@/viewmodels/PlatformNode'
import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'

const contact = new Contact()
const date = DateTime.utc(2020, 2, 3, 0, 0, 0, 0)

describe('ConfigurationsTree', () => {
  it('should create a ConfigurationsTree from an Array of nodes', () => {
    const platformNode = new PlatformNode(PlatformMountAction.createFromObject({
      id: '',
      platform: new Platform(),
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Platform mount'
    }))
    const deviceNode = new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device: new Device(),
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Device mount'
    }))

    const tree = ConfigurationsTree.fromArray([platformNode, deviceNode])
    expect(tree).toHaveLength(2)
  })
  it('should return an Array of nodes', () => {
    const platformNode = new PlatformNode(PlatformMountAction.createFromObject({
      id: '',
      platform: new Platform(),
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Platform mount'
    }))
    const deviceNode = new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device: new Device(),
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Device mount'
    }))

    const tree = ConfigurationsTree.fromArray([platformNode, deviceNode])
    const nodesArray = tree.toArray()

    expect(nodesArray).toBeInstanceOf(Array)
    expect(nodesArray).toHaveLength(2)
  })

  it('should create a ConfigurationsTree from another instance ', () => {
    const platformNode = new PlatformNode(PlatformMountAction.createFromObject({
      id: '',
      platform: new Platform(),
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Platform mount'
    }))
    const deviceNode = new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device: new Device(),
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Device mount'
    }))

    const firstTree = ConfigurationsTree.fromArray([platformNode, deviceNode])
    const secondTree = ConfigurationsTree.createFromObject(firstTree)

    expect(secondTree).not.toBe(firstTree)
    expect(secondTree).toEqual(firstTree)
    // allthough the wrapped platform is the same, the nodes are not!
    expect(Object.is(secondTree.toArray()[0], firstTree.toArray()[0])).toBeFalsy()
  })

  it('should validate if a given index is in its range', () => {
    const platformNode = new PlatformNode(PlatformMountAction.createFromObject({
      id: '',
      platform: new Platform(),
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Platform mount'
    }))
    const deviceNode = new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device: new Device(),
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Device mount'
    }))

    const tree = ConfigurationsTree.fromArray([platformNode, deviceNode])

    expect(tree.isValidIndex(1)).toBeTruthy()
    expect(tree.isValidIndex(2)).toBeFalsy()
  })

  it('should return a node at a given index', () => {
    const platformNode = new PlatformNode(PlatformMountAction.createFromObject({
      id: '',
      platform: new Platform(),
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Platform mount'
    }))
    const deviceNode = new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device: new Device(),
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Device mount'
    }))

    const tree = ConfigurationsTree.fromArray([platformNode, deviceNode])

    expect(Object.is(tree.at(1), deviceNode)).toBeTruthy()
    expect(() => { tree.at(2) }).toThrow()
  })

  it('should add a node', () => {
    const platformNode = new PlatformNode(PlatformMountAction.createFromObject({
      id: '',
      platform: new Platform(),
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Platform mount'
    }))
    const deviceNode = new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device: new Device(),
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Device mount'
    }))

    const tree = new ConfigurationsTree()

    expect(tree.push(deviceNode)).toEqual(1)
    expect(tree).toHaveLength(1)
    expect(tree.push(platformNode)).toEqual(2)
    expect(tree).toHaveLength(2)
  })

  it('should remove a given node', () => {
    const platformNode = new PlatformNode(PlatformMountAction.createFromObject({
      id: '',
      platform: new Platform(),
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Platform mount'
    }))
    const deviceNode = new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device: new Device(),
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Device mount'
    }))
    const someOtherNode = new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device: new Device(),
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Device mount'
    }))

    const tree = ConfigurationsTree.fromArray([platformNode, deviceNode])

    expect(tree.remove(deviceNode)).toBeTruthy()
    expect(tree).toHaveLength(1)

    expect(tree.remove(someOtherNode)).toBeFalsy()
    expect(tree).toHaveLength(1)
  })

  it('should remove a given node recursively', () => {
    const platformNode = new PlatformNode(PlatformMountAction.createFromObject({
      id: '',
      platform: new Platform(),
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Platform mount'
    }))
    const deviceNode = new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device: new Device(),
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Device mount'
    }))

    platformNode.getTree().push(deviceNode)

    const tree = ConfigurationsTree.fromArray([platformNode])

    expect(tree.remove(deviceNode)).toBeTruthy()
    expect(platformNode.getTree()).toHaveLength(0)
  })

  it('should remove a node at a given index', () => {
    const platformNode = new PlatformNode(PlatformMountAction.createFromObject({
      id: '',
      platform: new Platform(),
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Platform mount'
    }))
    const deviceNode = new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device: new Device(),
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Device mount'
    }))

    const tree = ConfigurationsTree.fromArray([platformNode, deviceNode])

    expect(Object.is(tree.removeAt(1), deviceNode)).toBeTruthy()
    expect(tree).toHaveLength(1)
    expect(() => { tree.removeAt(2) }).toThrow()
  })

  it('should return an array of node names for a given node id', () => {
    const platform = new Platform()
    platform.id = '1'
    platform.shortName = 'Platform'

    const device = new Device()
    device.id = '2'
    device.shortName = 'Device'

    const platformNode = new PlatformNode(PlatformMountAction.createFromObject({
      id: '',
      platform,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Platform mount'
    }))
    const deviceNode = new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Device mount'
    }))

    platformNode.getTree().push(deviceNode)

    const tree = ConfigurationsTree.fromArray([platformNode])

    expect(tree.getPath(deviceNode)).toEqual(['Platform', 'Device'])
    // when a node is not found, just an empty array should be returned
    expect(tree.getPath(new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device: new Device(),
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Device mount'
    })))).toEqual([])
  })
  it('should return a node by its id recursively', () => {
    const platform = new Platform()
    platform.id = '1'
    platform.shortName = 'Platform'

    const device = new Device()
    device.id = '2'
    device.shortName = 'Device'

    const platformNode = new PlatformNode(PlatformMountAction.createFromObject({
      id: '',
      platform,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Platform mount'
    }))
    const deviceNode = new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Device mount'
    }))

    platformNode.getTree().push(deviceNode)

    const tree = ConfigurationsTree.fromArray([platformNode])

    expect(Object.is(tree.getPlatformById('1'), platformNode)).toBeTruthy()
    expect(Object.is(tree.getDeviceById('2'), deviceNode)).toBeTruthy()
  })
  it('should return the parent node of a node', () => {
    const platform = new Platform()
    const device = new Device()

    const platformNode = new PlatformNode(PlatformMountAction.createFromObject({
      id: '',
      platform,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Platform mount'
    }))
    const deviceNode = new DeviceNode(DeviceMountAction.createFromObject({
      id: '',
      device,
      parentPlatform: null,
      offsetX: 0,
      offsetY: 0,
      offsetZ: 0,
      contact,
      date,
      description: 'Device mount'
    }))

    platformNode.getTree().push(deviceNode)

    const tree = ConfigurationsTree.fromArray([platformNode])

    expect(Object.is(tree.getParent(deviceNode), platformNode)).toBeTruthy()
    expect(tree.getParent(platformNode)).toBeNull()
  })
  describe('#getAllDeviceNodesAsList', () => {
    it('should return an empty array for an empty tree', () => {
      const tree = ConfigurationsTree.fromArray([])
      const deviceNodes = tree.getAllDeviceNodesAsList()

      expect(deviceNodes).toEqual([])
    })
    it('should stay empty if there is just a platform node', () => {
      const platform = new Platform()

      const platformNode = new PlatformNode(PlatformMountAction.createFromObject({
        id: '',
        platform,
        parentPlatform: null,
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        contact,
        date,
        description: 'Platform mount'
      }))

      const tree = ConfigurationsTree.fromArray([platformNode])

      const deviceNodes = tree.getAllDeviceNodesAsList()

      expect(deviceNodes).toEqual([])
    })
    it('should return a device node if it contains one', () => {
      const platform = new Platform()
      const device = new Device()

      const platformNode = new PlatformNode(PlatformMountAction.createFromObject({
        id: '',
        platform,
        parentPlatform: null,
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        contact,
        date,
        description: 'Platform mount'
      }))
      const deviceNode = new DeviceNode(DeviceMountAction.createFromObject({
        id: '',
        device,
        parentPlatform: null,
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        contact,
        date,
        description: 'Device mount'
      }))

      const tree = ConfigurationsTree.fromArray([platformNode, deviceNode])

      const deviceNodes = tree.getAllDeviceNodesAsList()

      expect(deviceNodes).toEqual([deviceNode])
    })
    it('should also consider device nodes if they are mounted on platform nodes', () => {
      const platform = new Platform()
      const device = new Device()

      const platformNode = new PlatformNode(PlatformMountAction.createFromObject({
        id: '',
        platform,
        parentPlatform: null,
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        contact,
        date,
        description: 'Platform mount'
      }))
      const deviceNode = new DeviceNode(DeviceMountAction.createFromObject({
        id: '',
        device,
        parentPlatform: null,
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        contact,
        date,
        description: 'Device mount'
      }))

      platformNode.getTree().push(deviceNode)

      const tree = ConfigurationsTree.fromArray([platformNode])

      const deviceNodes = tree.getAllDeviceNodesAsList()

      expect(deviceNodes).toEqual([deviceNode])
    })
  })
})
