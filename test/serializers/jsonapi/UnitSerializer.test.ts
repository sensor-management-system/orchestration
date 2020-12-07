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
import { Unit } from '@/models/Unit'
import { UnitSerializer } from '@/serializers/jsonapi/UnitSerializer'

describe('UnitSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            category: null,
            definition: null,
            note: null,
            provenance: 'ONE_PER_METER',
            provenance_uri: null,
            status: 'ACCEPTED',
            term: '1/m'
          },
          id: '1',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/units/1/'
          },
          relationships: {
            unitstype: {
              data: null,
              links: {
                self: 'http://rz-vm64.gfz-potsdam.de:5001/api/unit/Gray/unitstype'
              }
            }
          },
          type: 'Unit'
        },
        {
          attributes: {
            category: null,
            definition: null,
            note: null,
            provenance: 'ONE_PER_TIME',
            provenance_uri: null,
            status: 'ACCEPTED',
            term: '1/t'
          },
          id: '2',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/units/2/'
          },
          relationships: {
            unitstype: {
              data: null,
              links: {
                self: 'http://rz-vm64.gfz-potsdam.de:5001/api/unit/RAD/unitstype'
              }
            }
          },
          type: 'Unit'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedUnit1 = Unit.createFromObject({
        id: '1',
        name: '1/m',
        uri: 'units/1'
      })

      const expectedUnit2 = Unit.createFromObject({
        id: '2',
        name: '1/t',
        uri: 'units/2'
      })

      const serializer = new UnitSerializer('http://rz-vm64.gfz-potsdam.de:5001/api')

      const units = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(units)).toBeTruthy()
      expect(units.length).toEqual(2)
      expect(units[0]).toEqual(expectedUnit1)
      expect(units[1]).toEqual(expectedUnit2)
    })
  })
})
