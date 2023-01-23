/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
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
import Validator from '@/utils/validator'
import { ILocationTimepoint } from '@/serializers/controller/LocationActionTimepointSerializer'
import { LocationTypes } from '@/store/configurations'
import { IPermissionGroup, PermissionGroup } from '@/models/PermissionGroup'

const isValidEmailAddress = Validator.isValidEmailAddress
const startDateMustBeAfterPreviousAction = Validator.startDateMustBeAfterPreviousAction
const endDateMustBeBeforeNextAction = Validator.endDateMustBeBeforeNextAction
const validateStartDateIsBeforeEndDate = Validator.validateStartDateIsBeforeEndDate
const canNotIntersectWithExistingInterval = Validator.canNotIntersectWithExistingInterval
const canNotStartAnActionAfterAnActiveAction = Validator.canNotStartAnActionAfterAnActiveAction

describe('#isValidEmailAddress()', () => {
  it('should return true with an valid email address', () => {
    const email = 'john.doe@gfz-potsdam.de'
    expect(isValidEmailAddress(email)).toBeTruthy()
  })
  it('should return true with some more interesting email addresses', () => {
    // bob@⚔️.gg
    const email1 = 'xn--bob@-y13b.gg'
    expect(isValidEmailAddress(email1)).toBeTruthy()

    // max@müller.de
    const email2 = 'xn--max@mller-u9a.de'
    expect(isValidEmailAddress(email2)).toBeTruthy()
  })
  it('should return true with an valid email address with subdomains', () => {
    const email = 'john.doe@mail.gfz-potsdam.de'
    expect(isValidEmailAddress(email)).toBeTruthy()
  })
  it('should return false with invalid TLD', () => {
    const email1 = 'john.doe@gfz-potsdam'
    expect(typeof isValidEmailAddress(email1)).toBe('string')

    const email2 = 'john.doe@gfz-potsdam.'
    expect(typeof isValidEmailAddress(email2)).toBe('string')

    const email3 = 'john.doe@gfz-potsdam.d'
    expect(typeof isValidEmailAddress(email3)).toBe('string')
  })
  it('should return false with invalid domain', () => {
    const email1 = 'john.doe@.de'
    expect(typeof isValidEmailAddress(email1)).toBe('string')

    const email2 = 'john.doe@-.de'
    expect(typeof isValidEmailAddress(email2)).toBe('string')
  })
  it('should return false with no recipent', () => {
    const email1 = '@gfz-potsdam.de'
    expect(typeof isValidEmailAddress(email1)).toBe('string')
  })
})

