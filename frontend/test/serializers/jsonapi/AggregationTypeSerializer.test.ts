/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AggregationType } from '@/models/AggregationType'
import { AggregationTypeSerializer } from '@/serializers/jsonapi/AggregationTypeSerializer'

describe('AggregationTypeSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            category: null,
            definition: '',
            note: null,
            provenance: '',
            provenance_uri: null,
            status: 'ACCEPTED',
            term: 'Average'
          },
          id: '1',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/aggregationtypes/1/'
          },
          relationships: {
            global_provenence: {
              data: null
            }
          },
          type: 'AggregationType'
        }, {
          attributes: {
            category: 'category',
            definition: 'def',
            note: 'note',
            provenance: 'prov',
            provenance_uri: 'uri',
            status: 'ACCEPTED',
            term: 'Categorical'
          },
          id: '2',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/aggregationtypes/2/'
          },
          relationships: {
            global_provenance: {
              data: {
                id: '1',
                type: 'GlobalProvenance'
              }
            }
          },
          type: 'AggregationType'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedAggregationType1 = AggregationType.createFromObject({
        id: '1',
        name: 'Average',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/aggregationtypes/1/',
        definition: '',
        category: '',
        note: '',
        provenance: '',
        provenanceUri: '',
        globalProvenanceId: null
      })
      const expectedAggregationType2 = AggregationType.createFromObject({
        id: '2',
        name: 'Categorical',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/aggregationtypes/2/',
        definition: 'def',
        category: 'category',
        note: 'note',
        provenance: 'prov',
        provenanceUri: 'uri',
        globalProvenanceId: '1'
      })

      const serializer = new AggregationTypeSerializer()

      const aggregationTypes = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(aggregationTypes)).toBeTruthy()
      expect(aggregationTypes.length).toEqual(2)
      expect(aggregationTypes[0]).toEqual(expectedAggregationType1)
      expect(aggregationTypes[1]).toEqual(expectedAggregationType2)
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should transform the model to json payload', () => {
      const cvAggregation = AggregationType.createFromObject({
        id: '2',
        name: 'Average',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/aggregationtypes/2/',
        definition: 'mean',
        category: 'cat',
        note: 'note',
        provenance: 'statistics handbook',
        provenanceUri: 'uri',
        globalProvenanceId: '1'
      })

      const expectedResult = {
        attributes: {
          category: 'cat',
          definition: 'mean',
          note: 'note',
          provenance: 'statistics handbook',
          provenance_uri: 'uri',
          term: 'Average'
        },
        id: '2',
        relationships: {
          global_provenance: {
            data: {
              id: '1',
              type: 'GlobalProvenance'
            }
          }
        },
        type: 'AggregationType'
      }

      const serializer = new AggregationTypeSerializer()
      const result = serializer.convertModelToJsonApiData(cvAggregation)

      expect(result).toEqual(expectedResult)
    })
  })
})
