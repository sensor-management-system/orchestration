/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'
import { Device } from '@/models/Device'

describe('Device', () => {
  describe('#createdAt', () => {
    it('should allow to set a datetime', () => {
      const device = new Device()
      expect(device.createdAt).toBeNull()
      device.createdAt = DateTime.utc(2021, 1, 22, 7, 32, 42)
      expect(device.createdAt.year).toEqual(2021)
      expect(device.createdAt.month).toEqual(1)
      expect(device.createdAt.day).toEqual(22)
      expect(device.createdAt.hour).toEqual(7)
      expect(device.createdAt.minute).toEqual(32)
      expect(device.createdAt.second).toEqual(42)
      expect(device.createdAt.zoneName).toEqual('UTC')
    })
  })
  describe('#updatedAt', () => {
    it('should allow to set a datetime', () => {
      const device = new Device()
      expect(device.updatedAt).toBeNull()
      device.updatedAt = DateTime.utc(2020, 12, 24, 8, 42, 52)
      expect(device.updatedAt.year).toEqual(2020)
      expect(device.updatedAt.month).toEqual(12)
      expect(device.updatedAt.day).toEqual(24)
      expect(device.updatedAt.hour).toEqual(8)
      expect(device.updatedAt.minute).toEqual(42)
      expect(device.updatedAt.second).toEqual(52)
      expect(device.updatedAt.zoneName).toEqual('UTC')
    })
  })
})
