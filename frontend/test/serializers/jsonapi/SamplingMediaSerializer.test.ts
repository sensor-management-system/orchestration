/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { SamplingMedia } from '@/models/SamplingMedia'
import { SamplingMediaSerializer } from '@/serializers/jsonapi/SamplingMediaSerializer'

describe('SamplingMediaSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            category: null,
            definition: 'Specimen collection of ambient air or sensor emplaced to measure properties of ambient air.',
            note: null,
            provenance: null,
            provenance_uri: null,
            status: 'Accepted',
            term: 'Air'
          },
          id: '1',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/samplingmedia/1/'
          },
          relationships: {
            compartment: {
              data: {
                type: 'Compartment',
                id: '5'
              }
            },
            global_provenance: {
              data: null
            }
          },
          type: 'SamplingMedium'
        }, {
          attributes: {
            category: 'categ',
            definition: 'An instrument, sensor or other piece of human-made equipment upon which a measurement is made, such as datalogger temperature or battery voltage.',
            note: 'note',
            provenance: 'prov',
            provenance_uri: 'uri',
            status: 'Accepted',
            term: 'Equipment'
          },
          id: '2',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/samplingmedia/2/'
          },
          relationships: {
            compartment: {
              data: {
                type: 'Compartment',
                id: '2'
              }
            },
            global_provenance: {
              data: {
                id: '1',
                type: 'GlobalProvenance'
              }
            }
          },
          type: 'SamplingMedium'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedSamplingMedium1 = SamplingMedia.createFromObject({
        id: '1',
        name: 'Air',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/samplingmedia/1/',
        definition: 'Specimen collection of ambient air or sensor emplaced to measure properties of ambient air.',
        compartmentId: '5',
        category: '',
        note: '',
        provenance: '',
        provenanceUri: '',
        globalProvenanceId: null
      })
      const expectedSamplingMedium2 = SamplingMedia.createFromObject({
        id: '2',
        name: 'Equipment',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/samplingmedia/2/',
        definition: 'An instrument, sensor or other piece of human-made equipment upon which a measurement is made, such as datalogger temperature or battery voltage.',
        compartmentId: '2',
        category: 'categ',
        note: 'note',
        provenance: 'prov',
        provenanceUri: 'uri',
        globalProvenanceId: '1'
      })

      const serializer = new SamplingMediaSerializer()

      const samplingMedia = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(samplingMedia)).toBeTruthy()
      expect(samplingMedia.length).toEqual(2)
      expect(samplingMedia[0]).toEqual(expectedSamplingMedium1)
      expect(samplingMedia[1]).toEqual(expectedSamplingMedium2)
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should transform the model to json payload', () => {
      const smplingMedium = SamplingMedia.createFromObject({
        id: '2',
        name: 'Equipment',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/samplingmedia/2/',
        definition: 'An instrument, sensor or other piece of human-made equipment upon which a measurement is made, such as datalogger temperature or battery voltage.',
        compartmentId: '2',
        category: 'categ',
        note: 'note',
        provenance: 'prov',
        provenanceUri: 'uri',
        globalProvenanceId: '1'
      })

      const expectedResult = {
        attributes: {
          category: 'categ',
          definition: 'An instrument, sensor or other piece of human-made equipment upon which a measurement is made, such as datalogger temperature or battery voltage.',
          note: 'note',
          provenance: 'prov',
          provenance_uri: 'uri',
          term: 'Equipment'
        },
        id: '2',
        relationships: {
          compartment: {
            data: {
              type: 'Compartment',
              id: '2'
            }
          },
          global_provenance: {
            data: {
              id: '1',
              type: 'GlobalProvenance'
            }
          }
        },
        type: 'SamplingMedium'
      }

      const serializer = new SamplingMediaSerializer()
      const result = serializer.convertModelToJsonApiData(smplingMedium)

      expect(result).toEqual(expectedResult)
    })
  })
})
