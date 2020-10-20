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
            active: true,
            term: 'gray',
            unitsabbreviation: 'Gy',
            unitslink: 'http://qudt.org/vocab/unit#Gray; http://unitsofmeasure.org/ucum.html#para-30',
            unitsname: 'Gray',
            unitstypecv: 'Absorbed dose'
          },
          id: 'Gray',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/unit/Gray/'
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
            active: true,
            term: 'rad',
            unitsabbreviation: '',
            unitslink: 'http://qudt.org/vocab/unit#Rad; http://unitsofmeasure.org/ucum.html#para-33',
            unitsname: 'RAD',
            unitstypecv: 'Absorbed dose'
          },
          id: 'RAD',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/unit/RAD/'
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
        id: 'Gray',
        name: 'Gray [Gy]',
        uri: 'unit/Gray'
      })

      const expectedUnit2 = Unit.createFromObject({
        id: 'RAD',
        name: 'RAD',
        uri: 'unit/RAD'
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
