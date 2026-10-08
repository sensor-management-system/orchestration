/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * SPDX-License-Identifier: EUPL-1.2
 */
export const URL_IMAGE_ERROR = 'This image could not be loaded from its URL. Please add it as a file upload instead.'

/** Fetch and decode external images only in the browser, never via the backend. */
export async function fetchAttachmentImage (url: string): Promise<string> {
  if (typeof window === 'undefined') {
    throw new TypeError('Image previews require a browser')
  }
  const parsed = new URL(url)
  if (!['http:', 'https:'].includes(parsed.protocol) || parsed.username || parsed.password) {
    throw new Error('Unsupported image URL')
  }
  const controller = new AbortController()
  const timeout = window.setTimeout(() => controller.abort(), 15000)
  let objectUrl: string | null = null
  try {
    const response = await fetch(url, {
      mode: 'cors',
      credentials: 'omit',
      referrerPolicy: 'no-referrer',
      signal: controller.signal
    })
    if (!response.ok) {
      throw new Error('Image request failed')
    }
    objectUrl = window.URL.createObjectURL(await response.blob())
    const previewUrl = objectUrl
    await new Promise<void>((resolve, reject) => {
      const image = new window.Image()
      const decodeTimeout = window.setTimeout(() => {
        image.onload = null
        image.onerror = null
        image.src = ''
        reject(new Error('Image decoding timed out'))
      }, 15000)
      image.onload = () => {
        window.clearTimeout(decodeTimeout)
        resolve()
      }
      image.onerror = () => {
        window.clearTimeout(decodeTimeout)
        reject(new Error('Invalid image'))
      }
      image.src = previewUrl
    })
    return objectUrl
  } catch (error) {
    if (objectUrl) {
      window.URL.revokeObjectURL(objectUrl)
    }
    throw error
  } finally {
    window.clearTimeout(timeout)
  }
}
