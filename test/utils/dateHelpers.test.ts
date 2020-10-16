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
import { dateToString, stringToDate } from '@/utils/dateHelper'

describe('dateToString', () => {
  it('should work with by birthday', () => {
    const date = new Date('1990-09-18')
    const result = dateToString(date)

    expect(result).toBe('1990-09-18')
  })
  it('should also work with the date on that I write the tests', () => {
    const date = new Date('2020-09-25')
    const result = dateToString(date)

    expect(result).toBe('2020-09-25')
  })
})

describe('stringToDate', () => {
  it('should work with by birthday', () => {
    const day = '1990-09-18'
    const result = stringToDate(day)

    expect(result.getFullYear()).toBe(1990)
    expect(result.getMonth()).toBe(8) // it has a zero based count for months
    expect(result.getDate()).toBe(18)
  })
  it('should also work with the date on that I write the tests', () => {
    const day = '2020-09-25'
    const result = stringToDate(day)

    expect(result.getFullYear()).toBe(2020)
    expect(result.getMonth()).toBe(8) // it has a zero based count for months
    expect(result.getDate()).toBe(25)
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
