/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'

import { MountAction } from '@/models/MountAction'

import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'

import { dateToDateTimeString } from '@/utils/dateHelper'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { DynamicLocationAction } from '@/models/DynamicLocationAction'
import { getEntityByConfigurationsTreeNode } from '@/utils/configurationsTreeHelper'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { MountActionValidator } from '@/utils/MountActionValidator'

/**
 * Helper class to validate the unmount of one or multiple ConfigurationTreeNodes recursively in a given context
 */
export class UnmountActionValidator {
  public tree: ConfigurationsTree
  public endDate: DateTime
  public deviceMountActions: DeviceMountAction[]
  public platformMountActions: PlatformMountAction[]
  public dynamicLocationActions: DynamicLocationAction[]

  /**
   * @param {ConfigurationsTreeNode} tree - The configuration tree containing the nodes to validate.
   * @param {DateTime} endDate - The target date for unmounting.
   * @param {DeviceMountAction[]} deviceMountActions - Array of device mount actions from the configuration, used to detect conflicts.
   * @param {PlatformMountAction[]} platformMountActions - Array of platform mount actions from the configuration, used to detect conflicts.
   * @param {DynamicLocationAction[]} dynamicLocationActions - Array of dynamic location actions from the configuration, used to detect conflicts.
   */
  constructor (
    tree: ConfigurationsTree,
    endDate: DateTime,
    deviceMountActions: DeviceMountAction[],
    platformMountActions: PlatformMountAction[],
    dynamicLocationActions: DynamicLocationAction[]
  ) {
    this.tree = tree
    this.endDate = endDate
    this.deviceMountActions = deviceMountActions
    this.platformMountActions = platformMountActions
    this.dynamicLocationActions = dynamicLocationActions
  }

  get allMountActions (): Array<DeviceMountAction|PlatformMountAction> {
    return [...this.platformMountActions, ...this.deviceMountActions]
  }

  /**
   * Validates all nodes within the validator's tree and assigns errors to the corresponding node objects.
   * @returns whether there exist any errors for any of the containing tree nodes.
   */
  public validateTreeRecursively (): boolean {
    this.validateNodeUnmount(this.tree.root)

    for (const node of this.tree.getAllNodesAsList()) {
      this.validateNodeUnmount(node)
    }

    return !this.tree.root.hasErrors && !this.tree.root.hasChildErrors
  }

  /**
   * Validates a single node and assign errors to the corresponding node object.
   * @param {ConfigurationsTreeNode} node - The node to validate.
   * @returns whether there exist any errors for the given node.
   */
  public validateNodeUnmount (node: ConfigurationsTreeNode): boolean {
    node.removeErrors()
    if (node.isConfiguration()) {
      return true
    }

    if (node.isPlatform()) {
      const unpacked = node.unpack() as PlatformMountAction
      if (unpacked.platform.archived) {
        node.addError(`The platform ${node.nameWithoutOffsets} is archived. Please restore it first.`)
      }
      if (unpacked.parentPlatform && unpacked.parentPlatform?.archived) {
        node.addError(`The parent platform (${unpacked.parentPlatform.shortName}) is archived. Please restore it first.`)
      }
      const conflictMount = this.getMountActionWhereNodeIsUsedAsParentBeforeRemounted(node)
      if (conflictMount) {
        node.addError(`The platform ${node.nameWithoutOffsets} is used as parent platform from ${dateToDateTimeString(conflictMount.beginDate)}.`)
      }
    }

    if (node.isDevice()) {
      const unpacked = node.unpack() as DeviceMountAction
      if (unpacked.device.archived) {
        node.addError(`The device ${node.nameWithoutOffsets} is archived. Please restore it first.`)
      }
      if (unpacked.parentPlatform && unpacked.parentPlatform?.archived) {
        node.addError(`The parent platform (${unpacked.parentPlatform.shortName}) is archived. Please restore it first.`)
      }
      if (unpacked.parentDevice && unpacked.parentDevice?.archived) {
        node.addError(`The parent device (${unpacked.parentDevice.shortName}) is archived. Please restore it first.`)
      }
      const conflictMount = this.getMountActionWhereNodeIsUsedAsParentBeforeRemounted(node)
      if (conflictMount) {
        node.addError(`The device ${node.nameWithoutOffsets} is used as parent device from ${dateToDateTimeString(conflictMount.beginDate)}.`)
      }
      // check device mount actions against dynamic location actions
      const actionWithDeviceProperties = this.deviceMountActions.find(a => a.id === node.unpack().id)
      if (actionWithDeviceProperties) {
        // get all dynamic location actions that use properties of the current device mount action
        const dynamicLocationActions = MountActionValidator.getRelatedDynamicLocationActions(actionWithDeviceProperties, this.dynamicLocationActions)
        // create a new device mount action with the selected end date
        const newDeviceMountAction = DeviceMountAction.createFromObject(actionWithDeviceProperties)
        newDeviceMountAction.endDate = this.endDate
        const error = MountActionValidator.isDeviceMountActionCompatibleWithMultipleDynamicLocationActions(newDeviceMountAction, dynamicLocationActions)
        if (typeof error === 'object') {
          node.addError(`The device ${node.nameWithoutOffsets} is still referenced by a dynamic location. Please stop it first.`)
        }
      }
    }

    return !node.hasErrors
  }

