/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'
import { MaintenanceMessageApi } from '@/services/sms/MaintenanceMessageApi'

describe('MaintenanceMessageApi', () => {
  it('queries only the dedicated backend route', async () => {
    const get = jest.fn().mockResolvedValue({ status: 200, data: '# Maintenance' })
    const api = new MaintenanceMessageApi({ get } as unknown as AxiosInstance)
    expect(await api.getMessage()).toBe('# Maintenance')
    expect(get).toHaveBeenCalledWith('/maintenance-message', {
      headers: { Accept: 'text/plain' }, responseType: 'text'
    })
  })

  it('returns no message when disabled', async () => {
    const get = jest.fn().mockResolvedValue({ status: 204, data: '' })
    const api = new MaintenanceMessageApi({ get } as unknown as AxiosInstance)
    expect(await api.getMessage()).toBeNull()
  })
})
