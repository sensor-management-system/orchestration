/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2024
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
import Vue from 'vue'

import { DateTime } from 'luxon'

import { dateToDateTimeString, dateToDateTimeStringHHMM } from '@/utils/dateHelper'
import { round } from '@/utils/numericsHelper'
import { shortenRight, shortenLeft, shortenMiddle } from '@/utils/stringHelpers'

/**
 * returns a default string when value is empty
 *
 * @param {any} value - a value
 * @param {string} [defaultValue] - a default string, defaults to '-'
 * @returns {string} the string or the default, if the string is empty
 */
Vue.filter('orDefault', (value: string | number | null | undefined, defaultValue: string = '—'): string => {
  if (typeof value === 'string') {
    return value || defaultValue
  }
  if (typeof value === 'number') {
    return !isNaN(value) ? String(value) : defaultValue
  }
  return defaultValue
})

Vue.filter('toUtcDateTimeString', (value: DateTime, defaultValue: string = ''): string => {
  return dateToDateTimeString(value) || defaultValue
})
Vue.filter('toUtcDateTimeStringHHMM', (value: DateTime, defaultValue: string = ''): string => {
  return dateToDateTimeStringHHMM(value) || defaultValue
})

/**
 * shortens a string to length characters to the right, adds a replacement character
 *
 * @param {string} text - the text to shorten
 * @param {number} [length] - the length of the shortened text, defaults to stringHelpers.DEFAULT_SHORTEN_LENGTH
 * @param {string} [DEFAULT_REPLACEMENT] - a replacement string which is inserted to the right, defaults to stringHelpers.DEFAULT_REPLACEMENT
 * @returns {string} the shortened string
 */
Vue.filter('shortenRight', (text: string, length?: number, replacement?: string): string => {
  return shortenRight(text, length, replacement)
})

/**
 * shortens a string to length characters to the legt, adds a replacement character
 *
 * @param {string} text - the text to shorten
 * @param {number} [length] - the length of the shortened text, defaults to stringHelpers.DEFAULT_SHORTEN_LENGTH
 * @param {string} [DEFAULT_REPLACEMENT] - a replacement string which is inserted to the left, defaults to stringHelpers.DEFAULT_REPLACEMENT
 * @returns {string} the shortened string
 */
Vue.filter('shortenLeft', (text: string, length?: number, replacement?: string): string => {
  return shortenLeft(text, length, replacement)
})

/**
 * shortens a string to length characters, adds a replacement character in the middle
 *
 * @param {string} text - the text to shorten
 * @param {number} [length] - the length of the shortened text, defaults to stringHelpers.DEFAULT_SHORTEN_LENGTH
 * @param {string} [DEFAULT_REPLACEMENT] - a replacement string which is inserted in the middle, defaults to stringHelpers.DEFAULT_REPLACEMENT
 * @returns {string} the shortened string
 */
Vue.filter('shortenMiddle', (text: string, length?: number, replacement?: string): string => {
  return shortenMiddle(text, length, replacement)
})

/**
 * joins a list to a single string, but only uses those entries that have content
 *
 * @param {string[]} parts - the texts to concat
 * @param {string} [joinChar] - the text to join the parts together - defaults to ', ' for comma seperated lists
 * @returns {string} the joined string
 */
Vue.filter('sparseJoin', (parts: string[], joinChar: string = ', '): string => {
  return parts.filter(x => !!x).join(joinChar)
})

Vue.filter('round', (value: number, ndigits: number = 0): number => {
  return round(value, ndigits)
})
