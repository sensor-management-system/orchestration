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
export const dateToString = (aDate: Date | null): string => {
  if (!aDate) {
    return ''
  }
  const year = aDate.getFullYear()
  const month = aDate.getMonth() + 1
  const day = aDate.getDate()

  return year + '-' + month.toString().padStart(2, '0') + '-' + day.toString().padStart(2, '0')
}

export const stringToDate = (aDate: string): Date => {
  const newDate: Date = new Date(aDate)
  newDate.setHours(0, 0, 0)
  return newDate
}

export const timeStampToUTCDateTime = (value: number) : string => {
  if (!value) {
    return ''
  }
  const date = new Date(value * 1000)
  const day = '0' + date.getUTCDate()
  const month = '0' + (date.getUTCMonth() + 1)
  const year = date.getUTCFullYear()
  const hours = '0' + date.getUTCHours()
  const minutes = '0' + date.getUTCMinutes()
  const seconds = '0' + date.getUTCSeconds()

  return year +
    '-' +
    month.substr(-2) +
    '-' +
    day.substr(-2) +
    ' ' +
    hours.substr(-2) +
    ':' +
    minutes.substr(-2) +
    ':' +
    seconds.substr(-2) +
    ' UTC'
}
