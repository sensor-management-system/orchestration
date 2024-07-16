/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'
import Validator from '@/utils/validator'
import { ILocationTimepoint } from '@/serializers/controller/LocationActionTimepointSerializer'
import { LocationTypes } from '@/store/configurations'
import { IPermissionGroup, PermissionGroup } from '@/models/PermissionGroup'
import { Configuration } from '@/models/Configuration'
import { dateToDateTimeStringHHMM, dateToString } from '@/utils/dateHelper'
import { LocationType } from '@/models/Location'
import { Visibility } from '@/models/Visibility'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Device } from '@/models/Device'
import { Contact } from '@/models/Contact'

const isValidEmailAddress = Validator.isValidEmailAddress
const startDateMustBeAfterPreviousAction = Validator.startDateMustBeAfterPreviousAction
const endDateMustBeBeforeNextAction = Validator.endDateMustBeBeforeNextAction
const validateStartDateIsBeforeEndDate = Validator.validateStartDateIsBeforeEndDate
const canNotIntersectWithExistingInterval = Validator.canNotIntersectWithExistingInterval
const canNotStartAnActionAfterAnActiveAction = Validator.canNotStartAnActionAfterAnActiveAction
const validateMountingTimeRange = Validator.validateMountingTimeRange
const validateMountingDates = Validator.validateMountingDates
const validateInputForLocationType = Validator.validateInputForLocationType
const validateVisibility = Validator.validateVisibility
const endDateMustBeBeforeEndOfMountAction = Validator.endDateMustBeBeforeEndOfMountAction
const startDateMustBeAfterStartOfMountAction = Validator.startDateMustBeAfterStartOfMountAction
const endDateMustBeBeforeEndDateOfRelatedDevice = Validator.endDateMustBeBeforeEndDateOfRelatedDevice
const dateMustBeInRangeOfConfigurationDates = Validator.dateMustBeInRangeOfConfigurationDates

