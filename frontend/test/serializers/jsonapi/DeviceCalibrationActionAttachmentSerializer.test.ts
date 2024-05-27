/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2021 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { Attachment } from '@/models/Attachment'
import { IJsonApiEntityWithOptionalId } from '@/serializers/jsonapi/JsonApiTypes'
import { DeviceCalibrationActionAttachmentSerializer } from '@/serializers/jsonapi/DeviceCalibrationActionAttachmentSerializer'

describe('DeviceCalibrationActionAttachmentSerializer', () => {
  describe('#convertModelToJsonApiData', () => {
    it('should return a JSON API object from an attachment and an action id', () => {
      const attachment = Attachment.createFromObject({
        id: '1',
        label: 'foo',
        url: 'https://bar.baz',
        description: 'The foo',
        isUpload: false,
        createdAt: null
      })
      const actionId = '2'

      const expectedApiModel: IJsonApiEntityWithOptionalId = {
        type: 'device_calibration_attachment',
        attributes: {},
        relationships: {
          action: {
            data: {
              type: 'device_calibration_action',
              id: '2'
            }
          },
          attachment: {
            data: {
              type: 'device_attachment',
              id: '1'
            }
          }
        }
      }

      const serializer = new DeviceCalibrationActionAttachmentSerializer()
      const apiModel = serializer.convertModelToJsonApiData(attachment, actionId)

      expect(apiModel).toEqual(expectedApiModel)
    })
  })
})
