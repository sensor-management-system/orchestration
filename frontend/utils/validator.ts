/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Erik Pongratz <erik.pongratz@ufz.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'
import { LocationType } from '@/models/Location'
import { Configuration } from '@/models/Configuration'
import { IPermissionGroup } from '@/models/PermissionGroup'
import { Visibility } from '@/models/Visibility'
import { dateTimesEqual, dateToDateTimeStringHHMM, dateToString, sortCriteriaAscending } from '@/utils/dateHelper'
import { ILocationTimepoint } from '@/serializers/controller/LocationActionTimepointSerializer'
import { LocationTypes } from '@/store/configurations'
import { getActiveActionOrNull, getEndLocationTimepointForBeginning } from '@/utils/locationHelper'
import { DeviceMountAction } from '@/models/DeviceMountAction'

function sortedTimepoints (timepoints: ILocationTimepoint[]): ILocationTimepoint[] {
  return [...timepoints].sort((a, b) => sortCriteriaAscending(a.timepoint, b.timepoint))
}

export default {
  validateInputForStartDate (configuration: Configuration): (v: string) => (boolean | string) {
    return (v) => {
      if (v === '' || configuration.startDate === null) {
        return true
      }
      if (!configuration.endDate) {
        return true
      }
      if (configuration.startDate <= configuration.endDate) {
        return true
      }
      return 'Start date must not be after end date'
    }
  },

  validateInputForEndDate (configuration: Configuration): (v: string) => (boolean | string) {
    return (v) => {
      if (v === '' || configuration.endDate === null) {
        return true
      }
      if (!configuration.startDate) {
        return true
      }
      if (configuration.endDate >= configuration.startDate) {
        return true
      }
      return 'End date must not be before start date'
    }
  },

  validateMountingTimeRange (startDate: DateTime | null, endDate: DateTime | null, parentStartDate: DateTime, parentEndDate: DateTime | null): boolean | string {
    if (startDate === null) {
      return 'Start date is required'
    }
    if (!(startDate >= parentStartDate)) {
      return `Start date must not be before start date of the parent platform (${dateToString(parentStartDate)})`
    }
    if (parentEndDate) {
      if (!(startDate <= parentEndDate)) {
        return `Start date must be before end date of the parent platform (${dateToString(parentEndDate)})`
      }
      if (endDate && !(endDate >= parentStartDate)) {
        return `End date must be after start date of the parent platform (${dateToString(parentStartDate)})`
      }
      if (!endDate || !(endDate <= parentEndDate)) {
        return `End date must be before end date of the parent platform (${dateToString(parentEndDate)})`
      }
    }
    return true
  },

  validateMountingDates (startDate: DateTime | null, endDate: DateTime | null): boolean | string {
    if (startDate === null) {
      return 'Start date is required'
    }
    if (endDate === null) {
      return true
    }
    if (startDate && startDate <= endDate) {
      return true
    }
    return 'End date must be after start date'
  },

  validateInputForLocationType (v: string): boolean | string {
    if (v === LocationType.Stationary) {
      return true
    }
    if (v === LocationType.Dynamic) {
      return true
    }
    return 'Location type must be set'
  },

  mustBeProvided (fieldname: string): (v: any) => boolean | string {
    return function (v: any) {
      if (v == null || v === '') {
        return fieldname + ' must be provided'
      }
      return true
    }
  },

  /**
   * checks whether the address is an valid email or not
   *
   * @param {string} address - the address to validate
   * @returns {boolean|string} true when valid, otherwise an error message
   */
  isValidEmailAddress (address: string): boolean | string {
    // note: the following false positives are possible:
    // test@--a.de, test@-.a.de
    if (!address.match(/^.+@[a-z0-9-][a-z0-9-.]*[a-z0-9]\.[a-z]{2,}$/i)) {
      //                 ^  ^        ^          ^         ^ the TLD should at least have two characters
      //                 ^  ^        ^          ^ make sure that the domain doesn't end with a '-' or a '.'
      //                 ^  ^        ^ after the first character of the domain the characters 'a-z', '0-9', '-' and '.' are allowed
      //                 ^  ^ the domain should start with either a single letter or digit or a '-'
      //                 ^ before the @ every character is allowed
      return 'The email address is not valid'
    }
    return true
  },

  /**
   * validates the permission groups of an entity
   *
   * If the entity is private, then it is not allowed to have permission groups.
   * If the entity is not private, it is required to have permission groups.
   *
   * @param isPrivate whether the entity has Visibility private. default false
   * @param entityName The entity you are validating, e.g. device, platform, etc...
   * @returns String or boolean that informs the user about possible Permission Group configurations
   */
  validatePermissionGroups (isPrivate: boolean, entityName: string, canBePrivate: boolean = true): (groups: IPermissionGroup[]) => boolean | string {
    return function (groups: IPermissionGroup[]) {
      if (isPrivate && groups.length) {
        return `You are not allowed to add groups if the ${entityName} is private.`
      }
      if (!isPrivate && !groups.length) {
        if (canBePrivate) {
          return `You must add groups if the ${entityName} is not private.`
        }
        return 'You must add groups.'
      }
      return true
    }
  },

  /**
   * validates the permission group of an entity
   *
   * If the entity is private, then it is not allowed to have a permission group.
   * If the entity is not private, it is required to have a permission group.
   *
   * @param isPrivate whether the entity has Visibility private. default false
   * @returns String or boolean that informs the user about possible Permission Group configurations
   */
  validatePermissionGroup (isPrivate: boolean): (group: IPermissionGroup | null) => boolean | string {
    return function (group: IPermissionGroup | null) {
      if (isPrivate && group) {
        return 'You are not allowed to add a group.'
      }
      if (!isPrivate && !group) {
        return 'You must add a group.'
      }
      return true
    }
  },

  /**
   * validates the visibility of an entity
   *
   * If the entity is private, then it is not allowed to have permission groups.
   *
   * @param {Visibility} visibility - the visibility of the entity
   * @param {PermissionGroup[]} groups - the permission groups of the entity
   * @param {string} entityName - the entity name
   * @returns string or boolean that informs the user that he can't set a group in private visibility
   */
  validateVisibility (visibility: Visibility, groups: IPermissionGroup[], entityName: string): boolean | string {
    if (visibility === Visibility.Private && groups.length) {
      return `You are not allowed to set the visibility to private as long as the ${entityName} has permission groups.`
    }
    return true
  },
  canNotStartAnActionAfterAnActiveAction (dateToValidate: DateTime | null, locationTimepoints: ILocationTimepoint[]) {
    const activeAction = getActiveActionOrNull(locationTimepoints)

    if (activeAction == null) {
      return true
    }

    if (dateToValidate == null) {
      return true
    }

    return activeAction.timepoint < dateToValidate ? 'Must be before ' + dateToDateTimeStringHHMM(activeAction.timepoint) : true
  },
  canNotIntersectWithExistingInterval (dateToValidate: DateTime | null, locationTimepoints: ILocationTimepoint[]) {
    if (dateToValidate === null) {
      return true
    }

    if (locationTimepoints.length === 0) {
      return true
    }

    // In order to make the test easier, we want to make sure we have a sorted array of locationTimepoints.
    // In general those values should be sorted by the backend site, but in order to be robust
    // (also regarding to future changes), we should make sure that it sorted.
    const sortedlocationTimepoints = sortedTimepoints(locationTimepoints)

    const filteredArray = sortedlocationTimepoints.filter((item: ILocationTimepoint) => {
      return item.timepoint <= dateToValidate!
    })
    // If the last action is a start action, then it is invalid.
    if (filteredArray.length > 0) {
      const lastEntry = filteredArray[filteredArray.length - 1] as ILocationTimepoint

      const correspondingEndAction = getEndLocationTimepointForBeginning(lastEntry, sortedlocationTimepoints)

      if (correspondingEndAction) {
        return 'Must be before ' + dateToDateTimeStringHHMM(lastEntry.timepoint) + ' or after ' + dateToDateTimeStringHHMM(correspondingEndAction.timepoint) + ' (of existing location action)'
      }

      if (lastEntry.type === LocationTypes.staticEnd || lastEntry.type === LocationTypes.dynamicEnd) {
        if (dateTimesEqual(lastEntry.timepoint, dateToValidate)) {
          return 'Must be after ' + dateToDateTimeStringHHMM(lastEntry.timepoint)
        }
      }
    }
    return true
  },
  validateStartDateIsBeforeEndDate (startDate: DateTime | null, endDate: DateTime | null) {
    if (!startDate) {
      return true
    }
    if (!endDate) {
      return true
    }

    if (startDate >= endDate) {
      return 'Start date must not be after end date'
    }

    return true
  },
  endDateMustBeBeforeNextAction (startDate: DateTime | null, endDate: DateTime|null, locationTimepoints: ILocationTimepoint[]) {
    if (!startDate) {
      return true
    }

    const sortedlocationTimepoints = sortedTimepoints(locationTimepoints)

    const filteredArray = sortedlocationTimepoints.filter((item: ILocationTimepoint) => {
      return item.timepoint > startDate
    })

    if (filteredArray.length === 0) {
      return true
    }

    // the endDate has to be before the timepoint of the first entry of the location timepoint list
    if (!endDate) {
      return 'End date must be before ' + dateToDateTimeStringHHMM(filteredArray[0].timepoint) + ' (next action)'
    }

    if (endDate >= filteredArray[0].timepoint) {
      return 'End date must be before ' + dateToDateTimeStringHHMM(filteredArray[0].timepoint) + ' (next action)'
    }

    return true
  },
  startDateMustBeAfterPreviousAction (startDate: DateTime | null, endDate: DateTime | null, locationTimepoints: ILocationTimepoint[]) {
    if (!startDate) {
      return true
    }
    if (!endDate) {
      return true
    }

    const sortedlocationTimepoints = sortedTimepoints(locationTimepoints)

    const filteredArray = sortedlocationTimepoints.filter((item: ILocationTimepoint) => {
      return item.timepoint < endDate
    })

    if (filteredArray.length === 0) {
      return true
    }

    if (startDate <= filteredArray[filteredArray.length - 1].timepoint) {
      return 'Start date must be after ' + dateToDateTimeStringHHMM(filteredArray[filteredArray.length - 1].timepoint)
    }

    return true
  },
  endDateMustBeBeforeEndOfMountAction (endDate: DateTime | null, action: DeviceMountAction | undefined) {
    if (!action?.endDate) {
      return true
    }
    if (!endDate) {
      return 'End date must be before ' + dateToDateTimeStringHHMM(action.endDate) + ' (end of mount)'
    }

    if (endDate > action.endDate) {
      return 'End date must be before ' + dateToDateTimeStringHHMM(action.endDate) + ' (end of mount)'
    }

    return true
  },
  startDateMustBeAfterStartOfMountAction (startDate: DateTime | null, action: DeviceMountAction | undefined) {
    if (!action) {
      return true
    }
    if (!startDate) {
      return 'Start date must be after ' + dateToDateTimeStringHHMM(action.beginDate) + ' (begin of mount)'
    }
    if (startDate < action.beginDate) {
      return 'Start date must be after ' + dateToDateTimeStringHHMM(action.beginDate) + ' (begin of mount)'
    }

    return true
  },
  endDateMustBeBeforeEndDateOfRelatedDevice (endDateOfDynamicAction: DateTime | null, earliestEndDateOfRelatedDevice: DateTime | null) {
    if (!earliestEndDateOfRelatedDevice && !endDateOfDynamicAction) {
      return true
    }

    if (!endDateOfDynamicAction && earliestEndDateOfRelatedDevice != null) {
      return 'End date must be before ' + dateToDateTimeStringHHMM(earliestEndDateOfRelatedDevice) + ' (planned unmount).'
    }

    if ((endDateOfDynamicAction && earliestEndDateOfRelatedDevice) && endDateOfDynamicAction > earliestEndDateOfRelatedDevice) {
      return 'End date must be before ' + dateToDateTimeStringHHMM(earliestEndDateOfRelatedDevice) + ' (planned unmount).'
    }
    return true
  },
  dateMustBeInRangeOfConfigurationDates (configuration: Configuration|null, dateToValidate: DateTime|null) {
    if (!configuration || !dateToValidate) {
      return true
    }

    if ((!configuration.endDate && configuration.startDate) && (dateToValidate < configuration.startDate)) {
      return 'Date must be after ' + dateToDateTimeStringHHMM(configuration.startDate) + ' ( start date of configuration)'
    }

    if ((!configuration.startDate && configuration.endDate) && (dateToValidate > configuration.endDate)) {
      return 'Date must be before ' + dateToDateTimeStringHHMM(configuration.endDate) + ' ( end date of configuration)'
    }

    if ((configuration.startDate && configuration.endDate) && (dateToValidate < configuration.startDate || dateToValidate > configuration.endDate)) {
      return 'Date must be in the range of ' + dateToDateTimeStringHHMM(configuration.startDate) + ' -- ' + dateToDateTimeStringHHMM(configuration.endDate) + ' (dates of configuration)'
    }

    return true
  }
}
