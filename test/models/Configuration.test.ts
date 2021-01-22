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
import { Configuration } from '@/models/Configuration'

describe('Configuration', () => {
  describe('#projectName', () => {
    it('should be an empty string by default', () => {
      const configuration = new Configuration()
      expect(configuration.projectName).toEqual('')
    })
    it('should be possible to set it', () => {
      const configuration = new Configuration()
      configuration.projectName = 'abc'
      expect(configuration.projectName).toEqual('abc')
    })
  })
  describe('#projectUri', () => {
    it('should be an empty string by default', () => {
      const configuration = new Configuration()
      expect(configuration.projectUri).toEqual('')
    })
    it('should be possible to set it', () => {
      const configuration = new Configuration()
      configuration.projectUri = 'project/abc'
      expect(configuration.projectUri).toEqual('project/abc')
    })
  })
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
    it('should be possible to set projectName, -uri, label & status with it', () => {
      const configurationToCopyFrom = new Configuration()
      configurationToCopyFrom.projectName = 'Tereno NO'
      configurationToCopyFrom.projectUri = 'projects/tereno-no'
      configurationToCopyFrom.label = 'Boeken'
      configurationToCopyFrom.status = 'draft'

      expect(configurationToCopyFrom.startDate).toBeNull()
      expect(configurationToCopyFrom.endDate).toBeNull()

      const result = Configuration.createFromObject(configurationToCopyFrom)

      expect(result.projectName).toEqual('Tereno NO')
      expect(result.projectUri).toEqual('projects/tereno-no')
      expect(result.label).toEqual('Boeken')
      expect(result.status).toEqual('draft')
      expect(result.startDate).toBeNull()
      expect(result.endDate).toBeNull()
    })
    it('should also copy the start and end dates', () => {
      const configurationToCopyFrom = new Configuration()
      configurationToCopyFrom.projectName = 'Tereno NO'
      configurationToCopyFrom.projectUri = 'projects/tereno-no'
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
