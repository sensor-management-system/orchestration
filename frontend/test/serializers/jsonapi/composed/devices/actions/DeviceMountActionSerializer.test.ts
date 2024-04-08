/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2021-2024
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
import { PlatformBasicData } from '@/models/basic/PlatformBasicData'
import { ContactBasicData } from '@/models/basic/ContactBasicData'
import { ConfigurationBasicData } from '@/models/basic/ConfigurationBasicData'
import { DeviceMountActionBasicData } from '@/models/basic/DeviceMountActionBasicData'
import { DeviceMountAction } from '@/models/views/devices/actions/DeviceMountAction'
import { DeviceMountActionSerializer } from '@/serializers/jsonapi/composed/devices/actions/DeviceMountActionSerializer'
import { IJsonApiEntityListEnvelope } from '@/serializers/jsonapi/JsonApiTypes'
import { DeviceBasicData } from '@/models/basic/DeviceBasicData'

describe('DeviceMountActionSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a json api payload to a device mount action list', () => {
      const jsonApiObject: IJsonApiEntityListEnvelope = {
        data: [
          {
            type: 'device_mount_action',
            id: 'dm1',
            attributes: {
              offset_x: 0,
              offset_y: 0,
              offset_z: 0,
              begin_description: 'Device mount',
              end_description: 'Device unmount',
              begin_date: '2020-01-01T12:00:00.000Z',
              end_date: '2020-02-01T12:00:00.000Z',
              epsg_code: '4326',
              x: 12.5,
              y: 51.1,
              z: 0.0,
              elevation_datum_name: 'MSL',
              elevation_datum_uri: 'http://cv/el/1'
            },
            relationships: {
              begin_contact: {
                data: {
                  type: 'contact',
                  id: 'ct1'
                }
              },
              end_contact: {
                data: {
                  type: 'contact',
                  id: 'ct2'
                }
              },
              configuration: {
                data: {
                  type: 'configuration',
                  id: 'cf1'
                }
              }
            }
          },
          {
            type: 'device_mount_action',
            id: 'dm2',
            attributes: {
              offset_x: 1,
              offset_y: 2,
              offset_z: 3,
              begin_description: 'Device mount',
              begin_date: '2020-03-01T12:00:00.000Z'
            },
            relationships: {
              begin_contact: {
                data: {
                  type: 'contact',
                  id: 'ct2'
                }
              },
              configuration: {
                data: {
                  type: 'configuration',
                  id: 'cf1'
                }
              },
              parent_platform: {
                data: {
                  type: 'platform',
                  id: 'pt1'
                }
              }
            }
          },
          {
            type: 'device_mount_action',
            id: 'dm3',
            attributes: {
              offset_x: 1,
              offset_y: 2,
              offset_z: 3,
              begin_description: 'Device mount',
              begin_date: '2020-03-01T12:00:00.000Z'
            },
            relationships: {
              begin_contact: {
                data: {
                  type: 'contact',
                  id: 'ct2'
                }
              },
              configuration: {
                data: {
                  type: 'configuration',
                  id: 'cf1'
                }
              },
              parent_device: {
                data: {
                  type: 'device',
                  id: 'dv1'
                }
              }
            }
          }
        ],
        included: [
          {
            type: 'configuration',
            id: 'cf1',
            attributes: {
              start_date: '2020-08-28T13:49:48.015620+00:00',
              end_date: '2020-08-29T13:49:48.015620+00:00',
              label: 'Tereno NO Boeken',
              description: 'Boeken station',
              project: 'Tereno NO',
              campaign: 'Demmin',
              status: 'draft',
              archived: true
            }
          },
          {
            type: 'contact',
            id: 'ct1',
            attributes: {
              given_name: 'Max',
              email: 'test@test.test',
              website: null,
              organization: null,
              orcid: null,
              family_name: 'Mustermann'
            }
          },
          {
            type: 'contact',
            id: 'ct2',
            attributes: {
              given_name: 'Mux',
              email: 'foo@bar.test',
              website: null,
              organization: 'abc',
              orcid: '0000-0000-0000-0001',
              family_name: 'Mastermann'
            }
          },
          {
            type: 'platform',
            id: 'pt1',
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
            }
          },
          {
            type: 'device',
            id: 'dv1',
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
            }
          }
        ]
      }

      const expectedPt1 = PlatformBasicData.createFromObject({
        id: 'pt1',
        serialNumber: '000123',
        model: '0815',
        description: 'Soil Moisture station Boeken_BF1',
        platformTypeUri: 'type/Station',
        statusUri: 'status/inuse',
        website: 'http://www.tereno.net',
        updatedAt: DateTime.utc(2020, 8, 28, 13, 48, 35, 740),
        longName: 'Soil moisture station Boeken BF1, Germany',
        createdAt: DateTime.utc(2020, 8, 28, 13, 48, 35, 740),
        inventoryNumber: '0001234',
        manufacturerName: 'XYZ',
        shortName: 'boeken_BF1',
        statusName: 'in use',
        platformTypeName: 'Station',
        persistentIdentifier: 'boeken_BF1',
        manufacturerUri: 'manufacturer/xyz',
        updatedByUserId: null,
        createdByUserId: null,
        archived: true
      })
      const expectedDv1 = DeviceBasicData.createFromObject({
        id: 'dv1',
        serialNumber: '000123',
        model: '0815',
        description: 'Soil Moisture station Boeken_BF1',
        deviceTypeUri: 'type/Station',
        statusUri: 'status/inuse',
        website: 'http://www.tereno.net',
        updatedAt: DateTime.utc(2020, 8, 28, 13, 48, 35, 740),
        longName: 'Soil moisture station Boeken BF1, Germany',
        createdAt: DateTime.utc(2020, 8, 28, 13, 48, 35, 740),
        inventoryNumber: '0001234',
        manufacturerName: 'XYZ',
        shortName: 'boeken_BF1',
        statusName: 'in use',
        deviceTypeName: 'Station',
        persistentIdentifier: 'boeken_BF1',
        manufacturerUri: 'manufacturer/xyz',
        updatedByUserId: null,
        createdByUserId: null,
        archived: true
      })

      const expectedCt1 = ContactBasicData.createFromObject({
        id: 'ct1',
        givenName: 'Max',
        familyName: 'Mustermann',
        website: '',
        email: 'test@test.test',
        organization: '',
        orcid: '',
        createdAt: null,
        updatedAt: null,
        createdByUserId: null
      })
      const expectedCt2 = ContactBasicData.createFromObject({
        id: 'ct2',
        givenName: 'Mux',
        familyName: 'Mastermann',
        website: '',
        email: 'foo@bar.test',
        organization: 'abc',
        orcid: '0000-0000-0000-0001',
        createdAt: null,
        updatedAt: null,
        createdByUserId: null
      })

      const expectedCf1 = ConfigurationBasicData.createFromObject({
        id: 'cf1',
        startDate: DateTime.utc(2020, 8, 28, 13, 49, 48, 15),
        endDate: DateTime.utc(2020, 8, 29, 13, 49, 48, 15),
        label: 'Tereno NO Boeken',
        description: 'Boeken station',
        project: 'Tereno NO',
        campaign: 'Demmin',
        status: 'draft',
        archived: true
      })

      const expectedDm1 = DeviceMountActionBasicData.createFromObject({
        id: 'dm1',
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        beginDate: DateTime.utc(2020, 1, 1, 12, 0, 0),
        endDate: DateTime.utc(2020, 2, 1, 12, 0, 0),
        beginDescription: 'Device mount',
        endDescription: 'Device unmount',
        epsgCode: '4326',
        x: 12.5,
        y: 51.1,
        z: 0.0,
        elevationDatumName: 'MSL',
        elevationDatumUri: 'http://cv/el/1'
      })

      const expectedDm2 = DeviceMountActionBasicData.createFromObject({
        id: 'dm2',
        offsetX: 1,
        offsetY: 2,
        offsetZ: 3,
        beginDate: DateTime.utc(2020, 3, 1, 12, 0, 0),
        beginDescription: 'Device mount',
        endDate: null,
        endDescription: '',
        epsgCode: '',
        x: null,
        y: null,
        z: null,
        elevationDatumName: '',
        elevationDatumUri: ''
      })
      const expectedDm3 = DeviceMountActionBasicData.createFromObject({
        id: 'dm3',
        offsetX: 1,
        offsetY: 2,
        offsetZ: 3,
        beginDate: DateTime.utc(2020, 3, 1, 12, 0, 0),
        beginDescription: 'Device mount',
        endDate: null,
        endDescription: '',
        epsgCode: '',
        x: null,
        y: null,
        z: null,
        elevationDatumName: '',
        elevationDatumUri: ''
      })

      const expectedResult = [
        new DeviceMountAction(
          expectedDm1, expectedCf1, expectedCt1, expectedCt2, null, null
        ),
        new DeviceMountAction(
          expectedDm2, expectedCf1, expectedCt2, null, expectedPt1, null
        ),
        new DeviceMountAction(
          expectedDm3, expectedCf1, expectedCt2, null, null, expectedDv1
        )
      ]

      const serializer = new DeviceMountActionSerializer()
      const result = serializer.convertJsonApiObjectListToModelList(jsonApiObject)

      expect(result).toEqual(expectedResult)
    })
  })
})
