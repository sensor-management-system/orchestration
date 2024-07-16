/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2021 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'

import { PlatformMountActionBasicData } from '@/models/basic/PlatformMountActionBasicData'

import { PlatformMountActionBasicDataSerializer } from '@/serializers/jsonapi/basic/PlatformMountActionBasicDataSerializer'

const beginDate = DateTime.utc(2020, 1, 1, 12, 0, 0)
const endDate = DateTime.utc(2020, 2, 1, 12, 0, 0)

describe('PlatformMountActionBasicDataSerializer', () => {
  describe('#convertJsonApiDataToModel', () => {
    it('should covnert a single json api data object to a platform mount action', () => {
      const jsonApiData: any = {
        type: 'platform_mount_action',
        attributes: {
          offset_x: 0,
          offset_y: 0,
          offset_z: 0,
          begin_description: 'Platform mount',
          begin_date: '2020-01-01T12:00:00.000Z',
          end_description: 'Platform unmount',
          end_date: '2020-02-01T12:00:00.000Z',
          epsg_code: '4326',
          x: 12.5,
          y: 51.1,
          z: 0.0,
          elevation_datum_name: 'MSL',
          elevation_datum_uri: 'http://cv/el/1',
          label: 'Mount'
        },
        id: '1'
      }

      const expectePlatformMountAction = PlatformMountActionBasicData.createFromObject({
        id: '1',
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        beginDate,
        endDate,
        beginDescription: 'Platform mount',
        endDescription: 'Platform unmount',
        epsgCode: '4326',
        x: 12.5,
        y: 51.1,
        z: 0.0,
        elevationDatumName: 'MSL',
        elevationDatumUri: 'http://cv/el/1',
        label: 'Mount'
      })

      const serializer = new PlatformMountActionBasicDataSerializer()
      const platformMountAction = serializer.convertJsonApiDataToModel(jsonApiData)

      expect(platformMountAction).toEqual(expectePlatformMountAction)
    })
  })
})
