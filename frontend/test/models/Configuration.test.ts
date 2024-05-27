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
import { Configuration } from '@/models/Configuration'

describe('Configuration', () => {
  describe('#label', () => {
    it('should be an empty string by default', () => {
      const configuration = new Configuration()
      expect(configuration.label).toEqual('')
    })
    it('should be possible to set it', () => {
      const configuration = new Configuration()
      configuration.label = 'new configuration'
      expect(configuration.label).toEqual('new configuration')
    })
  })
  describe('#status', () => {
    it('should be an empty string by default', () => {
      const configuration = new Configuration()
      expect(configuration.status).toEqual('')
    })
    it('should be possible to set it', () => {
      const configuration = new Configuration()
      configuration.status = 'draft'
      expect(configuration.status).toEqual('draft')
    })
  })
  describe('createFromObject', () => {
    it('should be possible to set label & status with it', () => {
      const configurationToCopyFrom = new Configuration()
      configurationToCopyFrom.label = 'Boeken'
      configurationToCopyFrom.status = 'draft'

      expect(configurationToCopyFrom.startDate).toBeNull()
      expect(configurationToCopyFrom.endDate).toBeNull()

      const result = Configuration.createFromObject(configurationToCopyFrom)

      expect(result.label).toEqual('Boeken')
      expect(result.status).toEqual('draft')
      expect(result.startDate).toBeNull()
      expect(result.endDate).toBeNull()
    })
    it('should also copy the start and end dates', () => {
      const configurationToCopyFrom = new Configuration()
      configurationToCopyFrom.label = 'Boeken'
      configurationToCopyFrom.status = 'draft'

      configurationToCopyFrom.startDate = DateTime.utc(
        2021, // year
        1, // month (1 based)
        22, // day
        7, // hour
        15, // minute
        57 // second
      )
      configurationToCopyFrom.endDate = DateTime.utc(2021, 1, 31, 23, 59, 59)

      const result = Configuration.createFromObject(configurationToCopyFrom)

      expect(result.startDate).not.toBeNull()
      if (result.startDate !== null) {
        expect(result.startDate.year).toEqual(2021)
        expect(result.startDate.month).toEqual(1)
        expect(result.startDate.day).toEqual(22)
        expect(result.startDate.hour).toEqual(7)
        expect(result.startDate.minute).toEqual(15)
        expect(result.startDate.second).toEqual(57)
        expect(result.startDate.zoneName).toEqual('UTC')
      }
      expect(result.endDate).not.toBeNull()
      if (result.endDate !== null) {
        expect(result.endDate.day).toEqual(31)
        expect(result.endDate.hour).toEqual(23)
        expect(result.endDate.minute).toEqual(59)
        expect(result.endDate.second).toEqual(59)
        expect(result.endDate.zoneName).toEqual('UTC')
      }

      // and as the luxon DateTime objects are immutable, we don't
      // change anything
      const newDate = configurationToCopyFrom.startDate.set({
        year: 2030
      })
      expect(newDate.year).toEqual(2030)
      expect(configurationToCopyFrom.startDate.year).toEqual(2021)
      if (result.startDate !== null) {
        expect(result.startDate.year).toEqual(2021)
      }
    })
  })
})
