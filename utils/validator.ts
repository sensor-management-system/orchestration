/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021, 2022
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Tim Eder (UFZ, tim.eder@ufz.de)
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
import { LocationType } from '@/models/Location'
import { Configuration } from '@/models/Configuration'
import { IPermissionGroup } from '@/models/PermissionGroup'
import { Visibility } from '@/models/Visibility'
import { dateToString } from '@/utils/dateHelper'

export default {
  validateInputForStartDate (configuration: Configuration): (v: string) => (boolean | string) {
    return (v) => {
      if (v === null || v === '' || configuration.startDate === null) {
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
      if (v === null || v === '' || configuration.endDate === null) {
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

  validateMountingTimeRange (mountEndDate: DateTime | null, parentEndDate: DateTime | null): (v: string) => (boolean | string) {
    return (v) => {
      if (v === null || v === '' || parentEndDate === null) {
        return true
      }
      if (mountEndDate && mountEndDate <= parentEndDate) {
        return true
      }
      return `End date must be before parent platform end date (${dateToString(parentEndDate)})`
    }
  },

  validateMountingDates (startDate: DateTime, endDate: DateTime | null): (v: string) => (boolean | string) {
    return (v) => {
      if (v === null || v === '' || endDate === null) {
        return true
      }
      if (startDate && startDate <= endDate) {
        return true
      }
      return 'End date must not be before start date'
    }
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
  validatePermissionGroups (isPrivate: boolean, entityName: string): (groups: IPermissionGroup[]) => boolean | string {
    return function (groups: IPermissionGroup[]) {
      if (isPrivate && groups.length) {
        return `You are not allowed to add groups if the ${entityName} is private.`
      }
      if (!isPrivate && !groups.length) {
        return `You must add groups if the ${entityName} is not private.`
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
   * @param {PermissionGroup[]} groups - the permission groups of the entity
   * @param {string} entityName - the entity name
   * @returns {(visibility: Visibility) => boolean | string} a function that validates the visibility of an entity
   */
  validateVisibility (groups: IPermissionGroup[], entityName: string): (visibility: Visibility) => boolean | string {
    return function (visibility: Visibility) {
      if (visibility === Visibility.Private && groups.length) {
        return `You are not allowed to set the visibility to private as long as the ${entityName} has permission groups.`
      }
      return true
    }
  }
}
