/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'
import { Contact } from '@/models/Contact'
import { Parameter } from '@/models/Parameter'

describe('Parameter', () => {
  describe('#createdAt', () => {
    it('should allow to set a datetime', () => {
      const parameter = new Parameter()
      expect(parameter.createdAt).toBeNull()
      parameter.createdAt = DateTime.utc(2023, 1, 22, 7, 32, 42)
      expect(parameter.createdAt.year).toEqual(2023)
      expect(parameter.createdAt.month).toEqual(1)
      expect(parameter.createdAt.day).toEqual(22)
      expect(parameter.createdAt.hour).toEqual(7)
      expect(parameter.createdAt.minute).toEqual(32)
      expect(parameter.createdAt.second).toEqual(42)
      expect(parameter.createdAt.zoneName).toEqual('UTC')
    })
  })
  describe('#updatedAt', () => {
    it('should allow to set a datetime', () => {
      const parameter = new Parameter()
      expect(parameter.updatedAt).toBeNull()
      parameter.updatedAt = DateTime.utc(2020, 12, 24, 8, 42, 52)
      expect(parameter.updatedAt.year).toEqual(2020)
      expect(parameter.updatedAt.month).toEqual(12)
      expect(parameter.updatedAt.day).toEqual(24)
      expect(parameter.updatedAt.hour).toEqual(8)
      expect(parameter.updatedAt.minute).toEqual(42)
      expect(parameter.updatedAt.second).toEqual(52)
      expect(parameter.updatedAt.zoneName).toEqual('UTC')
    })
  })
  describe('#createFromObject', () => {
    it('should create a Parameter instance from a plain object', () => {
      const date1 = DateTime.fromISO('2023-05-27')
      const date2 = DateTime.fromISO('2023-05-28')

      const contact1 = new Contact()
      contact1.givenName = 'Bart'
      contact1.familyName = 'Simpson'
      contact1.email = 'el.barto@springfield.com'

      const contact2 = new Contact()
      contact2.givenName = 'Lisa'
      contact2.familyName = 'Simpson'
      contact2.email = 'lisa.simpson@springfield.com'

      const parameter = Parameter.createFromObject({
        id: '1',
        label: 'example parameter',
        description: 'this is a parameter',
        unitUri: 'https://link/to/some/vocab/uri',
        unitName: 'example unit',
        createdAt: date1,
        updatedAt: date2,
        createdBy: contact1,
        updatedBy: contact2
      })

      expect(typeof parameter).toBe('object')
      expect(parameter).toHaveProperty('id', '1')
      expect(parameter).toHaveProperty('label', 'example parameter')
      expect(parameter).toHaveProperty('description', 'this is a parameter')
      expect(parameter).toHaveProperty('unitUri', 'https://link/to/some/vocab/uri')
      expect(parameter).toHaveProperty('unitName', 'example unit')
      expect(parameter.createdAt).toBe(date1)
      expect(parameter.updatedAt).toBe(date2)
      expect(parameter.createdBy).toStrictEqual(contact1)
      expect(parameter.updatedBy).toStrictEqual(contact2)
    })
  })
})
