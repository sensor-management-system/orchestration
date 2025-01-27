/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'

import { PlatformMountAction } from '@/models/PlatformMountAction'
import { Platform } from '@/models/Platform'
import { Contact } from '@/models/Contact'

import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { PlatformNode } from '@/viewmodels/PlatformNode'
import { DeviceProperty } from '@/models/DeviceProperty'
import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import { DeviceNode } from '@/viewmodels/DeviceNode'
import { ConfigurationNode } from '@/viewmodels/ConfigurationNode'
import { UnmountActionValidator } from '@/utils/UnmountActionValidator'
import { Configuration } from '@/models/Configuration'
import { ConfigurationMountAction } from '@/viewmodels/ConfigurationMountAction'

function createDeviceNode (device: Device, parentNode: DeviceNode | PlatformNode | ConfigurationNode | null, beginYear: string | number = '2000', endYear: string | number | null = null): DeviceNode {
  const parentPlatform = parentNode?.isPlatform() ? (parentNode?.unpack() as PlatformMountAction).platform : null
  const parentDevice = parentNode?.isDevice() ? (parentNode?.unpack() as DeviceMountAction).device : null
  const mountAction = createDeviceMountAction(beginYear, endYear, device, parentDevice, parentPlatform)
  const node = new DeviceNode(mountAction)

  if (parentNode) {
    addChildrenForNode(parentNode, node)
  }

  return node
}

function createDeviceMountAction (beginYear: string | number, endYear: string | number | null, device: Device, parentDevice: Device | null, parentPlatform: Platform | null): DeviceMountAction {
  return new DeviceMountAction(
    DateTime.now().toString(),
    device,
    parentPlatform,
    parentDevice,
    DateTime.fromISO(`${beginYear}-01-01T10:00:00`),
    endYear ? DateTime.fromISO(`${endYear}-01-01T10:00:00`) : null,
    0,
    0,
    0,
    '',
    null,
    null,
    null,
    '',
    '',
    new Contact(),
    new Contact(),
    'Start of mount',
    'End of mount',
    ''
  )
}

function createPlatformNode (platform: Platform, parentNode: PlatformNode | ConfigurationNode | null, beginYear: string | number = '2000', endYear: string | number | null = null): PlatformNode {
  const parentPlatform = parentNode?.isPlatform() ? (parentNode?.unpack() as PlatformMountAction).platform : null
  const mountAction = createPlatformMountAction(beginYear, endYear, platform, parentPlatform)
  const node = new PlatformNode(mountAction)

  if (parentNode) {
    addChildrenForNode(parentNode, node)
  }

  return node
}

function createPlatformMountAction (beginYear: string | number, endYear: string | number | null, platform: Platform, parentPlatform: Platform | null): PlatformMountAction {
  return new PlatformMountAction(
    DateTime.now().toString(),
    platform,
    parentPlatform,
    DateTime.fromISO(`${beginYear}-01-01T10:00:00`),
    endYear ? DateTime.fromISO(`${endYear}-01-01T10:00:00`) : null,
    0,
    0,
    0,
    '',
    null,
    null,
    null,
    '',
    '',
    new Contact(),
    new Contact(),
    'Start of mount',
    'End of mount',
    ''
  )
}

function createConfigurationNode () {
  return new ConfigurationNode(new ConfigurationMountAction(new Configuration()))
}

function createConfigurationTreeByRootNode (root: ConfigurationNode): ConfigurationsTree {
  return ConfigurationsTree.fromArray([root, ...root.children])
}

function addChildrenForNode (parent: DeviceNode | PlatformNode | ConfigurationNode, children: DeviceNode | PlatformNode) {
  parent.setTree(ConfigurationsTree.fromArray([...parent.children, children]))
}

function createValidatorByRootNodeAndUnmountDate (
  root: ConfigurationNode,
  endYear: string | number,
  deviceMountActions: DeviceMountAction[] = [],
  platformMountActions: PlatformMountAction[] = [],
  dynamicLocationActions: DynamicLocationAction[] = []
) {
  return new UnmountActionValidator(
    createConfigurationTreeByRootNode(root),
    DateTime.fromISO(`${endYear}-01-01T10:00:00`),
    deviceMountActions,
    platformMountActions,
    dynamicLocationActions
  )
}