describe('#isValidEmailAddress()', () => {
  it('should return true with an valid email address', () => {
    const email = 'john.doe@gfz-potsdam.de'
    // Do not test with .toBeTruthy, as it passes when we get a non empty string back.
    // Those non empty strings represent error messages, so we don't want to see them
    // as passing.
    // So we better make a test with equality check here.
    // Note: This also effects most of the validation tests here.
    expect(isValidEmailAddress(email)).toEqual(true)
  })
  it('should return true with some more interesting email addresses', () => {
    // bob@⚔️.gg
    const email1 = 'xn--bob@-y13b.gg'
    expect(isValidEmailAddress(email1)).toEqual(true)

    // max@müller.de
    const email2 = 'xn--max@mller-u9a.de'
    expect(isValidEmailAddress(email2)).toEqual(true)
  })
  it('should return true with an valid email address with subdomains', () => {
    const email = 'john.doe@mail.gfz-potsdam.de'
    expect(isValidEmailAddress(email)).toEqual(true)
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
    expect(startDateMustBeAfterPreviousAction(checkDate, endDate, locationTimepoints)).toEqual(true)
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
    expect(startDateMustBeAfterPreviousAction(checkDate, endDate, locationTimepoints)).toEqual(true)
    // And it should also work if we have the reversed order.
    locationTimepoints.reverse()
    expect(startDateMustBeAfterPreviousAction(checkDate, endDate, locationTimepoints)).toEqual(true)
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
    expect(startDateMustBeAfterPreviousAction(checkDate, endDate, locationTimepoints)).toEqual(true)
    // And, again, also in reversed order
    locationTimepoints.reverse()
    expect(startDateMustBeAfterPreviousAction(checkDate, endDate, locationTimepoints)).toEqual(true)
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
    // And same if reversed order.
    locationTimepoints.reverse()
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
    expect(endDateMustBeBeforeNextAction(checkDate, endDate, locationTimepoints)).toEqual(true)
    locationTimepoints.reverse()
    expect(endDateMustBeBeforeNextAction(checkDate, endDate, locationTimepoints)).toEqual(true)
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
    expect(endDateMustBeBeforeNextAction(checkDate, endDate, locationTimepoints)).toEqual(true)
    locationTimepoints.reverse()
    expect(endDateMustBeBeforeNextAction(checkDate, endDate, locationTimepoints)).toEqual(true)
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
    locationTimepoints.reverse()
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

    expect(canNotIntersectWithExistingInterval(startDate, locationTimepoints)).toEqual(true)
  })
  it('should return true if no locations exists', () => {
    const startDate = DateTime.fromISO('1990-09-19', { zone: 'UTC' })
    const locationTimepoints: ILocationTimepoint[] = []

    expect(canNotIntersectWithExistingInterval(startDate, locationTimepoints)).toEqual(true)
  })
  it('should return true if the start date is after the last end date', () => {
    const startDate = DateTime.utc(2023, 4, 19, 9, 0, 0)
    const locationTimepoints = [
      {
        type: LocationTypes.staticStart,
        timepoint: DateTime.utc(2023, 4, 19, 7, 0, 0),
        id: '1',
        text: 'The location start'
      },
      {
        type: LocationTypes.staticEnd,
        timepoint: DateTime.utc(2023, 4, 19, 8, 0, 0),
        id: '1',
        text: 'The location end'
      }
    ]
    expect(canNotIntersectWithExistingInterval(startDate, locationTimepoints)).toEqual(true)
    locationTimepoints.reverse()
    expect(canNotIntersectWithExistingInterval(startDate, locationTimepoints)).toEqual(true)
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

    const expectedValidationMessage = 'Must be before ' + date1.setZone('UTC').toFormat('yyyy-MM-dd HH:mm') + ' or after ' + date2.setZone('UTC').toFormat('yyyy-MM-dd HH:mm') + ' (of existing location action)'
    expect(canNotIntersectWithExistingInterval(startDate, locationTimepoints)).toBe(expectedValidationMessage)
    locationTimepoints.reverse()
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
    locationTimepoints.reverse()
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
    expect(canNotStartAnActionAfterAnActiveAction(dateToCheck, locationTimepoints)).toEqual(true)
  })

  it('should return true if no location actions exist', () => {
    const dateToCheck = DateTime.fromISO('1990-09-21', { zone: 'UTC' })
    const locationTimepoints: ILocationTimepoint[] = []
    expect(canNotStartAnActionAfterAnActiveAction(dateToCheck, locationTimepoints)).toEqual(true)
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
    expect(canNotStartAnActionAfterAnActiveAction(dateToCheck, locationTimepoints)).toEqual(true)
    locationTimepoints.reverse()
    expect(canNotStartAnActionAfterAnActiveAction(dateToCheck, locationTimepoints)).toEqual(true)
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

describe('#validateInputForStartDate', () => {
  it('should return true if value is empty string \'\'', () => {
    const configuration = new Configuration()
    const validateInputForStartDate = Validator.validateInputForStartDate(configuration)

    const value = ''

    expect(validateInputForStartDate(value)).toEqual(true)
  })
  it('should return true if start date of configuration is null', () => {
    const configuration = new Configuration()
    const validateInputForStartDate = Validator.validateInputForStartDate(configuration)

    configuration.startDate = null
    const value = 'something'

    expect(validateInputForStartDate(value)).toEqual(true)
  })
  it('should return true if end date of configuration is not set', () => {
    const configuration = new Configuration()
    const validateInputForStartDate = Validator.validateInputForStartDate(configuration)

    configuration.startDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    configuration.endDate = null
    const value = 'something'

    expect(validateInputForStartDate(value)).toEqual(true)
  })
  it('should return true if start date of configuration is before end date of configuration', () => {
    const configuration = new Configuration()
    const validateInputForStartDate = Validator.validateInputForStartDate(configuration)

    configuration.startDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    configuration.endDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const value = 'something'

    expect(validateInputForStartDate(value)).toEqual(true)
  })
  it('should return true if start date of configuration is same as end date of configuration', () => {
    const configuration = new Configuration()
    const validateInputForStartDate = Validator.validateInputForEndDate(configuration)

    configuration.startDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    configuration.endDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    const value = 'something'

    expect(validateInputForStartDate(value)).toEqual(true)
  })
  it('should return message if start date of configuration is after end date of configuration', () => {
    const configuration = new Configuration()
    const validateInputForStartDate = Validator.validateInputForStartDate(configuration)

    configuration.startDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    configuration.endDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    const value = 'something'

    expect(validateInputForStartDate(value)).toEqual('Start date must not be after end date')
  })
})

describe('#validateInputForEndDate', () => {
  it('should return true if value is empty string \'\'', () => {
    const configuration = new Configuration()
    const validateInputForStartDate = Validator.validateInputForEndDate(configuration)

    const value = ''

    expect(validateInputForStartDate(value)).toEqual(true)
  })
  it('should return true if end date of configuration is null', () => {
    const configuration = new Configuration()
    const validateInputForStartDate = Validator.validateInputForEndDate(configuration)

    configuration.endDate = null
    const value = 'something'

    expect(validateInputForStartDate(value)).toEqual(true)
  })
  it('should return true if start date of configuration is not set', () => {
    const configuration = new Configuration()
    const validateInputForStartDate = Validator.validateInputForEndDate(configuration)

    configuration.startDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    configuration.endDate = null
    const value = 'something'

    expect(validateInputForStartDate(value)).toEqual(true)
  })
  it('should return true if end date of configuration is after start date of configuration', () => {
    const configuration = new Configuration()
    const validateInputForStartDate = Validator.validateInputForEndDate(configuration)

    configuration.startDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    configuration.endDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const value = 'something'

    expect(validateInputForStartDate(value)).toEqual(true)
  })
  it('should return true if start date of configuration is same as end date of configuration', () => {
    const configuration = new Configuration()
    const validateInputForStartDate = Validator.validateInputForEndDate(configuration)

    configuration.startDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    configuration.endDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    const value = 'something'

    expect(validateInputForStartDate(value)).toEqual(true)
  })
  it('should return message if start date of configuration is after end date of configuration', () => {
    const configuration = new Configuration()
    const validateInputForStartDate = Validator.validateInputForEndDate(configuration)

    configuration.startDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    configuration.endDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    const value = 'something'

    expect(validateInputForStartDate(value)).toEqual('End date must not be before start date')
  })
})

describe('#validateMountingTimeRange', () => {
  it('should return message if startDate is null', () => {
    const startDate = null
    const endDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const parentStartDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    const parentEndDate = DateTime.fromISO('2023-06-03', { zone: 'UTC' })

    const actual = validateMountingTimeRange(startDate, endDate, parentStartDate, parentEndDate)
    expect(actual).toEqual('Start date is required')
  })
  it('should return message if startDate is before parentStartDate', () => {
    const startDate = DateTime.fromISO('2023-05-01', { zone: 'UTC' })
    const endDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const parentStartDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    const parentEndDate = DateTime.fromISO('2023-06-03', { zone: 'UTC' })

    const actual = validateMountingTimeRange(startDate, endDate, parentStartDate, parentEndDate)
    expect(actual).toEqual(`Start date must not be before start date of the parent platform (${dateToString(parentStartDate)})`)
  })
  it('should return message if startDate is after parentEndDate', () => {
    const startDate = DateTime.fromISO('2023-06-04', { zone: 'UTC' })
    const endDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const parentStartDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    const parentEndDate = DateTime.fromISO('2023-06-03', { zone: 'UTC' })

    const actual = validateMountingTimeRange(startDate, endDate, parentStartDate, parentEndDate)
    expect(actual).toEqual(`Start date must be before end date of the parent platform (${dateToString(parentEndDate)})`)
  })
  it('should return message if endDate is before parentStartDate', () => {
    const startDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const endDate = DateTime.fromISO('2023-05-02', { zone: 'UTC' })
    const parentStartDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    const parentEndDate = DateTime.fromISO('2023-06-03', { zone: 'UTC' })

    const actual = validateMountingTimeRange(startDate, endDate, parentStartDate, parentEndDate)
    expect(actual).toEqual(`End date must be after start date of the parent platform (${dateToString(parentStartDate)})`)
  })
  it('should return message if parentEndDate is set but endDate is not set', () => {
    const startDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const endDate = null
    const parentStartDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    const parentEndDate = DateTime.fromISO('2023-06-03', { zone: 'UTC' })

    const actual = validateMountingTimeRange(startDate, endDate, parentStartDate, parentEndDate)
    expect(actual).toEqual(`End date must be before end date of the parent platform (${dateToString(parentEndDate)})`)
  })
  it('should return message if endDate is after parentEndDate', () => {
    const startDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const endDate = DateTime.fromISO('2023-06-04', { zone: 'UTC' })
    const parentStartDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    const parentEndDate = DateTime.fromISO('2023-06-03', { zone: 'UTC' })

    const actual = validateMountingTimeRange(startDate, endDate, parentStartDate, parentEndDate)
    expect(actual).toEqual(`End date must be before end date of the parent platform (${dateToString(parentEndDate)})`)
  })
  it('should return true if startDate is after parentStartDate', () => {
    const startDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const endDate = null
    const parentStartDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    const parentEndDate = null

    const actual = validateMountingTimeRange(startDate, endDate, parentStartDate, parentEndDate)
    expect(actual).toEqual(true)
  })
  it('should return true if endDate is after parentStartDate and endDate is after parentStartDate', () => {
    const startDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const endDate = DateTime.fromISO('2023-06-03', { zone: 'UTC' })
    const parentStartDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    const parentEndDate = null

    const actual = validateMountingTimeRange(startDate, endDate, parentStartDate, parentEndDate)
    expect(actual).toEqual(true)
  })
})

describe('#validateMountingDates', () => {
  it('should return message if startDate is null', () => {
    const startDate = null
    const endDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const actual = validateMountingDates(startDate, endDate)
    expect(actual).toEqual('Start date is required')
  })
  it('should return true if startDate is set and endDate is null', () => {
    const startDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const endDate = null
    const actual = validateMountingDates(startDate, endDate)
    expect(actual).toEqual(true)
  })
  it('should return true if startDate is before endDate', () => {
    const startDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const endDate = DateTime.fromISO('2023-06-03', { zone: 'UTC' })
    const actual = validateMountingDates(startDate, endDate)
    expect(actual).toEqual(true)
  })
  it('should return message if startDate is after endDate', () => {
    const startDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const endDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    const actual = validateMountingDates(startDate, endDate)
    expect(actual).toEqual('End date must be after start date')
  })
})

describe('#validateInputForLocationType', () => {
  it('should return true if value is LocationType.Stationary (=Stationary)', () => {
    const value = LocationType.Stationary
    const actual = validateInputForLocationType(value)
    expect(actual).toEqual(true)
  })
  it('should return true if value is LocationType.Dynamic (=Dynamic)', () => {
    const value = LocationType.Dynamic
    const actual = validateInputForLocationType(value)
    expect(actual).toEqual(true)
  })
  it('should return message if value is not of LocationType.Stationary or LocationType.Dynamic', () => {
    const value = ''
    const actual = validateInputForLocationType(value)
    expect(actual).toEqual('Location type must be set')
  })
})

describe('#mustBeProvided', () => {
  it('should return message if value is null', () => {
    const fieldName = 'fieldName'
    const mustBeProvided = Validator.mustBeProvided(fieldName)
    const value = null

    const actual = mustBeProvided(value)
    expect(actual).toEqual(fieldName + ' must be provided')
  })
  it('should return message if value is empty string', () => {
    const fieldName = 'fieldName'
    const mustBeProvided = Validator.mustBeProvided(fieldName)
    const value = ''

    const actual = mustBeProvided(value)
    expect(actual).toEqual(fieldName + ' must be provided')
  })
  it('should return true if value is provided', () => {
    const fieldName = 'fieldName'
    const mustBeProvided = Validator.mustBeProvided(fieldName)
    const value = 'a value'

    const actual = mustBeProvided(value)
    expect(actual).toEqual(true)
  })
})

describe('validatePermissionGroup', () => {
  it('should eturn message if isPrivate is true and a group is provided', () => {
    const isPrivate = true
    const validatePermissionGroup = Validator.validatePermissionGroup(isPrivate)
    const group = new PermissionGroup()

    const actual = validatePermissionGroup(group)
    expect(actual).toEqual('You are not allowed to add a group.')
  })
  it('should return message if isPrivate is false and group is null', () => {
    const isPrivate = false
    const validatePermissionGroup = Validator.validatePermissionGroup(isPrivate)
    const group = null

    const actual = validatePermissionGroup(group)
    expect(actual).toEqual('You must add a group.')
  })
  it('should return true if isPrivate is true and group is null', () => {
    const isPrivate = true
    const validatePermissionGroup = Validator.validatePermissionGroup(isPrivate)
    const group = null

    const actual = validatePermissionGroup(group)
    expect(actual).toEqual(true)
  })
  it('should return true if isPrivate is false and group is provided', () => {
    const isPrivate = false
    const validatePermissionGroup = Validator.validatePermissionGroup(isPrivate)
    const group = new PermissionGroup()

    const actual = validatePermissionGroup(group)
    expect(actual).toEqual(true)
  })
})

describe('#validateVisibility', () => {
  it('should return message if visibility is private and groups are provided ', () => {
    const visibility = Visibility.Private
    const groups: IPermissionGroup[] = [new PermissionGroup()]
    const entityName = 'entityName'

    const actual = validateVisibility(visibility, groups, entityName)
    expect(actual).toEqual(`You are not allowed to set the visibility to private as long as the ${entityName} has permission groups.`)
  })
  it('should return true if visibility is internal and groups are provided ', () => {
    const visibility = Visibility.Internal
    const groups: IPermissionGroup[] = [new PermissionGroup()]
    const entityName = 'entityName'

    const actual = validateVisibility(visibility, groups, entityName)
    expect(actual).toEqual(true)
  })
  it('should return true if visibility is public and groups are provided ', () => {
    const visibility = Visibility.Internal
    const groups: IPermissionGroup[] = [new PermissionGroup()]
    const entityName = 'entityName'

    const actual = validateVisibility(visibility, groups, entityName)
    expect(actual).toEqual(true)
  })
  it('should return true if visibility is private and no groups are provided ', () => {
    const visibility = Visibility.Private
    const groups: IPermissionGroup[] = []
    const entityName = 'entityName'

    const actual = validateVisibility(visibility, groups, entityName)
    expect(actual).toEqual(true)
  })
})

describe('#endDateMustBeBeforeEndOfMountAction', () => {
  it('should return true if action has no endDate', () => {
    const endDate = null

    const action = new DeviceMountAction(
      '1',
      new Device(),
      null,
      null,
      DateTime.fromISO('2023-06-02', { zone: 'UTC' }),
      null,
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
      null,
      '',
      '',
      ''
    )

    const actual = endDateMustBeBeforeEndOfMountAction(endDate, action)
    expect(actual).toEqual(true)
  })
  it('should return true if action is undefined', () => {
    const endDate = null
    const action = undefined

    const actual = endDateMustBeBeforeEndOfMountAction(endDate, action)
    expect(actual).toEqual(true)
  })
  it('should return message if no endDate is provided (of falsely type)', () => {
    const endDate = null
    const action = new DeviceMountAction(
      '1',
      new Device(),
      null,
      null,
      DateTime.fromISO('2023-06-02', { zone: 'UTC' }),
      null,
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
      null,
      '',
      '',
      ''
    )
    action.endDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })

    const actual = endDateMustBeBeforeEndOfMountAction(endDate, action)
    expect(actual).toEqual('End date must be before ' + dateToDateTimeStringHHMM(action.endDate) + ' (end of mount)')
  })
  it('should return message endDate is after endDate of action', () => {
    const endDate = DateTime.fromISO('2023-06-03', { zone: 'UTC' })
    const action = new DeviceMountAction(
      '1',
      new Device(),
      null,
      null,
      DateTime.fromISO('2023-06-02', { zone: 'UTC' }),
      null,
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
      null,
      '',
      '',
      ''
    )
    action.endDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })

    const actual = endDateMustBeBeforeEndOfMountAction(endDate, action)
    expect(actual).toEqual('End date must be before ' + dateToDateTimeStringHHMM(action.endDate) + ' (end of mount)')
  })
  it('should return true if endDate is before endDate of action', () => {
    const endDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    const action = new DeviceMountAction(
      '1',
      new Device(),
      null,
      null,
      DateTime.fromISO('2023-06-02', { zone: 'UTC' }),
      null,
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
      null,
      '',
      '',
      ''
    )
    action.endDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })

    const actual = endDateMustBeBeforeEndOfMountAction(endDate, action)
    expect(actual).toEqual(true)
  })
})

