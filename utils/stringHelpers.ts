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
