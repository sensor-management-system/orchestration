/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2021-2022
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

import { DateTime } from 'luxon'

import { DeviceMountActionBasicData } from '@/models/basic/DeviceMountActionBasicData'

import { DeviceMountActionBasicDataSerializer } from '@/serializers/jsonapi/basic/DeviceMountActionBasicDataSerializer'

const beginDate = DateTime.utc(2020, 1, 1, 12, 0, 0)
const endDate = DateTime.utc(2020, 2, 1, 12, 0, 0)

describe('DeviceMountActionBasicDataSerializer', () => {
  describe('#convertJsonApiDataToModel', () => {
    it('should covnert a single json api data object to a device mount action', () => {
      const jsonApiData: any = {
        type: 'device_mount_action',
        attributes: {
          offset_x: 0,
          offset_y: 0,
          offset_z: 0,
          begin_description: 'Device mount',
          begin_date: '2020-01-01T12:00:00.000Z',
          end_description: 'Device unmount',
          end_date: '2020-02-01T12:00:00.000Z'
        },
        id: '1'
      }

      const expectedDeviceMountAction = DeviceMountActionBasicData.createFromObject({
        id: '1',
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        beginDate,
        endDate,
        beginDescription: 'Device mount',
        endDescription: 'Device unmount'
      })

      const serializer = new DeviceMountActionBasicDataSerializer()
      const deviceMountAction = serializer.convertJsonApiDataToModel(jsonApiData)

      expect(deviceMountAction).toEqual(expectedDeviceMountAction)
    })
  })
})
