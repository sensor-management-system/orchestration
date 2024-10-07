/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { TsmLinkingInvolvedDevice } from '@/models/TsmLinkingInvolvedDevice'
import { TsmLinkingInvolvedDeviceSerializer } from '@/serializers/jsonapi/TsmLinkingInvolvedDeviceSerializer'

describe('TsmLinkingInvolvedDeviceSerializer', () => {
  describe('#convertJsonApiDataToModel', () => {
    it('should give back an involved device object', () => {
      const jsonApiData = {
        id: '123',
        type: 'involved_device_for_datastream_link',
        attributes: {
          order_index: 456
        },
        relationships: {
          device: {
            data: {
              id: '1',
              type: 'device'
            }
          }
        }
      }

      const expectedResult = TsmLinkingInvolvedDevice.createFromObject({
        id: '123',
        orderIndex: 456,
        deviceId: '1'
      })
      const serializer = new TsmLinkingInvolvedDeviceSerializer()
      const result = serializer.convertJsonApiDataToModel(jsonApiData)
      expect(result).toEqual(expectedResult)
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should convert the data to an involved device payload', () => {
      const model = TsmLinkingInvolvedDevice.createFromObject({
        id: '1',
        orderIndex: 2,
        deviceId: '3'
      })
      const datastreamLinkId = '4'

      const expectedResult = {
        id: '1',
        type: 'involved_device_for_datastream_link',
        attributes: {
          order_index: 2
        },
        relationships: {
          device: {
            data: {
              id: '3',
              type: 'device'
            }
          },
          datastream_link: {
            data: {
              id: '4',
              type: 'datastream_link'
            }
          }
        }
      }

      const serializer = new TsmLinkingInvolvedDeviceSerializer()
      const result = serializer.convertModelToJsonApiData(model, datastreamLinkId)

      expect(result).toEqual(expectedResult)
    })
  })
})