function createDevice (key: string = 'device') {
  const device = new Device()
  device.shortName = key
  return device
}

function createArchivedDevice (key: string = 'device') {
  const device = createDevice(key)
  device.archived = true
  return device
}

function createPlatform (key: string = 'platform') {
  const platform = new Platform()
  platform.shortName = key
  return platform
}

function createArchivedPlatform (key: string = 'platform') {
  const platform = createPlatform(key)
  platform.archived = true
  return platform
}

describe('#single unmounts', () => {
  it('should validate unmounting a single device', () => {
    const rootNode = createConfigurationNode()
    const nodeToUnmount = createDeviceNode(
      createDevice(),
      rootNode
    )

    const validator = createValidatorByRootNodeAndUnmountDate(rootNode, '2005')
    expect(validator.validateNodeUnmount(nodeToUnmount)).toBeTruthy()
  })

  it('should validate unmounting a single platform', () => {
    const rootNode = createConfigurationNode()
    const nodeToUnmount = createPlatformNode(
      createPlatform(),
      rootNode
    )

    const validator = createValidatorByRootNodeAndUnmountDate(rootNode, '2005')
    expect(validator.validateNodeUnmount(nodeToUnmount)).toBeTruthy()
  })

  it('should validate unmounting an archived device', () => {
    const rootNode = createConfigurationNode()
    const nodeToUnmount = createDeviceNode(
      createArchivedDevice(),
      rootNode
    )

    const validator = createValidatorByRootNodeAndUnmountDate(rootNode, '2005')
    expect(validator.validateNodeUnmount(nodeToUnmount)).toBeFalsy()
  })

  it('should validate unmounting an archived platform', () => {
    const rootNode = createConfigurationNode()
    const nodeToUnmount = createPlatformNode(
      createArchivedPlatform(),
      rootNode
    )

    const validator = createValidatorByRootNodeAndUnmountDate(rootNode, '2005')
    expect(validator.validateNodeUnmount(nodeToUnmount)).toBeFalsy()
  })

  it('should validate unmounting a device with archived parent device', () => {
    const rootNode = createConfigurationNode()
    const parentNode = createDeviceNode(
      createArchivedDevice(),
      rootNode
    )
    const nodeToUnmount = createDeviceNode(
      createDevice(),
      parentNode
    )

    const validator = createValidatorByRootNodeAndUnmountDate(rootNode, '2005')
    expect(validator.validateNodeUnmount(nodeToUnmount)).toBeFalsy()
  })

  it('should validate unmounting a device with archived parent platform', () => {
    const rootNode = createConfigurationNode()
    const parentNode = createPlatformNode(
      createArchivedPlatform('parent'),
      null
    )
    const nodeToUnmount = createDeviceNode(
      createDevice('child'),
      parentNode
    )

    const validator = createValidatorByRootNodeAndUnmountDate(rootNode, '2005')
    expect(validator.validateNodeUnmount(nodeToUnmount)).toBeFalsy()
  })

  it('should validate unmounting a platform with archived parent platform', () => {
    const rootNode = createConfigurationNode()
    const parentNode = createPlatformNode(
      createArchivedPlatform(),
      rootNode
    )
    const nodeToUnmount = createPlatformNode(
      createPlatform(),
      parentNode
    )

    const validator = createValidatorByRootNodeAndUnmountDate(rootNode, '2005')
    expect(validator.validateNodeUnmount(nodeToUnmount)).toBeFalsy()
  })
})

