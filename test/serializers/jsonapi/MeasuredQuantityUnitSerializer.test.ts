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
import { MeasuredQuantityUnit } from '@/models/MeasuredQuantityUnit'
import { MeasuredQuantityUnitSerializer } from '@/serializers/jsonapi/MeasuredQuantityUnitSerializer'

describe('MeasuredQuantityUnitSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            default_limit_min: '0.01',
            default_limit_max: '100'
          },
          id: '1',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/measuredquantityunits/1/'
          },
          relationships: {
            unit: {
              data: {
                type: 'Unit',
                id: '61'
              },
              links: {
                self: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/measuredquantityunits/1/relationships/unit'
              }
            },
            measured_quantity: {
              data: {
                type: 'MeasuredQuantity',
                id: '1'
              },
              links: {
                self: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/measuredquantityunits/1/relationships/measured_quantity'
              }
            }
          },
          type: 'MeasuredQuantityUnit'
        },
        {
          attributes: {
            default_limit_min: '0.01',
            default_limit_max: '100'
          },
          id: '2',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/measuredquantityunits/2/'
          },
          relationships: {
            unit: {
              data: {
                type: 'Unit',
                id: '67'
              },
              links: {
                self: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/measuredquantityunits/2/relationships/unit'
              }
            },
            measured_quantity: {
              data: {
                type: 'MeasuredQuantity',
                id: '1'
              },
              links: {
                self: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/measuredquantityunits/2/relationships/measured_quantity'
              }
            }
          },
          type: 'MeasuredQuantityUnit'
        }],
        included: [
          {
            type: 'Unit',
            id: '61',
            attributes: {
              term: 'mg/l',
              definition: null,
              provenance: 'MILLIGRAMS_PER_LITER',
              provenance_uri: null,
              category: null,
              note: null,
              status: 'ACCEPTED'
            },
            links: {
              self: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/units/61/'
            }
          },
          {
            type: 'Unit',
            id: '67',
            attributes: {
              term: 'µg/l',
              definition: null,
              provenance: 'MICROGRAMS_PER_LITER',
              provenance_uri: null,
              category: null,
              note: null,
              status: 'ACCEPTED'
            },
            links: {
              self: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/units/67/'
            }
          }
        ],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedUnit1 = MeasuredQuantityUnit.createFromObject({
        id: '1',
        name: 'mg/l',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/measuredquantityunits/1/',
        defaultLimitMin: '0.01',
        defaultLimitMax: '100',
        unitId: '61',
        measuredQuantityId: '1'
      })

      const expectedUnit2 = MeasuredQuantityUnit.createFromObject({
        id: '2',
        name: 'µg/l',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/measuredquantityunits/2/',
        defaultLimitMin: '0.01',
        defaultLimitMax: '100',
        unitId: '67',
        measuredQuantityId: '1'
      })

      const serializer = new MeasuredQuantityUnitSerializer()
      serializer.included = jsonApiObjectList.included

      const units = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(units)).toBeTruthy()
      expect(units.length).toEqual(2)
      expect(units[0]).toEqual(expectedUnit1)
      expect(units[1]).toEqual(expectedUnit2)
    })
  })
})
