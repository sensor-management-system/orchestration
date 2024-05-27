/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DeviceProperty } from '@/models/DeviceProperty'

export class Pluralizer {
  private knownPluralForms: {[key: string]: string } = {}

  constructor (knownPluralForms: {[key: string]: string} = {}) {
    this.knownPluralForms = knownPluralForms
  }

  pluralize (count: number, singular: string, explictPlural: string | null = null) {
    if (count === 1) {
      return singular
    }
    if (explictPlural) {
      return explictPlural
    }
    if (this.knownPluralForms[singular]) {
      return this.knownPluralForms[singular]
    }
    return singular + 's'
  }
}

const defaultPluralizer = new Pluralizer()
export const pluralize = defaultPluralizer.pluralize.bind(defaultPluralizer)

export const DEFAULT_SHORTEN_LENGTH = 50
export const DEFAULT_SHORTEN_REPLACEMENT = '…'

/**
 * shortens a string to length characters to the right, adds a replacement character
 *
 * @param {string} text - the text to shorten
 * @param {number} [length] - the length of the shortened text, defaults to DEFAULT_SHORTEN_LENGTH
 * @param {string} [DEFAULT_SHORTEN_REPLACEMENT] - a replacement string which is inserted to the right, defaults to DEFAULT_SHORTEN_REPLACEMENT
 * @returns {string} the shortened string
 */
export function shortenRight (text: string, length: number = DEFAULT_SHORTEN_LENGTH, replacement: string = DEFAULT_SHORTEN_REPLACEMENT): string {
  if (text.length <= length) {
    return text
  }
  const targetLength = length - replacement.length
  return text.substring(0, targetLength) + replacement
}

/**
 * capitalizes the first character of a string
 *
 * @param {string} text - the text to capitalize
 * @returns {string} the capitalized string
 */
export function capitalize (text: string): string {
  return text.charAt(0).toUpperCase() + text.slice(1)
}

/**
 * shortens a string to length characters to the legt, adds a replacement character
 *
 * @param {string} text - the text to shorten
 * @param {number} [length] - the length of the shortened text, defaults to DEFAULT_SHORTEN_LENGTH
 * @param {string} [DEFAULT_SHORTEN_REPLACEMENT] - a replacement string which is inserted to the left, defaults to DEFAULT_SHORTEN_REPLACEMENT
 * @returns {string} the shortened string
 */
export function shortenLeft (text: string, length: number = DEFAULT_SHORTEN_LENGTH, replacement: string = DEFAULT_SHORTEN_REPLACEMENT): string {
  if (text.length <= length) {
    return text
  }
  const targetLength = length - replacement.length
  return replacement + text.substring(text.length - targetLength)
}

/**
 * shortens a string to length characters, adds a replacement character in the middle
 *
 * @param {string} text - the text to shorten
 * @param {number} [length] - the length of the shortened text, defaults to DEFAULT_SHORTEN_LENGTH
 * @param {string} [DEFAULT_SHORTEN_REPLACEMENT] - a replacement string which is inserted in the middle, defaults to DEFAULT_SHORTEN_REPLACEMENT
 * @returns {string} the shortened string
 */
export function shortenMiddle (text: string, length: number = DEFAULT_SHORTEN_LENGTH, replacement: string = DEFAULT_SHORTEN_REPLACEMENT): string {
  if (text.length <= length) {
    return text
  }
  const targetLength = length - replacement.length
  let a, b: number
  if (targetLength % 2 === 0) {
    a = b = targetLength / 2
  } else {
    a = Math.ceil(targetLength / 2)
    b = Math.floor(targetLength / 2)
  }
  return text.substring(0, a) + replacement + text.substring(text.length - b)
}

export function generatePropertyTitle (property: DeviceProperty) {
  if (property) {
    const propertyName = property.propertyName ?? ''
    const label = property.label ?? ''
    const unit = property.unitName ?? ''
    return `${propertyName} ${label ? `- ${label}` : ''} ${unit ? `(${unit})` : ''}`
  }
  return ''
}

export function coalesce (firstText: string | null | undefined, alternativeText: string): string {
  if (firstText) {
    return firstText
  }
  return alternativeText
}
