/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2022
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Tim Eder (UFZ, tim.eder@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
 *   (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *   (UFZ, https://www.ufz.de)
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