describe('#single unmounts with other mount and dynamic locations as context', () => {
  it('should validate unmounting a platform which is later used as parent during same mount', () => {
    /**
     * parent platfrom mount   A---------------A
     *  child platfrom mount        B--------B
     *  invalid unmount date     x
     */
    const rootNode = createConfigurationNode()
    const parentPlatform = new Platform()
    const parentNode = createPlatformNode(
      parentPlatform,
      rootNode,
      '2010',
      null
    )

    const conflictingMountAction = createPlatformMountAction('2030', null, new Platform(), parentPlatform) // mount B
    const platformMountActions: PlatformMountAction[] = [conflictingMountAction]

    const validator = createValidatorByRootNodeAndUnmountDate(rootNode, '2020', [], platformMountActions, [])
    expect(validator.getMountActionWhereNodeIsUsedAsParentBeforeRemounted(parentNode)).toEqual(conflictingMountAction)
    expect(validator.validateNodeUnmount(parentNode)).toBeFalsy()
  })

  it('should validate unmounting a platform which is later used as parent after existing unmount', () => {
    /**
     * platform is mounted twice and used as parent in a later mount action only
     *
     * parent platform mounts   A---------------A    B----------------B
     *  child platform mounts                          C------------C
     *     valid unmount date           x
     */
    const rootNode = createConfigurationNode()
    const parentPlatform = createPlatform()
    const parentNode = createPlatformNode(
      parentPlatform,
      rootNode,
      '2000',
      '2015'
    )
    const platformMountActions: PlatformMountAction[] = [
      createPlatformMountAction('2000', '2015', parentPlatform, null), // mount A
      createPlatformMountAction('2020', '2035', parentPlatform, null), // mount B
      createPlatformMountAction('2025', '2030', new Platform(), parentPlatform) // mount C
    ]

    const validator = createValidatorByRootNodeAndUnmountDate(rootNode, '2010', [], platformMountActions, [])
    validator.validateNodeUnmount(parentNode)
    expect(validator.getMountActionWhereNodeIsUsedAsParentBeforeRemounted(parentNode)).toBeNull()
    expect(validator.validateNodeUnmount(parentNode)).toBeTruthy()
  })

  it('should validate unmounting a device which is later used as parent during same mount', () => { /**
   /**
     *   parent device mount   A---------------A
     *    child device mount        B--------B
     *  invalid unmount date     x
     */
    const rootNode = createConfigurationNode()
    const parentDevice = new Device()
    const parentNode = createDeviceNode(
      parentDevice,
      rootNode,
      '2010',
      null
    )

    const conflictingMountAction = createDeviceMountAction('2030', null, new Device(), parentDevice, null) // mount B
    const deviceMountActions: DeviceMountAction[] = [conflictingMountAction]

    const validator = createValidatorByRootNodeAndUnmountDate(rootNode, '2020', deviceMountActions, [], [])
    expect(validator.getMountActionWhereNodeIsUsedAsParentBeforeRemounted(parentNode)).toEqual(conflictingMountAction)
    expect(validator.validateNodeUnmount(parentNode)).toBeFalsy()
  })

  it('should validate unmounting a device which is later used as parent after existing unmount', () => {
    /**
     * platform is mounted twice and used as parent in a later mount action only
     *
     *  parent device mounts   A---------------A    B----------------B
     *   child device mounts                          C------------C
     *    valid unmount date           x
     */
    const rootNode = createConfigurationNode()
    const parentDevice = createDevice()
    const parentNode = createDeviceNode(
      parentDevice,
      rootNode,
      '2000',
      '2015'
    )
    const deviceMountActions: DeviceMountAction[] = [
      createDeviceMountAction('2000', '2015', parentDevice, null, null), // mount A
      createDeviceMountAction('2020', '2035', parentDevice, null, null), // mount B
      createDeviceMountAction('2025', '2030', new Device(), parentDevice, null) // mount C
    ]

    const validator = createValidatorByRootNodeAndUnmountDate(rootNode, '2010', deviceMountActions, [], [])
    validator.validateNodeUnmount(parentNode)
    expect(validator.getMountActionWhereNodeIsUsedAsParentBeforeRemounted(parentNode)).toBeNull()
    expect(validator.validateNodeUnmount(parentNode)).toBeTruthy()
  })

  it('should validate unmounting a device while used for dynamic location', () => {
    const devicePropertyX = new DeviceProperty()

    const deviceForDynamicLocation = createDevice()
    deviceForDynamicLocation.properties = [devicePropertyX]

    const dynamicLocationAction = new DynamicLocationAction()
    dynamicLocationAction.beginDate = DateTime.fromISO('2000-01-01T10:00:00')
    dynamicLocationAction.endDate = DateTime.fromISO('2020-01-01T10:00:00')
    dynamicLocationAction.x = devicePropertyX

    const rootNode = createConfigurationNode()
    const deviceNode = createDeviceNode(
      deviceForDynamicLocation,
      rootNode,
      '2000',
      null
    )

    const dynamicLocationActions: DynamicLocationAction[] = [dynamicLocationAction]
    const deviceMountActions: DeviceMountAction[] = [createDeviceMountAction('2000', '2020', deviceForDynamicLocation, null, null)]

    const validatorUnmountDuringDynamicLocation = createValidatorByRootNodeAndUnmountDate(rootNode, '2010', deviceMountActions, [], dynamicLocationActions)
    expect(validatorUnmountDuringDynamicLocation.validateNodeUnmount(deviceNode)).toBeFalsy()

    const validatorUnmountAfterDynamicLocation = createValidatorByRootNodeAndUnmountDate(rootNode, '2030', deviceMountActions, [], dynamicLocationActions)
    expect(validatorUnmountAfterDynamicLocation.validateNodeUnmount(deviceNode)).toBeTruthy()
  })

  it('should return existing mounts being overwritten', () => {
    const deviceToOverwriteExistingUnmount = createDevice()
    const yearToOverwrite = '2020'

    const rootNode = createConfigurationNode()
    const deviceNode = createDeviceNode(
      deviceToOverwriteExistingUnmount,
      rootNode,
      '2000',
      yearToOverwrite
    )

    const deviceMountActions: DeviceMountAction[] = [createDeviceMountAction('2000', yearToOverwrite, deviceToOverwriteExistingUnmount, null, null)]

    const validatorUnmountDuringDynamicLocation = createValidatorByRootNodeAndUnmountDate(rootNode, '2040', deviceMountActions, [], [])
    expect(validatorUnmountDuringDynamicLocation.getUnmountEndDateToOverwrite(deviceNode)).toBeNull()

    const validatorUnmountAfterDynamicLocation = createValidatorByRootNodeAndUnmountDate(rootNode, '2010', deviceMountActions, [], [])
    expect(validatorUnmountAfterDynamicLocation.getUnmountEndDateToOverwrite(deviceNode)?.year.toString()).toEqual(yearToOverwrite)
  })
})

