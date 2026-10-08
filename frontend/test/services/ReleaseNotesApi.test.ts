/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'
import { ReleaseNotesApi } from '@/services/sms/ReleaseNotesApi'

describe('ReleaseNotesApi', () => {
  it('requests the changelog directly without a backend proxy', async () => {
    const url = 'https://example.org/CHANGELOG.md'
    const get = jest.fn().mockResolvedValue({ data: '' })
    const api = new ReleaseNotesApi({ get } as unknown as AxiosInstance, url)
    await api.findAllReleases()
    expect(get).toHaveBeenCalledWith(url)
  })

  it('propagates request failures without a proxy fallback', async () => {
    const get = jest.fn().mockRejectedValue(new Error('CORS'))
    const api = new ReleaseNotesApi({ get } as unknown as AxiosInstance, 'https://example.org/CHANGELOG.md')
    await expect(api.findAllReleases()).rejects.toThrow('CORS')
    expect(get).toHaveBeenCalledTimes(1)
  })
})
