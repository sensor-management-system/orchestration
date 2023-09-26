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
import { PlatformType } from '@/models/PlatformType'
import { PlatformTypeSerializer } from '@/serializers/jsonapi/PlatformTypeSerializer'

describe('PlatformTypeSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            category: 'some category',
            definition: 'Some longer definition',
            note: null,
            provenance: 'Definition adapted from Wikipedia',
            provenance_uri: null,
            status: 'Accepted',
            term: 'Station'
          },
          id: '1',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/platformtypes/1/'
          },
          relationships: {
            global_provenence: {
              data: null
            }
          },
          type: 'PlatformType'
        }, {
          attributes: {
            category: 'some other category',
            definition: 'A short definition',
            note: 'sample note',
            provenance: 'somewhere',
            provenance_uri: 'abc',
            status: 'Accepted',
            term: 'Drone'
          },
          id: '2',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/platformtypes/2/'
          },
          relationships: {
            global_provenance: {
              data: {
                id: '1',
                type: 'GlobalProvenance'
              }
            }
          },
          type: 'PlatformType'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedPlatformType1 = PlatformType.createFromObject({
        id: '1',
        name: 'Station',
        category: 'some category',
        definition: 'Some longer definition',
        note: '',
        provenance: 'Definition adapted from Wikipedia',
        provenanceUri: '',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/platformtypes/1/',
        globalProvenanceId: null
      })
      const expectedPlatformType2 = PlatformType.createFromObject({
        id: '2',
        name: 'Drone',
        category: 'some other category',
        definition: 'A short definition',
        note: 'sample note',
        provenance: 'somewhere',
        provenanceUri: 'abc',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/platformtypes/2/',
        globalProvenanceId: '1'
      })

      const serializer = new PlatformTypeSerializer()

      const platformTypes = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(platformTypes)).toBeTruthy()
      expect(platformTypes.length).toEqual(2)
      expect(platformTypes[0]).toEqual(expectedPlatformType1)
      expect(platformTypes[1]).toEqual(expectedPlatformType2)
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should transform the model to json payload', () => {
      const platformType = PlatformType.createFromObject({
        id: '2',
        name: 'AutomaticLevel',
        category: 'Instrument',
        definition: 'A survey level that makes use of a compensator that ensures the line of sight remains horizontal once the operator has roughly leveled the instrument.',
        provenance: 'Definition adapted from Wikipedia. See http://en.wikipedia.org/wiki/Levelling',
        provenanceUri: 'abc',
        note: 'simple note',
        globalProvenanceId: '1',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/platformtypes/2/'
      })

      const expectedResult = {
        id: '2',
        type: 'PlatformType',
        attributes: {
          term: 'AutomaticLevel',
          category: 'Instrument',
          definition: 'A survey level that makes use of a compensator that ensures the line of sight remains horizontal once the operator has roughly leveled the instrument.',
          provenance: 'Definition adapted from Wikipedia. See http://en.wikipedia.org/wiki/Levelling',
          provenance_uri: 'abc',
          note: 'simple note'
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

      const serializer = new PlatformTypeSerializer()
      const result = serializer.convertModelToJsonApiData(platformType)

      expect(result).toEqual(expectedResult)
    })
  })
})
