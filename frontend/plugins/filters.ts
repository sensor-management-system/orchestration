/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
