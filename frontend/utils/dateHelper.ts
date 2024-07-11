/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
  return date.toFormat('yyyy-MM-dd HH:mm:ss')
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
  return aDate.setZone('UTC').toFormat('yyyy-MM-dd HH:mm:ss')
}

export const currentAsDateTimeObject = (): DateTime => {
  return DateTime.now().setZone('UTC')
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

export const sortCriteriaDescending = (a: DateTime, b: DateTime) => {
  // in JS: 0 * -1 = -0, so we return explicitly 0 in this case
  return sortCriteriaAscending(a, b) * -1 || 0
}