describe('#startDateMustBeAfterPreviousAction', () => {
  it('should return true if no locations actions exists', () => {
    const checkDate = DateTime.fromISO('1990-09-19', { zone: 'UTC' })
    const endDate = DateTime.fromISO('1990-09-20', { zone: 'UTC' })
    const locationTimepoints: ILocationTimepoint[] = []
    expect(startDateMustBeAfterPreviousAction(checkDate, endDate, locationTimepoints)).toBeTruthy()
  })
  it('should return true if the new location dates are before the existing ones', () => {
    const checkDate = DateTime.fromISO('1990-09-19', { zone: 'UTC' })
    const endDate = DateTime.fromISO('1990-09-20', { zone: 'UTC' })

    const date1 = DateTime.fromISO('1990-09-21', { zone: 'UTC' })
    const date2 = DateTime.fromISO('1990-09-22', { zone: 'UTC' })
    const locationTimepoints: ILocationTimepoint[] = [
      {
        type: LocationTypes.staticStart,
        timepoint: date1,
        id: '1',
        text: 'not important for test'
      },
      {
        type: LocationTypes.staticEnd,
        timepoint: date2,
        id: '1',
        text: 'not important for test'
      }
    ]
    expect(startDateMustBeAfterPreviousAction(checkDate, endDate, locationTimepoints)).toBeTruthy()
  })
  it('should return true if the new location dates are after the existing ones', () => {
    const checkDate = DateTime.fromISO('1990-09-19', { zone: 'UTC' })
    const endDate = DateTime.fromISO('1990-09-20', { zone: 'UTC' })

    const date1 = DateTime.fromISO('1990-09-17', { zone: 'UTC' })
    const date2 = DateTime.fromISO('1990-09-18', { zone: 'UTC' })
    const locationTimepoints: ILocationTimepoint[] = [
      {
        type: LocationTypes.staticStart,
        timepoint: date1,
        id: '1',
        text: 'not important for test'
      },
      {
        type: LocationTypes.staticEnd,
        timepoint: date2,
        id: '1',
        text: 'not important for test'
      }
    ]
    expect(startDateMustBeAfterPreviousAction(checkDate, endDate, locationTimepoints)).toBeTruthy()
  })

  it('should throw a validation error if the startdate is before the previous action', () => {
    const date1 = DateTime.fromISO('1990-09-18', { zone: 'UTC' })
    const date2 = DateTime.fromISO('1990-09-19', { zone: 'UTC' })

    const locationTimepoints: ILocationTimepoint[] = [
      {
        type: LocationTypes.staticStart,
        timepoint: date1,
        id: '1',
        text: 'not important for test'
      },
      {
        type: LocationTypes.staticEnd,
        timepoint: date2,
        id: '1',
        text: 'not important for test'
      }
    ]
    const checkDate = DateTime.fromISO('1990-09-19', { zone: 'UTC' })
    const endDate = DateTime.fromISO('1990-09-20', { zone: 'UTC' })
    expect(startDateMustBeAfterPreviousAction(checkDate, endDate, locationTimepoints)).toBe('Start date must be after ' + date2.setZone('UTC').toFormat('yyyy-MM-dd HH:mm'))
  })
})
describe('#endDateMustBeBeforeNextAction', () => {
  it('should return true if no location actions exists', () => {
    const checkDate = DateTime.fromISO('1990-09-19', { zone: 'UTC' })
    const endDate = DateTime.fromISO('1990-09-20', { zone: 'UTC' })
    const locationTimepoints: ILocationTimepoint[] = []
    expect(endDateMustBeBeforeNextAction(checkDate, endDate, locationTimepoints)).toBeTruthy()
  })
  it('should return true if the new location dates are before the existing ones', () => {
    const checkDate = DateTime.fromISO('1990-09-19', { zone: 'UTC' })
    const endDate = DateTime.fromISO('1990-09-20', { zone: 'UTC' })

    const date1 = DateTime.fromISO('1990-09-21', { zone: 'UTC' })
    const date2 = DateTime.fromISO('1990-09-22', { zone: 'UTC' })
    const locationTimepoints: ILocationTimepoint[] = [
      {
        type: LocationTypes.staticStart,
        timepoint: date1,
        id: '1',
        text: 'not important for test'
      },
      {
        type: LocationTypes.staticEnd,
        timepoint: date2,
        id: '1',
        text: 'not important for test'
      }
    ]
    expect(endDateMustBeBeforeNextAction(checkDate, endDate, locationTimepoints)).toBeTruthy()
  })
  it('should return true if the new location dates are after the existing ones', () => {
    const checkDate = DateTime.fromISO('1990-09-19', { zone: 'UTC' })
    const endDate = DateTime.fromISO('1990-09-20', { zone: 'UTC' })

    const date1 = DateTime.fromISO('1990-09-17', { zone: 'UTC' })
    const date2 = DateTime.fromISO('1990-09-18', { zone: 'UTC' })
    const locationTimepoints: ILocationTimepoint[] = [
      {
        type: LocationTypes.staticStart,
        timepoint: date1,
        id: '1',
        text: 'not important for test'
      },
      {
        type: LocationTypes.staticEnd,
        timepoint: date2,
        id: '1',
        text: 'not important for test'
      }
    ]
    expect(endDateMustBeBeforeNextAction(checkDate, endDate, locationTimepoints)).toBeTruthy()
  })

  it('should throw a validation error if the enddate is after the next action', () => {
    const checkDate = DateTime.fromISO('1990-09-19', { zone: 'UTC' })
    const endDate = DateTime.fromISO('1990-09-21', { zone: 'UTC' })

    const date1 = DateTime.fromISO('1990-09-21', { zone: 'UTC' })
    const date2 = DateTime.fromISO('1990-09-22', { zone: 'UTC' })

    const locationTimepoints: ILocationTimepoint[] = [
      {
        type: LocationTypes.staticStart,
        timepoint: date1,
        id: '1',
        text: 'not important for test'
      },
      {
        type: LocationTypes.staticEnd,
        timepoint: date2,
        id: '1',
        text: 'not important for test'
      }
    ]
    expect(endDateMustBeBeforeNextAction(checkDate, endDate, locationTimepoints)).toBe('End date must be before ' + date1.setZone('UTC').toFormat('yyyy-MM-dd HH:mm') + ' (next action)')
  })
})

