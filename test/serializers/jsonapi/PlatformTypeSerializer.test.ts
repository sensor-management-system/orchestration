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
import { PlatformType } from '@/models/PlatformType'
import { PlatformTypeSerializer } from '@/serializers/jsonapi/PlatformTypeSerializer'

describe('PlatformTypeSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            category: null,
            definition: null,
            note: null,
            provenance: null,
            provenance_uri: null,
            status: 'Accepted',
            term: 'Station'
          },
          id: '1',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/platformtypes/1/'
          },
          relationships: {},
          type: 'Platformtype'
        }, {
          attributes: {
            category: null,
            definition: null,
            note: null,
            provenance: null,
            provenance_uri: null,
            status: 'Accepted',
            term: 'Drone'
          },
          id: '2',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/platformtypes/2/'
          },
          relationships: {},
          type: 'Platformtype'
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
        uri: 'platformtypes/1'
      })
      const expectedPlatformType2 = PlatformType.createFromObject({
        id: '2',
        name: 'Drone',
        uri: 'platformtypes/2'
      })

      const serializer = new PlatformTypeSerializer('http://rz-vm64.gfz-potsdam.de:5001/api')

      const platformTypes = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(platformTypes)).toBeTruthy()
      expect(platformTypes.length).toEqual(2)
      expect(platformTypes[0]).toEqual(expectedPlatformType1)
      expect(platformTypes[1]).toEqual(expectedPlatformType2)
    })
  })
})
