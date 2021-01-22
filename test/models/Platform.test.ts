/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
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
