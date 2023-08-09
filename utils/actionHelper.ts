/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
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

import { DeviceActions, DeviceFilter, IOptionsForActionType, PossibleDeviceActions } from '@/store/devices'
import { IActionKind, KIND_OF_ACTION_TYPE_GENERIC_ACTION } from '@/models/ActionKind'
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
