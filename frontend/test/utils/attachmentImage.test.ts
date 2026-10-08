/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * SPDX-License-Identifier: EUPL-1.2
 */
import { fetchAttachmentImage } from '@/utils/attachmentImage'

describe('direct browser URL image loading', () => {
  const originalFetch = global.fetch
  const originalImage = window.Image
  let fetchMock: jest.MockedFunction<typeof fetch>
  let decodeFails = false

  beforeEach(() => {
    decodeFails = false
    fetchMock = jest.fn<ReturnType<typeof fetch>, Parameters<typeof fetch>>()
    fetchMock.mockResolvedValue({ ok: true, blob: () => Promise.resolve(new Blob(['image'])) } as Response)
    global.fetch = fetchMock
    window.URL.createObjectURL = jest.fn().mockReturnValue('blob:external')
    window.URL.revokeObjectURL = jest.fn()
    window.Image = class {
      onload: (() => void) | null = null
      onerror: (() => void) | null = null
      get src (): string { return '' }
      set src (_value: string) {
        if (decodeFails) { this.onerror?.() } else { this.onload?.() }
      }
    } as unknown as typeof window.Image
  })

  afterEach(() => {
    global.fetch = originalFetch
    window.Image = originalImage
  })

  it('fetches without credentials and verifies image decoding', async () => {
    expect(await fetchAttachmentImage('https://example.org/image')).toBe('blob:external')
    expect(global.fetch).toHaveBeenCalledWith('https://example.org/image', expect.objectContaining({
      mode: 'cors', credentials: 'omit', referrerPolicy: 'no-referrer'
    }))
  })

  it('rejects CORS or network errors', async () => {
    fetchMock.mockRejectedValue(new Error('CORS'))
    await expect(fetchAttachmentImage('https://example.org/image')).rejects.toThrow('CORS')
  })

  it('rejects unsuccessful HTTP responses', async () => {
    fetchMock.mockResolvedValue({ ok: false } as Response)
    await expect(fetchAttachmentImage('https://example.org/image')).rejects.toThrow('Image request failed')
  })

  it('rejects non-image content and revokes its blob URL', async () => {
    decodeFails = true
    await expect(fetchAttachmentImage('https://example.org/image')).rejects.toThrow('Invalid image')
    expect(window.URL.revokeObjectURL).toHaveBeenCalledWith('blob:external')
  })

  it.each(['file:///image.png', 'javascript:alert(1)', 'https://user:secret@example.org/image'])('rejects unsupported URLs: %s', async (url) => {
    await expect(fetchAttachmentImage(url)).rejects.toThrow('Unsupported image URL')
    expect(global.fetch).not.toHaveBeenCalled()
  })
})