  /**
   * Finds the MountAction with the nearest end date after the specified unmount date for a given node
   *
   * Example:
   *  node mounts: A----------A B----------B C----------C
   * unmount date:                   *
   *                                 ^ B is returned
   *
   * @param {ConfigurationsTreeNode | null} node - The node to find corresponding actions for.
   * @returns {DeviceMountAction|PlatformMountAction|null} - The nearest future MountAction if one exists; otherwise, returns null.
   */
  public getFutureUnmountActionForNodeEntity (node: ConfigurationsTreeNode): DeviceMountAction | PlatformMountAction | null {
    if (!node) {
      return null
    }
    const entity = getEntityByConfigurationsTreeNode(node)
    if (!entity || !this.endDate) {
      return null
    }
    let filteredMounts: DeviceMountAction[] | PlatformMountAction[] = []
    if (node.isPlatform()) {
      filteredMounts = this.platformMountActions.filter(mountAction =>
        mountAction.platform?.id === entity.id &&
        mountAction.endDate &&
        mountAction.endDate > this.endDate!
      )
    }
    if (node.isDevice()) {
      filteredMounts = this.deviceMountActions.filter(mountAction =>
        mountAction.device?.id === entity.id &&
        mountAction.endDate &&
        mountAction.endDate > this.endDate!
      )
    }
    const sortedMounts = filteredMounts.sort((a, b) => a.beginDate > b.beginDate ? 1 : -1)
    return sortedMounts.length > 0 ? sortedMounts[0] : null
  }

  /**
   * Finds the MountAction with the nearest start date after the specified time for a given parent node.
   *
   * Example:
   * mounts with given node as parent: A----------A B----------B C----------C
   *                     unmount date:                   *
   *                                                     ^ C is returned
   *
   * @param {ConfigurationsTreeNode | null} node - The node to find corresponding actions for.
   * @returns {DeviceMountAction|PlatformMountAction|null} - The nearest future MountAction if one exists; otherwise, returns null.
   */
  public getFutureMountActionWhereSelectedNodeIsParent (node: ConfigurationsTreeNode | null): DeviceMountAction | PlatformMountAction | null {
    if (!node) {
      return null
    }
    const entity = getEntityByConfigurationsTreeNode(node)
    if (!entity) {
      return null
    }
    let filteredMounts: DeviceMountAction[] | Array<DeviceMountAction | PlatformMountAction> = []
    if (node.isPlatform()) {
      filteredMounts = this.allMountActions.filter(mountAction =>
        mountAction.parentPlatform?.id === entity.id &&
        mountAction.beginDate &&
        mountAction.beginDate > this.endDate
      )
    }
    if (node.isDevice()) {
      filteredMounts = this.deviceMountActions.filter(mountAction =>
        mountAction.parentDevice?.id === entity.id &&
        mountAction.beginDate &&
        mountAction.beginDate > this.endDate
      )
    }
    const sortedMounts = filteredMounts.sort((a, b) => a.beginDate > b.beginDate ? 1 : -1)
    return sortedMounts.length > 0 ? sortedMounts[0] : null
  }

  /**
   * Finds a MountAction that prevents unmounting because it contains a given node as parent it was re-mounted.
   *
   *  Example:
   *  Unmount is invalid if there exists any mount action X with
   *    1. the selected node as parent and
   *    2. a start date later than the date to unmount
   *    3. a start date later that any other unmount U of the selected node
   *
   *             mounts of selected node: [---------------U]
   *  mount with selected node as parent:        X------X
   *                        unmount date:    *
   *                                         ^ invalid
   *
   *             mounts of selected node: [---------------U] [---------------]
   *  mount with selected node as parent:                           X------X
   *                        unmount date:        *              *
   *                                             ^ valid        ^ invalid
   *
   * @param {ConfigurationsTreeNode | null} node - The node to find corresponding actions for.
   * @returns {DeviceMountAction|PlatformMountAction|null} - A MountAction that blocks unmounting if one exists; otherwise, returns null.
   */
  public getMountActionWhereNodeIsUsedAsParentBeforeRemounted (node: ConfigurationsTreeNode): MountAction | null {
    const futureMountActionWhereSelectedNodeIsParent = this.getFutureMountActionWhereSelectedNodeIsParent(node)
    const futureUnmountActionForNodeEntity = this.getFutureUnmountActionForNodeEntity(node)

    if (!futureMountActionWhereSelectedNodeIsParent) {
      return null
    }
    if (!futureUnmountActionForNodeEntity) {
      return futureMountActionWhereSelectedNodeIsParent
    }
    return futureMountActionWhereSelectedNodeIsParent.beginDate < futureUnmountActionForNodeEntity.endDate! ? futureMountActionWhereSelectedNodeIsParent : null
  }

  /**
   * Finds the end date of the MountAction with the nearest end date after the specified time for a given node
   *
   * @param {ConfigurationsTreeNode | null} node - The node to find a corresponding date for.
   * @returns {DeviceMountAction|PlatformMountAction|null} - The nearest future unmount date if one exists; otherwise, returns null.
   */
  public getUnmountEndDateToOverwrite (node: ConfigurationsTreeNode): DateTime | null {
    const nextAction = this.getFutureUnmountActionForNodeEntity(node)
    return nextAction?.endDate ?? null
  }
}
