/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
            definition: 'Unit 1',
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
            global_provenance: {
              data: null
            }
          },
          type: 'Unit'
        },
        {
          attributes: {
            category: 'cat',
            definition: 'Unit 2',
            note: 'note',
            provenance: 'ONE_PER_TIME',
            provenance_uri: 'uri',
            status: 'ACCEPTED',
            term: '1/t'
          },
          id: '2',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/units/2/'
          },
          relationships: {
            global_provenance: {
              data: {
                id: '1',
                type: 'GlobalProvenance'
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
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/units/1/',
        definition: 'Unit 1',
        category: '',
        note: '',
        provenance: 'ONE_PER_METER',
        provenanceUri: '',
        globalProvenanceId: null
      })

      const expectedUnit2 = Unit.createFromObject({
        id: '2',
        name: '1/t',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/units/2/',
        definition: 'Unit 2',
        category: 'cat',
        note: 'note',
        provenance: 'ONE_PER_TIME',
        provenanceUri: 'uri',
        globalProvenanceId: '1'
      })

      const serializer = new UnitSerializer()

      const units = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(units)).toBeTruthy()
      expect(units.length).toEqual(2)
      expect(units[0]).toEqual(expectedUnit1)
      expect(units[1]).toEqual(expectedUnit2)
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should transform the model to json payload', () => {
      const unit = Unit.createFromObject({
        id: '2',
        name: '1/t',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/units/2/',
        definition: 'Unit 2',
        category: 'cat',
        note: 'note',
        provenance: 'ONE_PER_TIME',
        provenanceUri: 'uri',
        globalProvenanceId: '1'
      })

      const expectedResult = {
        id: '2',
        type: 'Unit',
        attributes: {
          category: 'cat',
          definition: 'Unit 2',
          note: 'note',
          provenance: 'ONE_PER_TIME',
          provenance_uri: 'uri',
          term: '1/t'
        },
        relationships: {
          global_provenance: {
            data: {
              id: '1',
              type: 'GlobalProvenance'
            }
          }
        }
      }

      const serializer = new UnitSerializer()
      const result = serializer.convertModelToJsonApiData(unit)

      expect(result).toEqual(expectedResult)
    })
  })
})
