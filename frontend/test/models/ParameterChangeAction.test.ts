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
import { ParameterChangeAction } from '@/models/ParameterChangeAction'

describe('Parameter', () => {
  describe('#createFromObject', () => {
    it('should create a ParameterChangeAction instance from a plain object', () => {
      const parameter = Parameter.createFromObject({
        id: '20',
        label: 'Test Param',
        description: 'This is a test param',
        unitUri: 'http://example.com/param1',
        unitName: 'Param1'
      })

      const date1 = DateTime.fromISO('2023-05-27')

      const contact1 = new Contact()
      contact1.givenName = 'Bart'
      contact1.familyName = 'Simpson'
      contact1.email = 'el.barto@springfield.com'

      const action = ParameterChangeAction.createFromObject({
        id: '1',
        date: date1,
        value: 'some value',
        description: 'a description of the parameter change',
        contact: contact1,
        parameter
      })

      expect(typeof action).toBe('object')
      expect(action).toHaveProperty('id', '1')
      expect(action.date).toBe(date1)
      expect(action).toHaveProperty('value', 'some value')
      expect(action).toHaveProperty('description', 'a description of the parameter change')
      expect(action.contact).toStrictEqual(contact1)
      expect(action.parameter).toStrictEqual(parameter)
    })
  })
})
