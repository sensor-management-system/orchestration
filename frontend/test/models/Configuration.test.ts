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
  describe('#getConfigurationStatus', () => {
    it('should return draft if there is no start date', () => {
      const date = DateTime.utc(
        2021, // year
        1, // month (1 based)
        22, // day
        7, // hour
        15, // minute
        57 // second
      )
      const configuration = new Configuration()
      expect(configuration.getConfigurationStatus(date)).toEqual('draft')
    })
    it('should return draft if the start date is after the test date', () => {
      const date = DateTime.utc(
        2021, // year
        1, // month (1 based)
        22, // day
        7, // hour
        15, // minute
        57 // second
      )
      const startDate = DateTime.utc(
        2022,
        1,
        22,
        7,
        15,
        57
      )
      const configuration = new Configuration()
      configuration.startDate = startDate
      expect(configuration.getConfigurationStatus(date)).toEqual('draft')
    })
    it('should return active if the start date is before the test date', () => {
      const date = DateTime.utc(
        2021, // year
        1, // month (1 based)
        22, // day
        7, // hour
        15, // minute
        57 // second
      )
      const startDate = DateTime.utc(
        2020,
        1,
        22,
        7,
        15,
        57
      )
      const configuration = new Configuration()
      configuration.startDate = startDate
      expect(configuration.getConfigurationStatus(date)).toEqual('active')
    })
    it('should return active if the start date is before the test date and the end date is after the test date', () => {
      const date = DateTime.utc(
        2021, // year
        1, // month (1 based)
        22, // day
        7, // hour
        15, // minute
        57 // second
      )
      const startDate = DateTime.utc(
        2020,
        1,
        22,
        7,
        15,
        57
      )
      const endDate = DateTime.utc(
        2022,
        1,
        22,
        7,
        15,
        57
      )
      const configuration = new Configuration()
      configuration.startDate = startDate
      configuration.endDate = endDate
      expect(configuration.getConfigurationStatus(date)).toEqual('active')
    })
    it('should return deprecated if the end date is before the test date', () => {
      const date = DateTime.utc(
        2021, // year
        1, // month (1 based)
        22, // day
        7, // hour
        15, // minute
        57 // second
      )
      const startDate = DateTime.utc(
        2019,
        1,
        22,
        7,
        15,
        57
      )
      const endDate = DateTime.utc(
        2020,
        1,
        22,
        7,
        15,
        57
      )
      const configuration = new Configuration()
      configuration.startDate = startDate
      configuration.endDate = endDate
      expect(configuration.getConfigurationStatus(date)).toEqual('deprecated')
    })
    it('should return deprecated if there is only an end date in the past', () => {
      const date = DateTime.utc(
        2021, // year
        1, // month (1 based)
        22, // day
        7, // hour
        15, // minute
        57 // second
      )
      const endDate = DateTime.utc(
        2020,
        1,
        22,
        7,
        15,
        57
      )
      const configuration = new Configuration()
      configuration.endDate = endDate
      expect(configuration.getConfigurationStatus(date)).toEqual('deprecated')
    })
    it('should return active if there is only an end date in the future', () => {
      const date = DateTime.utc(
        2021, // year
        1, // month (1 based)
        22, // day
        7, // hour
        15, // minute
        57 // second
      )
      const endDate = DateTime.utc(
        2023,
        1,
        22,
        7,
        15,
        57
      )
      const configuration = new Configuration()
      configuration.endDate = endDate
      expect(configuration.getConfigurationStatus(date)).toEqual('active')
    })
  })
  describe('createFromObject', () => {
    it('should be possible to set label & status with it', () => {
      const configurationToCopyFrom = new Configuration()
      configurationToCopyFrom.label = 'Boeken'

      expect(configurationToCopyFrom.startDate).toBeNull()
      expect(configurationToCopyFrom.endDate).toBeNull()

      const result = Configuration.createFromObject(configurationToCopyFrom)

      expect(result.label).toEqual('Boeken')
      expect(result.startDate).toBeNull()
      expect(result.endDate).toBeNull()
    })
    it('should also copy the start and end dates', () => {
      const configurationToCopyFrom = new Configuration()
      configurationToCopyFrom.label = 'Boeken'

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
