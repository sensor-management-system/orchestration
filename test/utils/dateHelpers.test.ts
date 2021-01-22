/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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
import { dateToString, stringToDate, timeStampToUTCDateTime } from '@/utils/dateHelper'

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
    expect(formatted).toEqual('2020-10-21 13:12:25 UTC')
  })
})
