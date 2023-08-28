/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2022
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
import { Status } from '@/models/Status'
import { StatusSerializer } from '@/serializers/jsonapi/StatusSerializer'

describe('StatusSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            category: null,
            definition: 'Data collection is complete. No new data values will be added.',
            note: null,
            provenance: null,
            provenance_uri: null,
            status: 'Accepted',
            term: 'Complete'
          },
          id: '1',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/equipmentstatus/1/'
          },
          relationships: {
            global_provenence: {
              data: null
            }
          },
          type: 'EqauipmentStatus'
        }, {
          attributes: {
            category: 'a category',
            definition: 'Data collection is ongoing.  New data values will be added periodically.',
            note: 'a note',
            provenance: 'a provenance',
            provenance_uri: 'https://provenance',
            status: 'Accepted',
            term: 'Ongoing'
          },
          id: '2',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/equipmentstatus/2/'
          },
          relationships: {
            global_provenance: {
              data: {
                id: '1',
                type: 'GlobalProvenance'
              }
            }
          },
          type: 'EqauipmentStatus'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedStatus1 = Status.createFromObject({
        id: '1',
        name: 'Complete',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/equipmentstatus/1/',
        definition: 'Data collection is complete. No new data values will be added.',
        category: '',
        note: '',
        provenance: '',
        provenanceUri: '',
        globalProvenanceId: null
      })
      const expectedStatus2 = Status.createFromObject({
        id: '2',
        name: 'Ongoing',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/equipmentstatus/2/',
        definition: 'Data collection is ongoing.  New data values will be added periodically.',
        category: 'a category',
        note: 'a note',
        provenance: 'a provenance',
        provenanceUri: 'https://provenance',
        globalProvenanceId: '1'
      })

      const serializer = new StatusSerializer()

      const states = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(states)).toBeTruthy()
      expect(states.length).toEqual(2)
      expect(states[0]).toEqual(expectedStatus1)
      expect(states[1]).toEqual(expectedStatus2)
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should transform the model to json payload', () => {
      const status = Status.createFromObject({
        id: '2',
        name: 'Ongoing',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/equipmentstatus/2/',
        definition: 'Data collection is ongoing.  New data values will be added periodically.',
        category: 'a category',
        note: 'a note',
        provenance: 'a provenance',
        provenanceUri: 'https://provenance',
        globalProvenanceId: '1'
      })

      const expectedResult = {
        id: '2',
        type: 'EquipmentStatus',
        attributes: {
          term: 'Ongoing',
          category: 'a category',
          definition: 'Data collection is ongoing.  New data values will be added periodically.',
          provenance: 'a provenance',
          provenance_uri: 'https://provenance',
          note: 'a note'
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

      const serializer = new StatusSerializer()
      const result = serializer.convertModelToJsonApiData(status)

      expect(result).toEqual(expectedResult)
    })
  })
})
