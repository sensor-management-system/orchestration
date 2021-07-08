/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2021
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

import { Attachment } from '@/models/Attachment'
import { IJsonApiEntityWithOptionalId } from '@/serializers/jsonapi/JsonApiTypes'
import { DeviceCalibrationActionAttachmentSerializer } from '@/serializers/jsonapi/DeviceCalibrationActionAttachmentSerializer'

describe('DeviceCalibrationActionAttachmentSerializer', () => {
  describe('#convertModelToJsonApiData', () => {
    it('should return a JSON API object from an attachment and an action id', () => {
      const attachment = Attachment.createFromObject({
        id: '1',
        label: 'foo',
        url: 'https://bar.baz'
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
