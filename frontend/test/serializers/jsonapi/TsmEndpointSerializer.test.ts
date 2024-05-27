/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { TsmEndpointSerializer } from '@/serializers/jsonapi/TsmEndpointSerializer'
import { TsmEndpoint } from '@/models/TsmEndpoint'

describe('TsmEndpointSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a json api object with multiple entries to a tsmEndpoint model list', () => {
      const jsonApiObjectList: any = {
        data: [
          {
            type: 'tsm_endpoint',
            attributes: {
              name: 'UFZ',
              url: 'https://ufz.de/tsmendpoint'
            },
            id: '1',
            links: {
              self: '/backend/api/v1/tsm-endpoints/1'
            }
          },
          {
            type: 'tsm_endpoint',
            attributes: {
              name: 'Test',
              url: 'https://test.de/tsmdl'
            },
            id: '2',
            links: {
              self: '/backend/api/v1/tsm-endpoints/2'
            }
          }
        ],
        links: {
          self: 'https://localhost.localdomain/backend/api/v1/tsm-endpoints'
        },
        meta: {
          count: 2
        },
        jsonapi: {
          version: '1.0'
        }
      }

      const expectedTsmEndpoint1 = new TsmEndpoint()
      const expectedTsmEndpoint2 = new TsmEndpoint()

      expectedTsmEndpoint1.id = '1'
      expectedTsmEndpoint1.url = 'https://ufz.de/tsmendpoint'
      expectedTsmEndpoint1.name = 'UFZ'

      expectedTsmEndpoint2.id = '2'
      expectedTsmEndpoint2.url = 'https://test.de/tsmdl'
      expectedTsmEndpoint2.name = 'Test'

      const serializer = new TsmEndpointSerializer()
      const tsmEndpoints = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(tsmEndpoints)).toBeTruthy()
      expect(tsmEndpoints.length).toEqual(2)
      expect(tsmEndpoints[0]).toEqual(expectedTsmEndpoint1)
      expect(tsmEndpoints[1]).toEqual(expectedTsmEndpoint2)
    })
  })
  describe('#convertJsonApiEntityToModel', () => {
    it('should convert a single json api object to a contact model', () => {
      const jsonApiObject: any = {
        type: 'tsm_endpoint',
        attributes: {
          name: 'Test',
          url: 'https://test.de/tsmdl'
        },
        id: '2',
        links: {
          self: '/backend/api/v1/tsm-endpoints/2'
        }
      }

      const expectedTsmEndpoint = new TsmEndpoint()
      expectedTsmEndpoint.id = '2'
      expectedTsmEndpoint.url = 'https://test.de/tsmdl'
      expectedTsmEndpoint.name = 'Test'

      const serializer = new TsmEndpointSerializer()
      const tsmEndpoint = serializer.convertJsonApiEntityToModel(jsonApiObject)

      expect(tsmEndpoint).toEqual(expectedTsmEndpoint)
    })
  })
})
