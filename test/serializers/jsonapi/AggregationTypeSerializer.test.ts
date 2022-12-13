/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2022
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
})
