/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2022
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Tim Eder (UFZ, tim.eder@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
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

import { MountAction } from '@/models/MountAction'

import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/viewmodels/ConfigurationsTreeNode'

import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'
import { Availability } from '@/models/Availability'

export enum MountActionValidationResultOp {
  GREATER_THAN = '>',
  LESS_THAN = '<',
  EMPTY = 'empty'
}

export interface IMountActionValidationResult {
  property: keyof Pick<MountAction, 'beginDate' | 'endDate'>
  targetProperty: keyof Pick<MountAction, 'beginDate' | 'endDate'>
  value: DateTime | null
  targetValue: DateTime | null
  op: MountActionValidationResultOp
}

/**
 * Helper class to model an error for validated timeranges in `MountAction` objects
 * @implements IMountActionValidationResult
 */
export class MountActionValidationResult implements IMountActionValidationResult {
  public readonly property: keyof Pick<MountAction, 'beginDate' | 'endDate'>
  public readonly targetProperty: keyof Pick<MountAction, 'beginDate' | 'endDate'>
  public readonly value: DateTime | null
  public readonly targetValue: DateTime | null
  public readonly op: MountActionValidationResultOp

  constructor (result: IMountActionValidationResult) {
    this.property = result.property
    this.targetProperty = result.targetProperty
    this.value = result.value
    this.targetValue = result.targetValue
    this.op = result.op
  }
}

/**
 * Helper class to validate the time ranges of `MountAction`s or `ConfigurationTreeNode`s in a `ConfigurationsTree`
 */
export class MountActionValidator {
  private _tree: ConfigurationsTree

  constructor (tree: ConfigurationsTree) {
    this._tree = tree
  }

  /**
   * returns an (human readable) error message from a given validation error object
   *
   * @static
   * @param {IMountActionValidationResult} error - the error object to build the message from
   * @returns {string} a (hopefully) human readable error message
   */
  public static buildErrorMessage (error: IMountActionValidationResult): string {
    const op = MountActionValidationResultOp
    const toWords = MountActionValidator._camelCaseToWords
    const toDateString = dateToDateTimeStringHHMM

    if (error.op === op.EMPTY) {
      return toWords(error.property) + ' must not be empty'
    }
    if (error.op === op.GREATER_THAN) {
      return toWords(error.property) + ' (' + toDateString(error.value) + ')' + ' must be before ' + toWords(error.targetProperty) + ' (' + toDateString(error.targetValue) + ')'
    }
    if (error.op === op.LESS_THAN) {
      return toWords(error.property) + ' (' + toDateString(error.value) + ')' + ' must be after ' + toWords(error.targetProperty) + ' (' + toDateString(error.targetValue) + ')'
    }
    return 'unknown error'
  }

  /**
   * converts camel case words into separated words
   *
   * used to convert property names like `beginDate` to human readable names
   * like `begin date`
   *
   * @static
   * @param {string} text - the camel case text to convert
   * @returns {string} the converted text splitted into words
   */
  private static _camelCaseToWords (text: string): string {
    return text.replace(/([a-z])([A-Z])/g, '$1 $2').toLowerCase()
  }

  /**
   * validates, if the timerange of an action intersects with the timerange another action
   *
   * @static
   * @param {MountAction} action - the action to validate
   * @param {MountAction} otherAction - an action to validate against
   * @returns {boolean | IMountActionValidationResult} returns `true` if the timeranges do not intersect, otherwise an error object
   */
  public static actionConflictsWith (action: MountAction, otherAction: MountAction): boolean | IMountActionValidationResult {
    if (!(action.beginDate >= otherAction.beginDate)) {
      return new MountActionValidationResult({
        property: 'beginDate',
        targetProperty: 'beginDate',
        value: action.beginDate,
        targetValue: otherAction.beginDate,
        op: MountActionValidationResultOp.LESS_THAN
      })
    }
    if (!otherAction.endDate) {
      return true
    }
    if (!(action.beginDate <= otherAction.endDate)) {
      return new MountActionValidationResult({
        property: 'beginDate',
        targetProperty: 'endDate',
        value: action.beginDate,
        targetValue: otherAction.endDate,
        op: MountActionValidationResultOp.GREATER_THAN
      })
    }
    if (action.endDate && !(action.endDate >= otherAction.beginDate)) {
      return new MountActionValidationResult({
        property: 'endDate',
        targetProperty: 'beginDate',
        value: action.endDate,
        targetValue: otherAction.beginDate,
        op: MountActionValidationResultOp.LESS_THAN
      })
    }
    if (action.endDate && !(action.endDate <= otherAction.endDate)) {
      return new MountActionValidationResult({
        property: 'endDate',
        targetProperty: 'endDate',
        value: action.endDate,
        targetValue: otherAction.endDate,
        op: MountActionValidationResultOp.GREATER_THAN
      })
    }
    if (!action.endDate) {
      return new MountActionValidationResult({
        property: 'endDate',
        targetProperty: 'endDate',
        value: action.endDate,
        targetValue: otherAction.endDate,
        op: MountActionValidationResultOp.EMPTY
      })
    }
    return true
  }

  /**
   * validates, if the timerange of an action intersects with the timerange another action
   *
   * if the check encounters an error, the error is returned immediately and the other actions are not checked.
   *
   * @static
   * @param {MountAction} action - the action to validate
   * @param {MountAction[]} otherActions - an `Array` of actions to validate against
   * @returns {boolean | IMountActionValidationResult} returns `true` if the timeranges do not intersect, otherwise an error object
   */
  public static actionConflictsWithMultiple (action: MountAction, otherActions: MountAction[]): boolean | MountActionValidationResult {
    for (const otherAction of otherActions) {
      const result = MountActionValidator.actionConflictsWith(otherAction, action)
      if (result !== true) {
        return result // we can stop with the first negative test
      }
    }
    return true
  }

  public static actionAvailableIn (action: MountAction, availabilities: Availability[]): boolean | MountActionValidationResult {
    for (const availability of availabilities) {
      if (availability.available) {
        continue
      }
      // we know that at least the `beginDate` property exists, if `available`
      // is set to false, so the following statement is just to supress the
      // compiler warnings ;-)
      if (!availability.beginDate) {
        continue
      }

      // no action `endDate` but action `beginDate` before the timeranges when not available
      //    |--------*
      // ^ begin
      if (action.beginDate && !action.endDate && action.beginDate < availability.beginDate) {
        return new MountActionValidationResult({
          property: 'endDate',
          targetProperty: 'beginDate',
          value: action.endDate,
          targetValue: availability.beginDate,
          op: MountActionValidationResultOp.EMPTY
        })
      }
      // action `beginDate` in the timerange when not available
      //    |--------*
      //      ^ begin
      if (action.beginDate >= availability.beginDate && (!availability.endDate || action.beginDate <= availability.endDate)) {
        return new MountActionValidationResult({
          property: 'beginDate',
          targetProperty: 'beginDate',
          value: action.beginDate,
          targetValue: availability.beginDate,
          op: MountActionValidationResultOp.GREATER_THAN
        })
      }
      // action `endDate` in the timerange when not available
      //    |--------*
      //          ^ end
      if (action.endDate && action.endDate >= availability.beginDate && (!availability.endDate || action.endDate <= availability.endDate)) {
        return new MountActionValidationResult({
          property: 'endDate',
          targetProperty: 'beginDate',
          value: action.endDate,
          targetValue: availability.beginDate,
          op: MountActionValidationResultOp.GREATER_THAN
        })
      }
      // action `beginDate` before and action `endDate` after the timerange when not available
      //    |--------|
      // ^ begin       ^ end
      if (action.beginDate < availability.beginDate && action.endDate && availability.endDate && action.endDate > availability.endDate) {
        return new MountActionValidationResult({
          property: 'endDate',
          targetProperty: 'endDate',
          value: action.endDate,
          targetValue: availability.endDate,
          op: MountActionValidationResultOp.GREATER_THAN
        })
      }
    }
    return true
  }

  /**
   * validates, if the timerange of the `MountAction` of a node intersects with
   * the timerange of the `MountAction` of its parent node
   *
   * @param {ConfigurationsTreeNode} node - the node to validate
   * @returns {boolean | IMountActionValidationResult} returns `true` if the timeranges are valid, otherwise an error object
   */
  public nodeIsWithinParentRange (node: ConfigurationsTreeNode): boolean | MountActionValidationResult {
    const parent = this._tree.getParent(node)
    if (!parent) {
      return true
    }
    return MountActionValidator.actionConflictsWith(node.unpack(), parent.unpack())
  }

  /**
   * validates, if the timerange of the `MountAction` of all childrens of a
   * node intersects with the timerange of the `MountAction` of the node
   *
   * @param {ConfigurationsTreeNode} node - the node to validate
   * @returns {boolean | IMountActionValidationResult} returns `true` if the timeranges are valid, otherwise an error object
   */
  public nodeChildrenAreWithinRange (node: ConfigurationsTreeNode): boolean | MountActionValidationResult {
    if (!node.canHaveChildren() || !node.children.length) {
      return true
    }
    const children: MountAction[] = []
    // collect all children (not only the direct ones)
    const getChildrenRecursive = (parent: ConfigurationsTreeNode, collected: MountAction[]): void => {
      if (!parent.canHaveChildren()) {
        return
      }
      parent.children.map(i => i.unpack()).forEach(i => collected.push(i))
      parent.children.forEach(i => getChildrenRecursive(i, collected))
    }
    getChildrenRecursive(node, children)
    return MountActionValidator.actionConflictsWithMultiple(node.unpack(), children)
  }
}
