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
import { LocationType } from '@/models/Location'
import { Configuration } from '@/models/Configuration'

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
  }
}
