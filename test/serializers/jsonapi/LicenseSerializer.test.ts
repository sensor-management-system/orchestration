/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2023
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
import { License } from '@/models/License'
import { LicenseSerializer } from '@/serializers/jsonapi/LicenseSerializer'

describe('LicenseSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            category: 'Software license',
            definition: 'A simple license',
            note: null,
            provenance: 'See MIT',
            provenance_uri: null,
            status: 'Accepted',
            term: 'MIT'
          },
          id: '1',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/licenses/1/'
          },
          relationships: {
            global_provenence: {
              data: null
            }
          },
          type: 'License'
        }, {
          attributes: {
            category: 'Data license',
            definition: 'CC',
            note: 'simple note',
            provenance: 'Definition adapted from Wikipedia. See http://en.wikipedia.org/wiki/CC4',
            provenance_uri: 'abc',
            status: 'Accepted',
            term: 'CC4'
          },
          id: '2',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/licenses/2/'
          },
          relationships: {
            global_provenance: {
              data: {
                id: '1',
                type: 'GlobalProvenance'
              }
            }
          },
          type: 'License'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedLicense1 = License.createFromObject({
        id: '1',
        name: 'MIT',
        definition: 'A simple license',
        provenance: 'See MIT',
        provenanceUri: '',
        note: '',
        category: 'Software license',
        globalProvenanceId: null,
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/licenses/1/'

      })
      const expectedLicense2 = License.createFromObject({
        id: '2',
        name: 'CC4',
        category: 'Data license',
        definition: 'CC',
        provenance: 'Definition adapted from Wikipedia. See http://en.wikipedia.org/wiki/CC4',
        provenanceUri: 'abc',
        note: 'simple note',
        globalProvenanceId: '1',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/licenses/2/'
      })

      const serializer = new LicenseSerializer()

      const licenses = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(licenses)).toBeTruthy()
      expect(licenses.length).toEqual(2)
      expect(licenses[0]).toEqual(expectedLicense1)
      expect(licenses[1]).toEqual(expectedLicense2)
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should transform the model to json payload', () => {
      const license = License.createFromObject({
        id: '2',
        name: 'CC4',
        category: 'Data license',
        definition: 'CC',
        provenance: 'Definition adapted from Wikipedia. See http://en.wikipedia.org/wiki/CC4',
        provenanceUri: 'abc',
        note: 'simple note',
        globalProvenanceId: '1',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/licenses/2/'
      })

      const expectedResult = {
        id: '2',
        type: 'License',
        attributes: {
          category: 'Data license',
          definition: 'CC',
          note: 'simple note',
          provenance: 'Definition adapted from Wikipedia. See http://en.wikipedia.org/wiki/CC4',
          provenance_uri: 'abc',
          term: 'CC4'
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

      const serializer = new LicenseSerializer()
      const result = serializer.convertModelToJsonApiData(license)

      expect(result).toEqual(expectedResult)
    })
  })
})
