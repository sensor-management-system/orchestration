/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { SoftwareType } from '@/models/SoftwareType'
import { SoftwareTypeSerializer } from '@/serializers/jsonapi/SoftwareTypeSerializer'

describe('SoftwareTypeSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            term: 'Software',
            definition: '',
            provenance: null,
            provenance_uri: null,
            category: null,
            note: null,
            status: 'ACCEPTED'
          },
          id: '1',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/softwaretypes/1/'
          },
          relationships: {},
          type: 'SoftwareType'
        }, {
          attributes: {
            term: 'Firmware',
            definition: '',
            provenance: null,
            provenance_uri: null,
            category: null,
            note: null,
            status: 'ACCEPTED'
          },
          id: '2',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/softwaretypes/2/'
          },
          relationships: {},
          type: 'SoftwareType'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedSoftwareType1 = SoftwareType.createFromObject({
        id: '1',
        name: 'Software',
        definition: '',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/softwaretypes/1/'
      })
      const expectedSoftwareType2 = SoftwareType.createFromObject({
        id: '2',
        name: 'Firmware',
        definition: '',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/softwaretypes/2/'
      })

      const serializer = new SoftwareTypeSerializer()

      const softwaretypes = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(softwaretypes)).toBeTruthy()
      expect(softwaretypes.length).toEqual(2)
      expect(softwaretypes[0]).toEqual(expectedSoftwareType1)
      expect(softwaretypes[1]).toEqual(expectedSoftwareType2)
    })
  })
})