describe('#validateStartDateIsBeforeEndDate', () => {
  it('should return true if startDate is missing', () => {
    const startDate = null
    const endDate = DateTime.fromISO('1990-09-20', { zone: 'UTC' })
    expect(validateStartDateIsBeforeEndDate(startDate, endDate)).toBeTruthy()
  })

  it('should return true if endDate is missing', () => {
    const startDate = null
    const endDate = DateTime.fromISO('1990-09-20', { zone: 'UTC' })
    expect(validateStartDateIsBeforeEndDate(startDate, endDate)).toBeTruthy()
  })

  it('should return true if startDate is before endDate', () => {
    const startDate = DateTime.fromISO('1990-09-19', { zone: 'UTC' })
    const endDate = DateTime.fromISO('1990-09-20', { zone: 'UTC' })
    expect(validateStartDateIsBeforeEndDate(startDate, endDate)).toBeTruthy()
  })
  it('should return a validation error if startDate is after endDate', () => {
    const startDate = DateTime.fromISO('1990-09-19', { zone: 'UTC' })
    const endDate = DateTime.fromISO('1990-09-18', { zone: 'UTC' })
    expect(validateStartDateIsBeforeEndDate(startDate, endDate)).toBe('Start date must not be after end date')
  })
})
describe('#canNotIntersectWithExistingInterval', () => {
  it('should return true if startDate is missing', () => {
    const startDate = null
    const locationTimepoints: ILocationTimepoint[] = []

    expect(canNotIntersectWithExistingInterval(startDate, locationTimepoints)).toBeTruthy()
  })
  it('should return true if no locations exists', () => {
    const startDate = DateTime.fromISO('1990-09-19', { zone: 'UTC' })
    const locationTimepoints: ILocationTimepoint[] = []

    expect(canNotIntersectWithExistingInterval(startDate, locationTimepoints)).toBeTruthy()
  })
  it('should return a validation error when the startDate is intersecting with an existing location action', () => {
    const startDate = DateTime.fromISO('1990-09-21', { zone: 'UTC' })

    const date1 = DateTime.fromISO('1990-09-20', { zone: 'UTC' })
    const date2 = DateTime.fromISO('1990-09-22', { zone: 'UTC' })
    const locationTimepoints: ILocationTimepoint[] = [
      {
        type: LocationTypes.staticStart,
        timepoint: date1,
        id: '1',
        text: 'not important for test'
      },
      {
        type: LocationTypes.staticEnd,
        timepoint: date2,
        id: '1',
        text: 'not important for test'
      }
    ]

    const expectedValidationMessage = 'Must be before ' + date1.setZone('UTC').toFormat('yyyy-MM-dd HH:mm') + ' or after ' + date2.setZone('UTC').toFormat('yyyy-MM-dd HH:mm')
    expect(canNotIntersectWithExistingInterval(startDate, locationTimepoints)).toBe(expectedValidationMessage)
  })

  it('should return a validation error when the startDate is the same es the end date of an existing location action', () => {
    const startDate = DateTime.fromISO('1990-09-21', { zone: 'UTC' })

    const date1 = DateTime.fromISO('1990-09-20', { zone: 'UTC' })
    const date2 = DateTime.fromISO('1990-09-21', { zone: 'UTC' })
    const locationTimepoints: ILocationTimepoint[] = [
      {
        type: LocationTypes.staticStart,
        timepoint: date1,
        id: '1',
        text: 'not important for test'
      },
      {
        type: LocationTypes.staticEnd,
        timepoint: date2,
        id: '1',
        text: 'not important for test'
      }
    ]

    const expectedValidationMessage = 'Must be after ' + date2.setZone('UTC').toFormat('yyyy-MM-dd HH:mm')
    expect(canNotIntersectWithExistingInterval(startDate, locationTimepoints)).toBe(expectedValidationMessage)
  })
})

