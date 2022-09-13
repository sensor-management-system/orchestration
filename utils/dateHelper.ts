/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
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

export const dateToString = (aDate: DateTime | null): string => {
  if (!aDate) {
    return ''
  }
  return aDate.setZone('UTC').toFormat('yyyy-MM-dd')
}

export const dateToDateTimeStringHHMM = (aDate: DateTime | null): string => {
  if (!aDate) {
    return ''
  }
  return aDate.setZone('UTC').toFormat('yyyy-MM-dd HH:mm')
}

export const stringToDate = (aDate: string): DateTime => {
  return DateTime.fromISO(aDate, { zone: 'UTC' })
}

export const stringToDateTimeFormat = (aDate: string): DateTime => {
  return DateTime.fromFormat(aDate, 'yyyy-MM-dd HH:mm', { zone: 'UTC' })
}

export const timeStampToUTCDateTime = (value: number): string => {
  if (!value) {
    return ''
  }
  const date = DateTime.fromSeconds(value).setZone('UTC')
  return date.toFormat('yyyy-MM-dd HH:mm:ss') + ' UTC'
}

export const ISOToDateTimeString = (aDate: string | null): string => {
  if (!aDate) {
    return ''
  }
  const date = DateTime.fromISO(aDate, { zone: 'utc' })
  return dateToDateTimeStringHHMM(date)
}

export function dateTimesEqual (dateTime1: DateTime, dateTime2: DateTime): boolean {
  return dateTime1.toUTC().toISO() === dateTime2.toUTC().toISO()
}

export const dateToDateTimeString = (aDate: DateTime | null): string => {
  if (!aDate) {
    return ''
  }
  return aDate.setZone('UTC').toFormat('yyyy-MM-dd HH:mm:ss') + ' UTC'
}

export const currentAsUtcDateSecondsAsZeros = (): DateTime => {
  return DateTime.fromFormat(DateTime.now().toFormat('yyyy-MM-dd HH:mm'), 'yyyy-MM-dd HH:mm')
}

export const sortCriteriaAscending = (a: DateTime, b: DateTime) => {
  if (a < b) {
    return -1
  } else if (a > b) {
    return 1
  }
  return 0
}
