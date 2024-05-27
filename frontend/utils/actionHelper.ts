/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DeviceActions, DeviceFilter, IOptionsForActionType, PossibleDeviceActions } from '@/store/devices'
import { IActionKind, KIND_OF_ACTION_TYPE_DEVICE_MOUNT, KIND_OF_ACTION_TYPE_DEVICE_UNMOUNT, KIND_OF_ACTION_TYPE_GENERIC_ACTION, KIND_OF_ACTION_TYPE_PLATFORM_MOUNT, KIND_OF_ACTION_TYPE_PLATFORM_UNMOUNT } from '@/models/ActionKind'
import { GenericAction } from '@/models/GenericAction'
import { IActionCommonDetails } from '@/models/ActionCommonDetails'
import { IDateCompareable } from '@/modelUtils/Compareables'
import { PlatformActions, PlatformFilter, PossiblePlatformActions } from '@/store/platforms'
import { ITimelineAction } from '@/utils/configurationInterfaces'
import { byDateOldestLast, byLogicOrderHighestFirst } from '@/modelUtils/mountHelpers'
import { ConfigurationFilter } from '@/store/configurations'

function matchesContactSelect (action: PossibleDeviceActions, selectedContacts: string[]) {
  let matchesContact = false
  if (selectedContacts.length > 0) {
    if (action.contact === null) {
      matchesContact = false
    } else {
      matchesContact = selectedContacts.includes(action.contact.toString())
    }
  } else {
    matchesContact = true
  }

  return matchesContact
}

function matchesYearSelection (action: PossibleDeviceActions, selectedYears: number[]) {
  let matchesYear = false

  if (selectedYears.length > 0) {
    if (action.date === null) {
      matchesYear = false
    } else if (action.kind === KIND_OF_ACTION_TYPE_GENERIC_ACTION) {
      const genericAction = action as GenericAction
      if (genericAction.endDate) {
        matchesYear = selectedYears.some((year: number) => {
          return genericAction.date!.year <= year && year <= genericAction.endDate!.year
        })
      } else {
        matchesYear = selectedYears.includes(action.date.year)
      }
    } else {
      matchesYear = selectedYears.includes(action.date.year)
    }
  } else {
    matchesYear = true
  }

  return matchesYear
}

function matchesActionTypeSelection (action: PossibleDeviceActions | PossiblePlatformActions | ITimelineAction, selectedActionTypes: IOptionsForActionType[]) {
  let matchesActionType = false

  if (selectedActionTypes.length > 0) {
    matchesActionType = selectedActionTypes.some((selectedActionType: IOptionsForActionType) => {
      if (action.kind === KIND_OF_ACTION_TYPE_GENERIC_ACTION && selectedActionType.kind === KIND_OF_ACTION_TYPE_GENERIC_ACTION) {
        const genericAction = action as GenericAction
        return genericAction.actionTypeUrl === selectedActionType.uri
      }
      return selectedActionType.kind === action.kind
    })
  } else {
    matchesActionType = true
  }

  return matchesActionType
}

export function getDistinctContactsOfActions (actions: IActionCommonDetails[]) {
  const allContacts: string[] = actions.filter((action: IActionCommonDetails) => !!action.contact).map((action: IActionCommonDetails) => {
    return action.contact!.toString()
  })
  const distinctContacts = new Set(allContacts)
  return Array.from(distinctContacts).sort()
}

export function getDistinctYearsOfActions (actions: IActionKind[] | IDateCompareable[]) {
  // @ts-ignore
  const genericActionEndYears = actions.filter((action: IActionKind) => {
    if (action.kind === KIND_OF_ACTION_TYPE_GENERIC_ACTION) {
      const genericAction = action as GenericAction
      if (genericAction.endDate) {
        return true
      }
    }
    return false
  }).map((action: GenericAction) => {
    return action.endDate!.year
  })

  // @ts-ignore
  const allYears: number[] = actions.filter((action: IDateCompareable) => !!action.date).map((action: IDateCompareable) => {
    return action.date!.year
  })

  const mergedYears = [...allYears, ...genericActionEndYears]

  const distinctYears = new Set(mergedYears)
  // create array and sort descening
  return Array.from(distinctYears).sort((a, b) => a - b).reverse()
}