describe('#recursive unmounts', () => {
  it('should validate unmounting flat children', () => {
    /**
     * root
     * ├── valid
     * ├── valid
     * ├── valid
     * └── valid
     */
    const rootNode = createConfigurationNode()
    createDeviceNode(
      createDevice(),
      rootNode
    )
    createDeviceNode(
      createDevice(),
      rootNode
    )
    createPlatformNode(
      createPlatform(),
      rootNode
    )
    createPlatformNode(
      createPlatform(),
      rootNode
    )

    const validator = createValidatorByRootNodeAndUnmountDate(rootNode, '2005')
    expect(validator.validateTreeRecursively()).toBeTruthy()
  })

  it('should validate unmounting flat children with at least one invalid child', () => {
    /**
     * root
     * ├── valid
     * ├── valid
     * ├── valid
     * └── invalid
     */
    const rootNode = createConfigurationNode()
    createDeviceNode(
      createDevice(),
      rootNode
    )
    createDeviceNode(
      createDevice(),
      rootNode
    )
    createPlatformNode(
      createPlatform(),
      rootNode
    )
    createPlatformNode(
      createArchivedPlatform(), // invalid
      rootNode
    )

    const validator = createValidatorByRootNodeAndUnmountDate(rootNode, '2005')
    expect(validator.validateTreeRecursively()).toBeFalsy()
  })

  /**
   * root
   * └── valid
   *     └── valid
   *         └── valid
   */
  it('should validate unmounting deep children', () => {
    const rootNode = createConfigurationNode()
    const validPlatform = createPlatformNode(
      createPlatform(),
      rootNode
    )
    const validDevice = createDeviceNode(
      createDevice(),
      validPlatform
    )
    createDeviceNode(
      createDevice(),
      validDevice
    )

    const validator = createValidatorByRootNodeAndUnmountDate(rootNode, '2005')
    expect(validator.validateTreeRecursively()).toBeTruthy()
  })

  /**
   * root
   * └── valid
   *     └── valid
   *         └── invalid
   */
  it('should validate unmounting deep children with at least on invalid nested child', () => {
    const rootNode = createConfigurationNode()
    const validPlatform = createPlatformNode(
      createPlatform(),
      rootNode
    )
    const validDevice = createDeviceNode(
      createDevice(),
      validPlatform
    )
    createDeviceNode(
      createArchivedDevice(), // invalid
      validDevice
    )

    const validator = createValidatorByRootNodeAndUnmountDate(rootNode, '2005')
    expect(validator.validateTreeRecursively()).toBeFalsy()
  })
})