describe('#startDateMustBeAfterStartOfMountAction', () => {
  it('should return true if no action is provided (of falsely type) ', () => {
    const startDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    const action = undefined

    const actual = startDateMustBeAfterStartOfMountAction(startDate, action)
    expect(actual).toEqual(true)
  })
  it('should return true if no action is provided (of falsely type)', () => {
    const startDate = null
    const action = new DeviceMountAction(
      '1',
      new Device(),
      null,
      null,
      DateTime.fromISO('2023-06-02', { zone: 'UTC' }),
      null,
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
      null,
      '',
      '',
      ''
    )

    const actual = startDateMustBeAfterStartOfMountAction(startDate, action)
    expect(actual).toEqual('Start date must be after ' + dateToDateTimeStringHHMM(action.beginDate) + ' (begin of mount)')
  })
  it('should return message if startDate is before startDate of action', () => {
    const startDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    const action = new DeviceMountAction(
      '1',
      new Device(),
      null,
      null,
      DateTime.fromISO('2023-06-02', { zone: 'UTC' }),
      null,
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
      null,
      '',
      '',
      ''
    )

    const actual = startDateMustBeAfterStartOfMountAction(startDate, action)
    expect(actual).toEqual('Start date must be after ' + dateToDateTimeStringHHMM(action.beginDate) + ' (begin of mount)')
  })
  it('should return message if startDate is before startDate of action', () => {
    const startDate = DateTime.fromISO('2023-06-03', { zone: 'UTC' })
    const action = new DeviceMountAction(
      '1',
      new Device(),
      null,
      null,
      DateTime.fromISO('2023-06-02', { zone: 'UTC' }),
      null,
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
      null,
      '',
      '',
      ''
    )

    const actual = startDateMustBeAfterStartOfMountAction(startDate, action)
    expect(actual).toEqual(true)
  })
})

