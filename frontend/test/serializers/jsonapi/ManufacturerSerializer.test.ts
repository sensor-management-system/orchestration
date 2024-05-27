/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
