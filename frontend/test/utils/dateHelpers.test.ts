/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2021
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'
import {
  dateTimesEqual,
  dateToString,
  stringToDate,
  timeStampToUTCDateTime,
  sortCriteriaAscending,
  sortCriteriaDescending
} from '@/utils/dateHelper'

describe('dateToString', () => {
  it('should work with by birthday', () => {
    const date = DateTime.fromISO('1990-09-18', { zone: 'UTC' })
    const result = dateToString(date)

    expect(result).toBe('1990-09-18')
  })
  it('should also work with the date on that I write the tests', () => {
    const date = DateTime.fromISO('2020-09-25', { zone: 'UTC' })
    const result = dateToString(date)

    expect(result).toBe('2020-09-25')
  })
})

describe('stringToDate', () => {
  it('should work with by birthday', () => {
    const day = '1990-09-18'
    const result = stringToDate(day)

    expect(result.year).toBe(1990)
    expect(result.month).toBe(9)
    expect(result.day).toBe(18)
  })
  it('should also work with the date on that I write the tests', () => {
    const day = '2020-09-25'
    const result = stringToDate(day)

    expect(result.year).toBe(2020)
    expect(result.month).toBe(9)
    expect(result.day).toBe(25)
  })
})

describe('stringToDate and dateToString', () => {
  const they = it
  they('should work together', () => {
    const inputValue = '2020-09-25'
    const asDate = stringToDate(inputValue)
    const asStr = dateToString(asDate)

    expect(asStr).toBe(inputValue)
  })
})

describe('timeStampToUTCDateTime', () => {
  it('should work with a current timestamp given by perl', () => {
    // by perl -e 'print time()'
    const timestamp = 1603285945
    const formatted = timeStampToUTCDateTime(timestamp)

    // in german summer time it is 15:12:25
    // in utc it is 13:12:25
    expect(formatted).toEqual('2020-10-21 13:12:25')
  })
})
describe('dateTimesEqual', () => {
  it('should return true for the very same objects', () => {
    const date = DateTime.utc(2020, 1, 1, 0, 0, 0, 0)
    expect(dateTimesEqual(date, date)).toBeTruthy()
  })
  it('should return true for eqivalent objects that are not equal themselves', () => {
    const date1 = DateTime.utc(2020, 1, 1, 0, 0, 0, 0)
    const date2 = DateTime.fromISO(date1.toISO()!)

    // they are not really equal
    // but they must be equivalent
    expect(date1).not.toEqual(date2)
    expect(dateTimesEqual(date1, date2)).toBeTruthy()
  })
  it('should return false for different objects', () => {
    const date1 = DateTime.utc(2020, 1, 1, 0, 0, 0, 0)
    const date2 = DateTime.utc(2020, 1, 2, 0, 0, 0, 0)
    expect(dateTimesEqual(date1, date2)).not.toBeTruthy()
  })
  it('should return true if they have different time zones but represent the same point it time', () => {
    const date1 = DateTime.local(2020, 1, 1, 0, 0, 0, 0)
    const date2 = date1.toUTC()
    expect(dateTimesEqual(date1, date2)).toBeTruthy()
  })
})
describe('sortCriteriaAscending', () => {
  it('should return 0 for same DateTimes', () => {
    const date1 = DateTime.utc(2023, 9, 8, 10, 0, 0, 0)
    const date2 = DateTime.utc(2023, 9, 8, 10, 0, 0, 0)
    const result = sortCriteriaAscending(date1, date2)
    expect(result).toEqual(0)
  })
  it('should return -1 if first DateTime is less than second DateTime', () => {
    const date1 = DateTime.utc(2023, 8, 11, 12, 0, 0, 0)
    const date2 = DateTime.utc(2023, 9, 8, 10, 0, 0, 0)
    const result = sortCriteriaAscending(date1, date2)
    expect(result).toEqual(-1)
  })
  it('should return 1 if first DateTime is greater than second DateTime', () => {
    const date1 = DateTime.utc(2023, 9, 8, 10, 0, 0, 0)
    const date2 = DateTime.utc(2023, 8, 11, 12, 0, 0, 0)
    const result = sortCriteriaAscending(date1, date2)
    expect(result).toEqual(1)
  })
})
describe('sortCriteriaDescending', () => {
  it('should return 0 for same DateTimes', () => {
    const date1 = DateTime.utc(2023, 9, 8, 10, 0, 0, 0)
    const date2 = DateTime.utc(2023, 9, 8, 10, 0, 0, 0)
    const result = sortCriteriaDescending(date1, date2)
    expect(result).toEqual(0)
  })
  it('should return -1 if first DateTime is greater than second DateTime', () => {
    const date1 = DateTime.utc(2023, 9, 8, 10, 0, 0, 0)
    const date2 = DateTime.utc(2023, 8, 11, 12, 0, 0, 0)
    const result = sortCriteriaDescending(date1, date2)
    expect(result).toEqual(-1)
  })
  it('should return 1 if first DateTime is less than second DateTime', () => {
    const date1 = DateTime.utc(2023, 8, 11, 12, 0, 0, 0)
    const date2 = DateTime.utc(2023, 9, 8, 10, 0, 0, 0)
    const result = sortCriteriaDescending(date1, date2)
    expect(result).toEqual(1)
  })
})