describe('#endDateMustBeBeforeEndDateOfRelatedDevice', () => {
  it('should return true if endDateOfDynamicAction is null and earliestEndDateOfRelatedDevice is null', () => {
    const endDateOfDynamicAction = null
    const earliestEndDateOfRelatedDevice = null
    const actual = endDateMustBeBeforeEndDateOfRelatedDevice(endDateOfDynamicAction, earliestEndDateOfRelatedDevice)

    expect(actual).toEqual(true)
  })
  it('should return message if endDateOfDynamicAction is null and earliestEndDateOfRelatedDevice is Date', () => {
    const endDateOfDynamicAction = null
    const earliestEndDateOfRelatedDevice = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const actual = endDateMustBeBeforeEndDateOfRelatedDevice(endDateOfDynamicAction, earliestEndDateOfRelatedDevice)

    expect(actual).toEqual('End date must be before ' + dateToDateTimeStringHHMM(earliestEndDateOfRelatedDevice) + ' (planned unmount).')
  })
  it('should return message if endDateOfDynamicAction is after earliestEndDateOfRelatedDevice', () => {
    const endDateOfDynamicAction = DateTime.fromISO('2023-06-03', { zone: 'UTC' })
    const earliestEndDateOfRelatedDevice = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const actual = endDateMustBeBeforeEndDateOfRelatedDevice(endDateOfDynamicAction, earliestEndDateOfRelatedDevice)

    expect(actual).toEqual('End date must be before ' + dateToDateTimeStringHHMM(earliestEndDateOfRelatedDevice) + ' (planned unmount).')
  })
  it('should return true if earliestEndDateOfRelatedDevice is before earliestEndDateOfRelatedDevice', () => {
    const endDateOfDynamicAction = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    const earliestEndDateOfRelatedDevice = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const actual = endDateMustBeBeforeEndDateOfRelatedDevice(endDateOfDynamicAction, earliestEndDateOfRelatedDevice)

    expect(actual).toEqual(true)
  })
})

