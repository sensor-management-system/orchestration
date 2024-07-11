/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2023 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'
import { DeviceBasicData } from '@/models/basic/DeviceBasicData'

import { DeviceBasicDataSerializer } from '@/serializers/jsonapi/basic/DeviceBasicDataSerializer'

describe('DeviceBasicDataSerializer', () => {
  describe('#convertJsonApiDataToModel', () => {
    it('should convert a json api data to a device model', () => {
      const jsonApiData: any = {
        type: 'device',
        attributes: {
          serial_number: '000123',
          model: '0815',
          description: 'Soil Moisture station Boeken_BF1',
          device_type_uri: 'type/Station',
          status_uri: 'status/inuse',
          website: 'http://www.tereno.net',
          updated_at: '2020-08-28T13:48:35.740944+00:00',
          long_name: 'Soil moisture station Boeken BF1, Germany',
          created_at: '2020-08-28T13:48:35.740944+00:00',
          inventory_number: '0001234',
          manufacturer_name: 'XYZ',
          short_name: 'boeken_BF1',
          status_name: 'in use',
          device_type_name: 'Station',
          persistent_identifier: 'boeken_BF1',
          manufacturer_uri: 'manufacturer/xyz',
          archived: true
        },
        id: '37'
      }
      const expectedDevice = new DeviceBasicData()
      expectedDevice.id = '37'
      expectedDevice.serialNumber = '000123'
      expectedDevice.model = '0815'
      expectedDevice.description = 'Soil Moisture station Boeken_BF1'

      expectedDevice.deviceTypeUri = 'type/Station'
      expectedDevice.statusUri = 'status/inuse'
      expectedDevice.website = 'http://www.tereno.net'
      expectedDevice.updatedAt = DateTime.utc(2020, 8, 28, 13, 48, 35, 740)
      expectedDevice.longName = 'Soil moisture station Boeken BF1, Germany'
      expectedDevice.createdAt = DateTime.utc(2020, 8, 28, 13, 48, 35, 740)
      expectedDevice.inventoryNumber = '0001234'
      expectedDevice.manufacturerName = 'XYZ'
      expectedDevice.shortName = 'boeken_BF1'
      expectedDevice.statusName = 'in use'
      expectedDevice.deviceTypeName = 'Station'
      expectedDevice.persistentIdentifier = 'boeken_BF1'
      expectedDevice.manufacturerUri = 'manufacturer/xyz'
      expectedDevice.archived = true

      const serializer = new DeviceBasicDataSerializer()
      const device = serializer.convertJsonApiDataToModel(jsonApiData)

      expect(device).toEqual(expectedDevice)
    })
  })
})
