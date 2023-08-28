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
import { Manufacturer } from '@/models/Manufacturer'
import { ManufacturerSerializer } from '@/serializers/jsonapi/ManufacturerSerializer'

describe('ManufacturerSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            category: null,
            definition: 'ecoTech Umwelt-Meßsysteme GmbH',
            note: null,
            provenance: null,
            provenance_uri: null,
            status: 'Accepted',
            term: 'ecoTech'
          },
          id: '1',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/manufacturers/1/'
          },
          relationships: {
            global_provenence: {
              data: null
            }
          },
          type: 'Manufacturer'
        }, {
          attributes: {
            category: 'category',
            definition: 'Campbell Scientific Ltd.',
            note: 'note',
            provenance: 'provenance',
            provenance_uri: 'provenance uri',
            status: 'Accepted',
            term: 'Campbell'
          },
          id: '2',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/manufacturers/2/'
          },
          relationships: {
            global_provenance: {
              data: {
                id: '1',
                type: 'GlobalProvenance'
              }
            }
          },
          type: 'Manufacturer'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedManufacturer1 = Manufacturer.createFromObject({
        id: '1',
        name: 'ecoTech',
        definition: 'ecoTech Umwelt-Meßsysteme GmbH',
        provenance: '',
        provenanceUri: '',
        category: '',
        note: '',
        globalProvenanceId: null,
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/manufacturers/1/'
      })
      const expectedManufacturer2 = Manufacturer.createFromObject({
        id: '2',
        name: 'Campbell',
        category: 'category',
        definition: 'Campbell Scientific Ltd.',
        note: 'note',
        provenance: 'provenance',
        provenanceUri: 'provenance uri',
        globalProvenanceId: '1',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/manufacturers/2/'
      })

      const serializer = new ManufacturerSerializer()

      const manufacturers = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(manufacturers)).toBeTruthy()
      expect(manufacturers.length).toEqual(2)
      expect(manufacturers[0]).toEqual(expectedManufacturer1)
      expect(manufacturers[1]).toEqual(expectedManufacturer2)
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should transform the model to json payload', () => {
      const manufacturer = Manufacturer.createFromObject({
        id: '2',
        name: 'Some Coorp',
        category: 'special',
        definition: 'No idea what we want to put in there for manufacturers.',
        provenance: 'website?',
        provenanceUri: 'https://somewhere.at.net',
        note: 'simple note',
        globalProvenanceId: '1',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/manufacturers/2/'
      })

      const expectedResult = {
        id: '2',
        type: 'Manufacturer',
        attributes: {
          category: 'special',
          definition: 'No idea what we want to put in there for manufacturers.',
          provenance: 'website?',
          provenance_uri: 'https://somewhere.at.net',
          note: 'simple note',
          term: 'Some Coorp'
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

      const serializer = new ManufacturerSerializer()
      const result = serializer.convertModelToJsonApiData(manufacturer)

      expect(result).toEqual(expectedResult)
    })
  })
})
