/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Kotyba Alhaj Taha <kotyba.alhaj-taha@ufz.de>
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'
import { PlatformBasicData } from '@/models/basic/PlatformBasicData'

import { PlatformBasicDataSerializer } from '@/serializers/jsonapi/basic/PlatformBasicDataSerializer'

describe('PlatformBasicDataSerializer', () => {
  describe('#convertJsonApiDataToModel', () => {
    it('should convert a json api data to a platform model', () => {
      const jsonApiData: any = {
        type: 'platform',
        attributes: {
          serial_number: '000123',
          model: '0815',
          description: 'Soil Moisture station Boeken_BF1',
          platform_type_uri: 'type/Station',
          status_uri: 'status/inuse',
          website: 'http://www.tereno.net',
          updated_at: '2020-08-28T13:48:35.740944+00:00',
          long_name: 'Soil moisture station Boeken BF1, Germany',
          created_at: '2020-08-28T13:48:35.740944+00:00',
          inventory_number: '0001234',
          manufacturer_name: 'XYZ',
          short_name: 'boeken_BF1',
          status_name: 'in use',
          platform_type_name: 'Station',
          persistent_identifier: 'boeken_BF1',
          manufacturer_uri: 'manufacturer/xyz',
          archived: true
        },
        id: '37'
      }
      const expectedPlatform = new PlatformBasicData()
      expectedPlatform.id = '37'
      expectedPlatform.serialNumber = '000123'
      expectedPlatform.model = '0815'
      expectedPlatform.description = 'Soil Moisture station Boeken_BF1'

      expectedPlatform.platformTypeUri = 'type/Station'
      expectedPlatform.statusUri = 'status/inuse'
      expectedPlatform.website = 'http://www.tereno.net'
      expectedPlatform.updatedAt = DateTime.utc(2020, 8, 28, 13, 48, 35, 740)
      expectedPlatform.longName = 'Soil moisture station Boeken BF1, Germany'
      expectedPlatform.createdAt = DateTime.utc(2020, 8, 28, 13, 48, 35, 740)
      expectedPlatform.inventoryNumber = '0001234'
      expectedPlatform.manufacturerName = 'XYZ'
      expectedPlatform.shortName = 'boeken_BF1'
      expectedPlatform.statusName = 'in use'
      expectedPlatform.platformTypeName = 'Station'
      expectedPlatform.persistentIdentifier = 'boeken_BF1'
      expectedPlatform.manufacturerUri = 'manufacturer/xyz'
      expectedPlatform.archived = true

      const serializer = new PlatformBasicDataSerializer()
      const platform = serializer.convertJsonApiDataToModel(jsonApiData)

      expect(platform).toEqual(expectedPlatform)
    })
  })
})