export function sortActions (actions: ITimelineAction[] | PlatformActions | DeviceActions) {
  const actionsCopy = actions.slice()

  const byDateOldestAndUnmountBeforeMount = (a: ITimelineAction | PossiblePlatformActions | PossibleDeviceActions, b: ITimelineAction | PossiblePlatformActions | PossibleDeviceActions): number => {
    const result = byDateOldestLast(a, b)
    if (result !== 0) {
      return result
    }
    if (!('logicOrder' in a) || !('logicOrder' in b)) {
      return result
    }
    // ok, what do we want?

    // We want the following order (from logically most up to date, to oldest):
    // DeviceMount D (DeviceMountAction id=2)
    // PlatformMount P (PlatformMountAction id=2)
    // PlatformUnmount P (PlatformMountAction id=1)
    // DeviceUnmount D (DeviceMountAction id=1)
    // DeviceMount D (DeviceMountAction id=1)
    // PlatformMount P (PlatformMountAction id=1)
    // However, we can't rely on the ascending numbers of the id fields
    // Just about if they are the same or are different.

    // in general we have the following logicOrders (but this may not be up to date...)
    //  PlatformUnmount 400
    //  DeviceUnmount 300
    //  DeviceMount 200
    //  PlatformMount 100

    // So we need some special handling to ensure the mounts and unmounts also
    // consider if they are for the same mount action - or for different ones.

    // As long as compare platform mounts with platform unmounts and
    // device mounts with device unmounts we can use the ids of the associated
    // mount action (that contains the data for both (mount&unmount)).

    if (a.kind === KIND_OF_ACTION_TYPE_PLATFORM_UNMOUNT) {
      if (b.kind === KIND_OF_ACTION_TYPE_PLATFORM_MOUNT) {
        if ('id' in a && 'id' in b) {
          if (a.id === b.id) {
            // It is the very same mount action, so we want to have the mount before
            // the mount
            return -1
          } else {
            return 1
          }
        }
      }
    }
    if (a.kind === KIND_OF_ACTION_TYPE_PLATFORM_MOUNT) {
      if (b.kind === KIND_OF_ACTION_TYPE_PLATFORM_UNMOUNT) {
        if ('id' in a && 'id' in b) {
          if (a.id === b.id) {
            return 1
          } else {
            return -1
          }
        }
      }
    }

    if (a.kind === KIND_OF_ACTION_TYPE_DEVICE_UNMOUNT) {
      if (b.kind === KIND_OF_ACTION_TYPE_DEVICE_MOUNT) {
        if ('id' in a && 'id' in b) {
          if (a.id === b.id) {
            return -1
          } else {
            return 1
          }
        }
      }
    }
    if (a.kind === KIND_OF_ACTION_TYPE_DEVICE_MOUNT) {
      if (b.kind === KIND_OF_ACTION_TYPE_DEVICE_UNMOUNT) {
        if ('id' in a && 'id' in b) {
          if (a.id === b.id) {
            return 1
          } else {
            return -1
          }
        }
      }
    }

    // in any other case, consider the "main" logic order
    return byLogicOrderHighestFirst(a, b)
  }

  return actionsCopy.sort(byDateOldestAndUnmountBeforeMount)
}

export function filterActions (actions: DeviceActions | PlatformActions | ITimelineAction[], filter: DeviceFilter | PlatformFilter | ConfigurationFilter) {
  const {
    selectedActionTypes,
    selectedYears,
    selectedContacts
  } = filter

  // @ts-ignore
  const filteredActions = actions.filter((action: PossibleDeviceActions | PossiblePlatformActions | ITimelineAction) => {
    // @ts-ignore
    return matchesActionTypeSelection(action, selectedActionTypes) && matchesYearSelection(action, selectedYears) && matchesContactSelect(action, selectedContacts)
  })

  return filteredActions
}