describe('#canNotStartAnActionAfterAnActiveAction', () => {
  it('should return true if dateToValidate is null', () => {
    const dateToCheck = null

    const date1 = DateTime.fromISO('1990-09-21', { zone: 'UTC' })
    const locationTimepoints: ILocationTimepoint[] = [
      {
        type: LocationTypes.staticStart,
        timepoint: date1,
        id: '1',
        text: 'not important for test'
      }
    ]
    expect(canNotStartAnActionAfterAnActiveAction(dateToCheck, locationTimepoints)).toBeTruthy()
  })

  it('should return true if no location actions exist', () => {
    const dateToCheck = DateTime.fromISO('1990-09-21', { zone: 'UTC' })
    const locationTimepoints: ILocationTimepoint[] = []
    expect(canNotStartAnActionAfterAnActiveAction(dateToCheck, locationTimepoints)).toBeTruthy()
  })

  it('should return true if no active action exist', () => {
    const dateToCheck = DateTime.fromISO('1990-09-23', { zone: 'UTC' })

    const date1 = DateTime.fromISO('1990-09-21', { zone: 'UTC' })
    const date2 = DateTime.fromISO('1990-09-22', { zone: 'UTC' })

    const locationTimepoints: ILocationTimepoint[] = [
      {
        type: LocationTypes.staticStart,
        timepoint: date1,
        id: '1',
        text: 'not important for test'
      },
      {
        type: LocationTypes.staticEnd,
        timepoint: date2,
        id: '1',
        text: 'not important for test'
      }
    ]
    expect(canNotStartAnActionAfterAnActiveAction(dateToCheck, locationTimepoints)).toBeTruthy()
  })
  it('should return validation error if the date is after an active action', () => {
    const dateToCheck = DateTime.fromISO('1990-09-23', { zone: 'UTC' })

    const date1 = DateTime.fromISO('1990-09-21', { zone: 'UTC' })

    const locationTimepoints: ILocationTimepoint[] = [
      {
        type: LocationTypes.staticStart,
        timepoint: date1,
        id: '1',
        text: 'not important for test'
      }
    ]
    expect(canNotStartAnActionAfterAnActiveAction(dateToCheck, locationTimepoints)).toBe('Must be before ' + date1.setZone('UTC').toFormat('yyyy-MM-dd HH:mm'))
  })
})

describe('#validatePermissionGroups', () => {
  it('should return true for a non private thing with groups', () => {
    const groups = [PermissionGroup.createFromObject({
      id: '1',
      name: 'Test group 1',
      description: 'abc'
    })]
    const isPrivate = false
    const checkFunction = Validator.validatePermissionGroups(isPrivate, 'device')
    const result = checkFunction(groups)
    expect(result).toBe(true)
  })
  it('should return true for a private thing without groups', () => {
    const groups: IPermissionGroup[] = []
    const isPrivate = true
    const checkFunction = Validator.validatePermissionGroups(isPrivate, 'device')
    const result = checkFunction(groups)
    expect(result).toBe(true)
  })
  it('should tell me that I can\'t add groups to a private entity', () => {
    const groups = [PermissionGroup.createFromObject({
      id: '1',
      name: 'Test group 1',
      description: 'abc'
    })]
    const isPrivate = true
    const checkFunction = Validator.validatePermissionGroups(isPrivate, 'device')
    const result = checkFunction(groups)
    expect(result).toEqual('You are not allowed to add groups if the device is private.')
  })
  it('should tell me that I need to add groups to a non private entity', () => {
    const groups: IPermissionGroup[] = []
    const isPrivate = false
    const checkFunction = Validator.validatePermissionGroups(isPrivate, 'device')
    const result = checkFunction(groups)
    expect(result).toEqual('You must add groups if the device is not private.')
  })
  it('should tell me that I need to add groups if the entity can\'t be private (different wording)', () => {
    /* Not all the permission group managable entites are allowed to be private.
       For sites this is not allowed.
       We don't want to show the message here that would claim somehow that the
       thing must be private.
    */
    const groups: IPermissionGroup[] = []
    const isPrivate = false
    const canBePrivate = false
    const checkFunction = Validator.validatePermissionGroups(isPrivate, 'site', canBePrivate)
    const result = checkFunction(groups)
    expect(result).toEqual('You must add groups.')
  })
})
