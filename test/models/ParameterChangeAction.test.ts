/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2023
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
