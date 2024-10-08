/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2023 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'

import { TsmdlDatasource } from '@/models/TsmdlDatasource'
import { TsmdlDatastream } from '@/models/TsmdlDatastream'
import { TsmdlThing } from '@/models/TsmdlThing'
import { TsmLinking } from '@/models/TsmLinking'
import { TsmLinkingSerializer } from '@/serializers/jsonapi/TsmLinkingSerializer'
import { TsmdlEntity } from '@/models/TsmdlEntity'
import { Device } from '@/models/Device'
import { DeviceProperty } from '@/models/DeviceProperty'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Contact } from '@/models/Contact'
import { TsmEndpoint } from '@/models/TsmEndpoint'
import { TsmLinkingInvolvedDevice } from '@/models/TsmLinkingInvolvedDevice'

function withName<X extends TsmdlEntity> (arg: X, name: string) {
  arg.name = name
  return arg
}

describe('TsmLinkingSerializer', () => {
  describe('#convertJsonApiDataToModel', () => {
    it('should give back an tsm linking object', () => {
      const jsonApiData = {
        id: '123',
        type: 'datastream_link',
        attributes: {
          begin_date: '2020-01-01T00:00:00.000Z',
          end_date: '2021-01-01T00:00:00.000Z',
          datastream_id: 'stream_123',
          datastream_name: '123 stream',
          datasource_id: 'source_123',
          datasource_name: '123 source',
          thing_id: 'thing_123',
          thing_name: '123 thing',
          license_name: 'CCBY',
          license_uri: 'https://sensors.gfz-potsdam.de/cv/api/v1/licenses/1',
          aggregation_period: 180
        },
        relationships: {
          device_property: {
            data: {
              id: '1',
              type: 'device_property'
            }
          },
          device_mount_action: {
            data: {
              id: '2',
              type: 'device_mount_action'
            }
          },
          tsm_endpoint: {
            data: {
              id: '3',
              type: 'tsm_endpoint'
            }
          }
        }
      }

      const expectedResult = TsmLinking.createFromObject({
        id: '123',
        configurationId: '',
        // The relationships are set, but we don't include the entry.
        // So it stays null.
        deviceMountAction: null,
        device: null,
        deviceProperty: null,
        tsmEndpoint: null,
        datastream: withName(new TsmdlDatastream('stream_123'), '123 stream'),
        datasource: withName(new TsmdlDatasource('source_123'), '123 source'),
        thing: withName(new TsmdlThing('thing_123'), '123 thing'),
        startDate: DateTime.utc(2020, 1, 1, 0, 0, 0, 0),
        endDate: DateTime.utc(2021, 1, 1, 0, 0, 0, 0),
        licenseName: 'CCBY',
        licenseUri: 'https://sensors.gfz-potsdam.de/cv/api/v1/licenses/1',
        aggregationPeriod: 180,
        involvedDevices: []
      })
      const serializer = new TsmLinkingSerializer()
      const result = serializer.convertJsonApiDataToModel(jsonApiData, [])
      expect(result).toEqual(expectedResult)
    })
    it('should also work with way less data', () => {
      const jsonApiData = {
        id: '123',
        type: 'datastream_link',
        attributes: {
          begin_date: null,
          end_date: null,
          // xxx_id fields are not nullable
          // while name fields are.
          datastream_id: '',
          datastream_name: null,
          datasource_id: '',
          datasource_name: null,
          thing_id: '',
          thing_name: null,
          license_name: null,
          license_uri: null,
          aggregation_period: null
        },
        relationships: {
          device_property: {
            data: {
              id: '1',
              type: 'device_property'
            }
          },
          device_mount_action: {
            data: {
              id: '2',
              type: 'device_mount_action'
            }
          },
          tsm_endpoint: {
            data: {
              id: '3',
              type: 'tsm_endpoint'
            }
          }
        }
      }

      const expectedResult = TsmLinking.createFromObject({
        id: '123',
        configurationId: '',
        // The relationships are set, but we don't include the entry.
        // So it stays null.
        deviceMountAction: null,
        device: null,
        deviceProperty: null,
        tsmEndpoint: null,
        datastream: withName(new TsmdlDatastream(''), ''),
        datasource: withName(new TsmdlDatasource(''), ''),
        thing: withName(new TsmdlThing(''), ''),
        startDate: null,
        endDate: null,
        licenseName: '',
        licenseUri: '',
        aggregationPeriod: null,
        involvedDevices: []
      })
      const serializer = new TsmLinkingSerializer()
      const result = serializer.convertJsonApiDataToModel(jsonApiData, [])
      expect(result).toEqual(expectedResult)
    })
    it('should be able to include involved devices', () => {
      const jsonApiData = {
        id: '123',
        type: 'datastream_link',
        attributes: {
          begin_date: '2020-01-01T00:00:00.000Z',
          end_date: '2021-01-01T00:00:00.000Z',
          datastream_id: 'stream_123',
          datastream_name: '123 stream',
          datasource_id: 'source_123',
          datasource_name: '123 source',
          thing_id: 'thing_123',
          thing_name: '123 thing',
          license_name: 'CCBY',
          license_uri: 'https://sensors.gfz-potsdam.de/cv/api/v1/licenses/1',
          aggregation_period: 180
        },
        relationships: {
          device_property: {
            data: {
              id: '1',
              type: 'device_property'
            }
          },
          device_mount_action: {
            data: {
              id: '2',
              type: 'device_mount_action'
            }
          },
          tsm_endpoint: {
            data: {
              id: '3',
              type: 'tsm_endpoint'
            }
          },
          involved_devices: {
            data: [
              {
                id: '4',
                type: 'involved_device_for_datastream_link'
              },
              {
                id: '5',
                type: 'involved_device_for_datastream_link'
              }
            ]
          }
        }
      }
      const included = [
        {
          type: 'involved_device_for_datastream_link',
          id: '4',
          attributes: {
            order_index: 1
          },
          relationships: {
            device: {
              data: {
                id: '7',
                type: 'device'
              }
            }
          }
        },
        {
          type: 'involved_device_for_datastream_link',
          id: '5',
          attributes: {
            order_index: 2
          },
          relationships: {
            device: {
              data: {
                id: '8',
                type: 'device'
              }
            }
          }
        }
      ]

      const expectedResult = TsmLinking.createFromObject({
        id: '123',
        configurationId: '',
        // The relationships are set, but we don't include the entry.
        // So it stays null.
        deviceMountAction: null,
        device: null,
        deviceProperty: null,
        tsmEndpoint: null,
        datastream: withName(new TsmdlDatastream('stream_123'), '123 stream'),
        datasource: withName(new TsmdlDatasource('source_123'), '123 source'),
        thing: withName(new TsmdlThing('thing_123'), '123 thing'),
        startDate: DateTime.utc(2020, 1, 1, 0, 0, 0, 0),
        endDate: DateTime.utc(2021, 1, 1, 0, 0, 0, 0),
        licenseName: 'CCBY',
        licenseUri: 'https://sensors.gfz-potsdam.de/cv/api/v1/licenses/1',
        aggregationPeriod: 180,
        involvedDevices: [
          TsmLinkingInvolvedDevice.createFromObject({
            id: '4',
            orderIndex: 1,
            deviceId: '7'
          }),
          TsmLinkingInvolvedDevice.createFromObject({
            id: '5',
            orderIndex: 2,
            deviceId: '8'
          })
        ]
      })
      const serializer = new TsmLinkingSerializer()
      const result = serializer.convertJsonApiDataToModel(jsonApiData, included)
      expect(result).toEqual(expectedResult)
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should convert the data to a datastream link payload', () => {
      const device = new Device()
      device.id = '1'

      const deviceProperty = new DeviceProperty()
      deviceProperty.id = '2'

      const contact = new Contact()
      contact.id = '3'

      const deviceMountAction = new DeviceMountAction(
        '4',
        device,
        null,
        null,
        DateTime.utc(2020, 1, 1, 0, 0, 0, 0),
        DateTime.utc(2021, 1, 1, 0, 0, 0, 0),
        0,
        0,
        0,
        '',
        null,
        null,
        null,
        '',
        '',
        contact,
        contact,
        '',
        '',
        ''
      )
      const tsmEndpoint = new TsmEndpoint()
      tsmEndpoint.id = '5'

      const tsmLinking = TsmLinking.createFromObject({
        id: '6',
        configurationId: '',
        // The relationships are set, but we don't include the entry.
        // So it stays null.
        deviceMountAction,
        device,
        deviceProperty,
        tsmEndpoint,
        datastream: withName(new TsmdlDatastream('stream_123'), '123 stream'),
        datasource: withName(new TsmdlDatasource('source_123'), '123 source'),
        thing: withName(new TsmdlThing('thing_123'), '123 thing'),
        startDate: DateTime.utc(2020, 1, 1, 0, 0, 0, 0),
        endDate: DateTime.utc(2021, 1, 1, 0, 0, 0, 0),
        licenseName: 'CCBY',
        licenseUri: 'https://sensors.gfz-potsdam.de/cv/api/v1/licenses/1',
        aggregationPeriod: 180,
        involvedDevices: []
      })

      const expectedResult = {
        id: '6',
        type: 'datastream_link',
        attributes: {
          begin_date: '2020-01-01T00:00:00.000Z',
          end_date: '2021-01-01T00:00:00.000Z',
          datasource_id: 'source_123',
          datasource_name: '123 source',
          thing_id: 'thing_123',
          thing_name: '123 thing',
          datastream_id: 'stream_123',
          datastream_name: '123 stream',
          license_name: 'CCBY',
          license_uri: 'https://sensors.gfz-potsdam.de/cv/api/v1/licenses/1',
          aggregation_period: 180
        },
        relationships: {
          device_mount_action: {
            data: {
              id: '4',
              type: 'device_mount_action'
            }
          },
          device_property: {
            data: {
              id: '2',
              type: 'device_property'
            }
          },
          tsm_endpoint: {
            data: {
              id: '5',
              type: 'tsm_endpoint'
            }
          }
        }
      }

      const serializer = new TsmLinkingSerializer()
      const result = serializer.convertModelToJsonApiData(tsmLinking)

      expect(result).toEqual(expectedResult)
    })
    it('should also work with a minimal set of data', () => {
      const device = new Device()
      device.id = '1'

      const deviceProperty = new DeviceProperty()
      deviceProperty.id = '2'

      const contact = new Contact()
      contact.id = '3'

      const deviceMountAction = new DeviceMountAction(
        '4',
        device,
        null,
        null,
        DateTime.utc(2020, 1, 1, 0, 0, 0, 0),
        DateTime.utc(2021, 1, 1, 0, 0, 0, 0),
        0,
        0,
        0,
        '',
        null,
        null,
        null,
        '',
        '',
        contact,
        contact,
        '',
        '',
        ''
      )
      const tsmEndpoint = new TsmEndpoint()
      tsmEndpoint.id = '5'

      const tsmLinking = TsmLinking.createFromObject({
        id: '6',
        configurationId: '',
        // The relationships are set, but we don't include the entry.
        // So it stays null.
        deviceMountAction,
        device,
        deviceProperty,
        tsmEndpoint,
        datastream: withName(new TsmdlDatastream(''), ''),
        datasource: withName(new TsmdlDatasource(''), ''),
        thing: withName(new TsmdlThing(''), ''),
        startDate: null,
        endDate: null,
        licenseName: '',
        licenseUri: '',
        aggregationPeriod: null,
        involvedDevices: []
      })

      const expectedResult = {
        id: '6',
        type: 'datastream_link',
        attributes: {
          begin_date: null,
          end_date: null,
          datasource_id: '',
          datasource_name: '',
          thing_id: '',
          thing_name: '',
          datastream_id: '',
          datastream_name: '',
          license_name: '',
          license_uri: '',
          aggregation_period: null
        },
        relationships: {
          device_mount_action: {
            data: {
              id: '4',
              type: 'device_mount_action'
            }
          },
          device_property: {
            data: {
              id: '2',
              type: 'device_property'
            }
          },
          tsm_endpoint: {
            data: {
              id: '5',
              type: 'tsm_endpoint'
            }
          }
        }
      }

      const serializer = new TsmLinkingSerializer()
      const result = serializer.convertModelToJsonApiData(tsmLinking)

      expect(result).toEqual(expectedResult)
    })
  })
})