describe('#dateMustBeInRangeOfConfigurationDates', () => {
  it('should return true if configuration is null', () => {
    const configuration = null
    const dateToValidate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })

    const actual = dateMustBeInRangeOfConfigurationDates(configuration, dateToValidate)
    expect(actual).toEqual(true)
  })
  it('should return true if dateToValidate is null', () => {
    const configuration = new Configuration()
    const dateToValidate = null

    const actual = dateMustBeInRangeOfConfigurationDates(configuration, dateToValidate)
    expect(actual).toEqual(true)
  })
  it('should return message if configuration has a start date but no end date and dateToValidate is before start date of configuration', () => {
    const configuration = new Configuration()
    configuration.startDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const dateToValidate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })

    const actual = dateMustBeInRangeOfConfigurationDates(configuration, dateToValidate)
    expect(actual).toEqual('Date must be after ' + dateToDateTimeStringHHMM(configuration.startDate) + ' ( start date of configuration)')
  })
  it('should return message if configuration has a end date but no start date and dateToValidate is after end date of configuration', () => {
    const configuration = new Configuration()
    configuration.endDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const dateToValidate = DateTime.fromISO('2023-06-03', { zone: 'UTC' })

    const actual = dateMustBeInRangeOfConfigurationDates(configuration, dateToValidate)
    expect(actual).toEqual('Date must be before ' + dateToDateTimeStringHHMM(configuration.endDate) + ' ( end date of configuration)')
  })
  it('should return message if dateToValidate is before start date of configuration', () => {
    const configuration = new Configuration()
    configuration.startDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    configuration.endDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const dateToValidate = DateTime.fromISO('2023-05-03', { zone: 'UTC' })

    const actual = dateMustBeInRangeOfConfigurationDates(configuration, dateToValidate)
    expect(actual).toEqual('Date must be in the range of ' + dateToDateTimeStringHHMM(configuration.startDate) + ' -- ' + dateToDateTimeStringHHMM(configuration.endDate) + ' (dates of configuration)')
  })
  it('should return message if dateToValidate is after end date of configuration', () => {
    const configuration = new Configuration()
    configuration.startDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    configuration.endDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const dateToValidate = DateTime.fromISO('2023-07-03', { zone: 'UTC' })

    const actual = dateMustBeInRangeOfConfigurationDates(configuration, dateToValidate)
    expect(actual).toEqual('Date must be in the range of ' + dateToDateTimeStringHHMM(configuration.startDate) + ' -- ' + dateToDateTimeStringHHMM(configuration.endDate) + ' (dates of configuration)')
  })
  it('should return message if dateToValidate is after end date of configuration', () => {
    const configuration = new Configuration()
    configuration.startDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    configuration.endDate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })
    const dateToValidate = DateTime.fromISO('2023-07-03', { zone: 'UTC' })

    const actual = dateMustBeInRangeOfConfigurationDates(configuration, dateToValidate)
    expect(actual).toEqual('Date must be in the range of ' + dateToDateTimeStringHHMM(configuration.startDate) + ' -- ' + dateToDateTimeStringHHMM(configuration.endDate) + ' (dates of configuration)')
  })
  it('should return true if dateToValidate is between after end date of configuration', () => {
    const configuration = new Configuration()
    configuration.startDate = DateTime.fromISO('2023-06-01', { zone: 'UTC' })
    configuration.endDate = DateTime.fromISO('2023-06-03', { zone: 'UTC' })
    const dateToValidate = DateTime.fromISO('2023-06-02', { zone: 'UTC' })

    const actual = dateMustBeInRangeOfConfigurationDates(configuration, dateToValidate)
    expect(actual).toEqual(true)
  })
})
