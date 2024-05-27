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
import { Platform } from '@/models/Platform'

describe('Platform', () => {
  describe('#createdAt', () => {
    it('should allow to set a datetime', () => {
      const platform = new Platform()
      expect(platform.createdAt).toBeNull()
      platform.createdAt = DateTime.utc(2021, 1, 22, 7, 32, 42)
      expect(platform.createdAt.year).toEqual(2021)
      expect(platform.createdAt.month).toEqual(1)
      expect(platform.createdAt.day).toEqual(22)
      expect(platform.createdAt.hour).toEqual(7)
      expect(platform.createdAt.minute).toEqual(32)
      expect(platform.createdAt.second).toEqual(42)
      expect(platform.createdAt.zoneName).toEqual('UTC')
    })
  })
  describe('#updatedAt', () => {
    it('should allow to set a datetime', () => {
      const platform = new Platform()
      expect(platform.updatedAt).toBeNull()
      platform.updatedAt = DateTime.utc(2020, 12, 24, 8, 42, 52)
      expect(platform.updatedAt.year).toEqual(2020)
      expect(platform.updatedAt.month).toEqual(12)
      expect(platform.updatedAt.day).toEqual(24)
      expect(platform.updatedAt.hour).toEqual(8)
      expect(platform.updatedAt.minute).toEqual(42)
      expect(platform.updatedAt.second).toEqual(52)
      expect(platform.updatedAt.zoneName).toEqual('UTC')
    })
  })
})
