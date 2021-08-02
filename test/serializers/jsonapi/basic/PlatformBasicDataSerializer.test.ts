/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
 * - Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 * (UFZ, https://www.ufz.de)
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
          manufacturer_uri: 'manufacturer/xyz'
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

      const serializer = new PlatformBasicDataSerializer()
      const platform = serializer.convertJsonApiDataToModel(jsonApiData)

      expect(platform).toEqual(expectedPlatform)
    })
  })
})
