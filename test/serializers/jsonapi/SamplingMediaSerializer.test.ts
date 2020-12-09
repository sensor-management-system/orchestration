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
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/samplingmedium/1/'
          },
          relationships: {},
          type: 'Samplingmedium'
        }, {
          attributes: {
            category: null,
            definition: 'An instrument, sensor or other piece of human-made equipment upon which a measurement is made, such as datalogger temperature or battery voltage.',
            note: null,
            provenance: null,
            provenance_uri: null,
            status: 'Accepted',
            term: 'Equipment'
          },
          id: '2',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/samplingmedium/2/'
          },
          relationships: {},
          type: 'Samplingmedium'
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
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/samplingmedium/1/'
      })
      const expectedSamplingMedium2 = SamplingMedia.createFromObject({
        id: '2',
        name: 'Equipment',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/samplingmedium/2/'
      })

      const serializer = new SamplingMediaSerializer()

      const samplingMedia = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(samplingMedia)).toBeTruthy()
      expect(samplingMedia.length).toEqual(2)
      expect(samplingMedia[0]).toEqual(expectedSamplingMedium1)
      expect(samplingMedia[1]).toEqual(expectedSamplingMedium2)
    })
  })
})
