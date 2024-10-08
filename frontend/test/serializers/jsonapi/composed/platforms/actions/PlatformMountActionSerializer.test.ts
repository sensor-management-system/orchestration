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
import { PlatformBasicData } from '@/models/basic/PlatformBasicData'
import { ContactBasicData } from '@/models/basic/ContactBasicData'
import { ConfigurationBasicData } from '@/models/basic/ConfigurationBasicData'
import { PlatformMountActionBasicData } from '@/models/basic/PlatformMountActionBasicData'
import { PlatformMountAction } from '@/models/views/platforms/actions/PlatformMountAction'
import { PlatformMountActionSerializer } from '@/serializers/jsonapi/composed/platforms/actions/PlatformMountActionSerializer'
import { IJsonApiEntityListEnvelope } from '@/serializers/jsonapi/JsonApiTypes'

describe('PlatformMountActionSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a json api payload to a platform mount action list', () => {
      const jsonApiObject: IJsonApiEntityListEnvelope = {
        data: [
          {
            type: 'platform_mount_action',
            id: 'pm1',
            attributes: {
              offset_x: 0,
              offset_y: 0,
              offset_z: 0,
              begin_description: 'Platform mount',
              end_description: 'Platform unmount',
              begin_date: '2020-01-01T12:00:00.000Z',
              end_date: '2020-02-01T12:00:00.000Z',
              epsg_code: '4326',
              x: 12.5,
              y: 51.1,
              z: 0.0,
              elevation_datum_name: 'MSL',
              elevation_datum_uri: 'http://cv/el/1',
              label: 'Mount'
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
            type: 'platform_mount_action',
            id: 'pm2',
            attributes: {
              offset_x: 1,
              offset_y: 2,
              offset_z: 3,
              begin_description: 'Platform mount',
              begin_date: '2020-03-01T12:00:00.000Z',
              label: ''
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
              organization: 'xyz',
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
        organization: 'xyz',
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

      const expectedPm1 = PlatformMountActionBasicData.createFromObject({
        id: 'pm1',
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        beginDate: DateTime.utc(2020, 1, 1, 12, 0, 0),
        endDate: DateTime.utc(2020, 2, 1, 12, 0, 0),
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

      const expectedPm2 = PlatformMountActionBasicData.createFromObject({
        id: 'pm2',
        offsetX: 1,
        offsetY: 2,
        offsetZ: 3,
        beginDate: DateTime.utc(2020, 3, 1, 12, 0, 0),
        beginDescription: 'Platform mount',
        endDate: null,
        endDescription: '',
        epsgCode: '',
        x: null,
        y: null,
        z: null,
        elevationDatumName: '',
        elevationDatumUri: '',
        label: ''
      })

      const expectedResult = [
        new PlatformMountAction(
          expectedPm1, expectedCf1, expectedCt1, expectedCt2, null
        ),
        new PlatformMountAction(
          expectedPm2, expectedCf1, expectedCt2, null, expectedPt1
        )
      ]

      const serializer = new PlatformMountActionSerializer()
      const result = serializer.convertJsonApiObjectListToModelList(jsonApiObject)

      expect(result).toEqual(expectedResult)
    })
  })
})
