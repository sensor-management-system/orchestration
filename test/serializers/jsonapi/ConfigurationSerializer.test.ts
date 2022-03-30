/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2021
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

import { Configuration } from '@/models/Configuration'
import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { DeviceUnmountAction } from '@/models/DeviceUnmountAction'
import { Platform } from '@/models/Platform'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { PlatformUnmountAction } from '@/models/PlatformUnmountAction'
import { StationaryLocation, DynamicLocation, LocationType } from '@/models/Location'

import {
  IJsonApiEntityWithoutDetailsDataDict,
  IJsonApiEntityWithoutDetailsDataDictList
} from '@/serializers/jsonapi/JsonApiTypes'

import {
  ConfigurationSerializer,
  IConfigurationWithMeta,
  configurationWithMetaToConfigurationByThrowingErrorOnMissing,
  configurationWithMetaToConfigurationByAddingDummyObjects
} from '@/serializers/jsonapi/ConfigurationSerializer'

import { DeviceProperty } from '@/models/DeviceProperty'
import { MeasuringRange } from '@/models/MeasuringRange'
import { DynamicLocationBeginAction } from '@/models/DynamicLocationBeginAction'
import { DynamicLocationEndAction } from '@/models/DynamicLocationEndAction'

import { StaticLocationBeginAction } from '@/models/StaticLocationBeginAction'
import { StaticLocationEndAction } from '@/models/StaticLocationEndAction'

describe('LocationType', () => {
  it('should be fixed what values can be given - and those should be consistent with the serializer', () => {
    expect(LocationType.Stationary).toEqual('Stationary')
    expect(LocationType.Dynamic).toEqual('Dynamic')
  })
})
describe('ConfigurationSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a json api object with multiple entries to a configuration model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          type: 'configuration',
          attributes: {
            start_date: '2020-08-28T13:49:48.015620+00:00',
            end_date: '2020-08-29T13:49:48.015620+00:00',
            location_type: LocationType.Dynamic,
            project_uri: 'projects/Tereno-NO',
            project_name: 'Tereno NO',
            label: 'Tereno NO Boeken',
            status: 'draft'
          },
          relationships: {
            src_longitude: {
              data: {
                type: 'device_property',
                id: '100'
              }
            },
            src_latitude: {
              data: {
                type: 'device_property',
                id: '101'
              }
            },
            src_elevation: {
            },
            platform_mount_actions: {
              data: [
                {
                  type: 'platform_mount_action',
                  id: '1'
                },
                {
                  type: 'platform_mount_action',
                  id: '2'
                },
                {
                  type: 'platform_mount_action',
                  id: '3'
                }
              ]
            },
            platform_unmount_actions: {
              data: [
                {
                  type: 'platform_unmount_action',
                  id: '1'
                }
              ]
            },
            device_mount_actions: {
              data: [
                {
                  type: 'device_mount_action',
                  id: '1'
                },
                {
                  type: 'device_mount_action',
                  id: '2'
                }
              ]
            },
            device_unmount_actions: {
              data: [
                {
                  type: 'device_unmount_action',
                  id: '1'
                }
              ]
            },
            configuration_static_location_begin_actions: {
              data: [
                {
                  type: 'configuration_static_location_begin_action',
                  id: '1111'
                }
              ]
            },
            configuration_static_location_end_actions: {
              data: [
                {
                  type: 'configuration_static_location_end_action',
                  id: '2222'
                }
              ]
            },
            configuration_dynamic_location_begin_actions: {
              data: [
                {
                  type: 'configuration_dynamic_location_end_action',
                  id: '3333'
                }
              ]
            },
            configuration_dynamic_location_end_actions: {
              data: [
                {
                  type: 'configuration_dynamic_location_end_action',
                  id: '4444'
                }
              ]
            }
            // no contacts, as we expect an empty case here
          },
          id: '1'
        }, {
          type: 'configuration',
          attributes: {
            // no start and no end date
            location_type: LocationType.Dynamic,
            // no fields for longitude, latitude & elevation,
            // no fields for project_uri or project_name
            // no field for label
            status: 'draft'
          },
          relationships: {
            // no contacts, as we expect an empty case here
            // and handle device properties somehow
          },
          id: '2'
        }, {
          type: 'configuration',
          attributes: {},
          relationships: {},
          id: '3'
        }, {
          type: 'configuration',
          attributes: {
            location_type: LocationType.Stationary,
            longitude: 13.0,
            latitude: 52.0,
            elevation: 100.0
          },
          relationships: {},
          id: '4'
        }],
        included: [{
          type: 'platform_mount_action',
          id: '1',
          attributes: {
            offset_x: 1.0,
            offset_y: 2.0,
            offset_z: 3.0,
            description: '',
            begin_date: '2020-01-01T13:49:48.000000+00:00'
          },
          relationships: {
            platform: {
              data: {
                type: 'platform',
                id: '37'
              }
            },
            contact: {
              data: {
                type: 'contact',
                id: '1'
              }
            },
            configuration: {
              data: {
                type: 'configuration',
                id: '1'
              }
            }
          }
        },
        {
          type: 'platform_mount_action',
          id: '2',
          attributes: {
            offset_x: 4.0,
            offset_y: 5.0,
            offset_z: 6.0,
            description: '',
            begin_date: '2020-01-01T14:49:48.000000+00:00'
          },
          relationships: {
            platform: {
              data: {
                type: 'platform',
                id: '38'
              }
            },
            parent_platform: {
              data: {
                type: 'platform',
                id: '37'
              }
            },
            contact: {
              data: {
                type: 'contact',
                id: '1'
              }
            },
            configuration: {
              data: {
                type: 'configuration',
                id: '1'
              }
            }
          }
        },
        {
          type: 'platform_mount_action',
          id: '3',
          attributes: {
            offset_x: 13.0,
            offset_y: 14.0,
            offset_z: 15.0,
            description: 'mount',
            begin_date: '2020-01-01T15:49:48.000000+00:00'
          },
          relationships: {
            platform: {
              data: {
                type: 'platform',
                id: '41'
              }
            },
            contact: {
              data: {
                type: 'contact',
                id: '1'
              }
            },
            configuration: {
              data: {
                type: 'configuration',
                id: '1'
              }
            }
          }
        },
        {
          type: 'platform_unmount_action',
          id: '1',
          attributes: {
            end_date: '2021-01-01T15:49:48.000000+00:00',
            description: 'unmount'
          },
          relationships: {
            platform: {
              data: {
                type: 'platform',
                id: '41'
              }
            },
            contact: {
              data: {
                type: 'contact',
                id: '1'
              }
            },
            configuration: {
              data: {
                type: 'configuration',
                id: '1'
              }
            }
          }
        },
        {
          type: 'device_mount_action',
          id: '1',
          attributes: {
            offset_x: 7.0,
            offset_y: 8.0,
            offset_z: 9.0,
            description: '',
            begin_date: '2020-01-01T16:49:48.000000+00:00'
          },
          relationships: {
            device: {
              data: {
                type: 'device',
                id: '39'
              }
            },
            parent_platform: {
              data: {
                type: 'platform',
                id: '38'
              }
            },
            contact: {
              data: {
                type: 'contact',
                id: '1'
              }
            },
            configuration: {
              data: {
                type: 'configuration',
                id: '1'
              }
            }
          }
        },
        {
          type: 'device_mount_action',
          id: '2',
          attributes: {
            offset_x: 10.0,
            offset_y: 11.0,
            offset_z: 12.0,
            description: 'device mount',
            begin_date: '2020-01-01T17:49:48.000000+00:00'
          },
          relationships: {
            device: {
              data: {
                type: 'device',
                id: '40'
              }
            },
            parent_platform: {
              data: {
                type: 'platform',
                id: '38'
              }
            },
            contact: {
              data: {
                type: 'contact',
                id: '1'
              }
            },
            configuration: {
              data: {
                type: 'configuration',
                id: '1'
              }
            }
          }
        },
        {
          type: 'device_unmount_action',
          id: '1',
          attributes: {
            description: 'device unmount',
            end_date: '2021-01-01T17:49:48.000000+00:00'
          },
          relationships: {
            device: {
              data: {
                type: 'device',
                id: '40'
              }
            },
            contact: {
              data: {
                type: 'contact',
                id: '1'
              }
            },
            configuration: {
              data: {
                type: 'configuration',
                id: '1'
              }
            }
          }
        },
        {
          type: 'configuration_static_location_begin_action',
          id: '1111',
          attributes: {
            description: 'start static action',
            x: 1.0,
            y: 2.0,
            z: 3.0,
            epsg_code: '4326',
            elevation_datum_name: 'MSL',
            elevation_datum_uri: 'some/uri',
            begin_date: '2021-01-01T17:49:48.000000+00:00'
          },
          relationships: {
            contact: {
              data: {
                type: 'contact',
                id: '1'
              }
            },
            configuration: {
              data: {
                type: 'configuration',
                id: '1'
              }
            }
          }
        },
        {
          type: 'configuration_static_location_end_action',
          id: '2222',
          attributes: {
            description: 'stop static action',
            end_date: '2021-01-02T17:49:48.000000+00:00'
          },
          relationships: {
            contact: {
              data: {
                type: 'contact',
                id: '1'
              }
            },
            configuration: {
              data: {
                type: 'configuration',
                id: '1'
              }
            }
          }
        },
        {
          type: 'configuration_dynamic_location_begin_action',
          id: '3333',
          attributes: {
            description: 'start static action',
            epsg_code: '4326',
            elevation_datum_name: 'MSL',
            elevation_datum_uri: 'some/uri',
            begin_date: '2021-01-03T17:49:48.000000+00:00'
          },
          relationships: {
            contact: {
              data: {
                type: 'contact',
                id: '1'
              }
            },
            configuration: {
              data: {
                type: 'configuration',
                id: '1'
              }
            },
            x_property: {
              data: {
                type: 'device_property',
                id: '100'
              }
            },
            y_property: {
              data: {
                type: 'device_property',
                id: '101'
              }
            },
            z_property: {
              data: {
                type: 'device_property',
                id: null
              }
            }
          }
        },
        {
          type: 'configuration_dynamic_location_end_action',
          id: '4444',
          attributes: {
            description: 'stop dynamic action',
            end_date: '2021-01-04T17:49:48.000000+00:00'
          },
          relationships: {
            contact: {
              data: {
                type: 'contact',
                id: '1'
              }
            },
            configuration: {
              data: {
                type: 'configuration',
                id: '1'
              }
            }
          }
        },
        {
          type: 'device_property',
          id: '100',
          attributes: {
            sampling_media_name: 'Air',
            sampling_media_uri: 'medium/air',
            compartment_name: 'C1',
            compartment_uri: 'compartment/c1',
            property_name: 'Temperature',
            property_uri: 'property/temperature',
            unit_name: 'degree',
            unit_uri: 'unit/degree',
            failure_value: -999,
            measuring_range_min: -273,
            measuring_range_max: 100,
            label: 'air_temperature',
            accuracy: 0.1,
            resolution: 0.05,
            resolution_unit_name: 'TemperatureRes',
            resolution_unit_uri: 'property/res/temperature'
          },
          relationships: {
            device: {
              data: {
                type: 'device',
                // just an example device included already for the
                // mount actions
                id: '39'
              }
            }
          }
        },
        {
          type: 'device_property',
          id: '101',
          attributes: {
            sampling_media_name: 'Water',
            sampling_media_uri: 'medium/water',
            compartment_name: 'C1',
            compartment_uri: 'compartment/c1',
            property_name: 'Temperature',
            property_uri: 'property/temperature',
            unit_name: 'degree',
            unit_uri: 'unit/degree',
            failure_value: -999,
            measuring_range_min: -10,
            measuring_range_max: 100,
            label: 'water_temperature',
            accuracy: 0.1,
            resolution: 0.05,
            resolution_unit_name: 'TemperatureRes',
            resolution_unit_uri: 'property/res/temperature'
          },
          relationships: {
            device: {
              data: {
                type: 'device',
                // just an example device included already for the
                // mount actions
                id: '39'
              }
            }
          }
        },
        {
          type: 'contact',
          id: '1',
          attributes: {
            given_name: 'Max',
            family_name: 'Mustermann',
            email: 'max@mustermann.xyz',
            website: ''
          }
        },
        {
          type: 'platform',
          id: '37',
          attributes: {
            inventory_number: '',
            platform_type_uri: 'type/station',
            short_name: 'boeken_BF1',
            created_at: '2020-08-28T13:48:35.740944+00:00',
            manufacturer_name: '',
            description: 'Boeken BF1',
            updated_at: '2020-08-29T13:48:35.740944+00:00',
            long_name: 'Boeken BF1',
            manufacturer_uri: '',
            platform_type_name: 'Station',
            serial_number: '',
            persistent_identifier: null,
            model: '',
            website: '',
            status_uri: '',
            status_name: ''
          },
          relationships: {
            // nothing more to make the test case not too complex
          }
        },
        {
          type: 'platform',
          id: '38',
          attributes: {
            inventory_number: '',
            platform_type_uri: 'type/station',
            short_name: 'boeken_BF12',
            created_at: '2020-09-28T13:48:35.740944+00:00',
            manufacturer_name: '',
            description: 'Boeken BF2',
            updated_at: '2020-09-29T13:48:35.740944+00:00',
            long_name: 'Boeken BF2',
            manufacturer_uri: '',
            platform_type_name: 'Station',
            serial_number: '',
            persistent_identifier: null,
            model: '',
            website: '',
            status_uri: '',
            status_name: ''
          },
          relationships: {
            // nothing more to make the test case not too complex
          }
        },
        {
          type: 'platform',
          id: '41',
          attributes: {
            inventory_number: '',
            platform_type_uri: 'type/station',
            short_name: 'boeken_BF123',
            created_at: '2020-09-29T13:48:35.740944+00:00',
            manufacturer_name: '',
            description: 'Boeken BF3',
            updated_at: '2020-09-30T13:48:35.740944+00:00',
            long_name: 'Boeken BF3',
            manufacturer_uri: '',
            platform_type_name: 'Station',
            serial_number: '',
            persistent_identifier: null,
            model: '',
            website: '',
            status_uri: '',
            status_name: ''
          }
        }, {
          type: 'device',
          id: '39',
          attributes: {
            inventory_number: '',
            short_name: 'Adcon wind vane',
            device_type_uri: '',
            created_at: '2020-08-28T13:49:48.799090+00:00',
            manufacturer_name: 'OTT Hydromet GmbH',
            dual_use: false,
            description: '',
            device_type_name: '',
            updated_at: '2020-08-29T13:49:48.799090+00:00',
            manufacturer_uri: '',
            long_name: 'Adcon wind vane',
            serial_number: '',
            persistent_identifier: null,
            model: 'Wind Vane',
            website: 'www.adcon.com',
            status_uri: '',
            status_name: ''
          },
          relationships: {
            // nothing more to make the test case not too complex
          }
        }, {
          type: 'device',
          id: '40',
          attributes: {
            inventory_number: '',
            short_name: 'Adcon leafwetness',
            device_type_uri: '',
            created_at: '2020-08-29T13:49:48.799090+00:00',
            manufacturer_name: 'OTT Hydromet GmbH',
            dual_use: false,
            description: '',
            device_type_name: '',
            updated_at: '2020-09-29T13:49:48.799090+00:00',
            manufacturer_uri: '',
            long_name: 'Adcon leafwetness',
            serial_number: '',
            persistent_identifier: null,
            model: 'Leaf Wetness',
            website: 'http://www.adcon.com',
            status_uri: '',
            status_name: ''
          },
          relationships: {
            // nothing more to make the test case not too complex
          }
        }],
        meta: {
          count: 2
        },
        jsonapi: {
          version: '1.0'
        }
      }

      const expectedPlatform1 = Platform.createFromObject({
        id: '37',
        inventoryNumber: '',
        platformTypeUri: 'type/station',
        shortName: 'boeken_BF1',
        createdAt: DateTime.utc(
          2020, 8, 28, 13, 48, 35, 740 // no sub milliseconds
        ),
        manufacturerName: '',
        attachments: [],
        description: 'Boeken BF1',
        updatedAt: DateTime.utc(
          2020, 8, 29, 13, 48, 35, 740),
        longName: 'Boeken BF1',
        manufacturerUri: '',
        platformTypeName: 'Station',
        serialNumber: '',
        persistentIdentifier: '',
        model: '',
        website: '',
        statusUri: '',
        statusName: '',
        contacts: [],
        createdByUserId: null,
        updatedByUserId: null
      })
      const expectedPlatform2 = Platform.createFromObject({
        id: '38',
        inventoryNumber: '',
        platformTypeUri: 'type/station',
        shortName: 'boeken_BF12',
        createdAt: DateTime.utc(2020, 9, 28, 13, 48, 35, 740),
        manufacturerName: '',
        attachments: [],
        description: 'Boeken BF2',
        updatedAt: DateTime.utc(2020, 9, 29, 13, 48, 35, 740),
        longName: 'Boeken BF2',
        manufacturerUri: '',
        platformTypeName: 'Station',
        serialNumber: '',
        persistentIdentifier: '',
        model: '',
        website: '',
        statusUri: '',
        statusName: '',
        contacts: [],
        createdByUserId: null,
        updatedByUserId: null
      })
      const expectedPlatform3 = Platform.createFromObject({
        id: '41',
        inventoryNumber: '',
        platformTypeUri: 'type/station',
        shortName: 'boeken_BF123',
        createdAt: DateTime.utc(2020, 9, 29, 13, 48, 35, 740),
        manufacturerName: '',
        attachments: [],
        description: 'Boeken BF3',
        updatedAt: DateTime.utc(2020, 9, 30, 13, 48, 35, 740),
        longName: 'Boeken BF3',
        manufacturerUri: '',
        platformTypeName: 'Station',
        serialNumber: '',
        persistentIdentifier: '',
        model: '',
        website: '',
        statusUri: '',
        statusName: '',
        contacts: [],
        createdByUserId: null,
        updatedByUserId: null
      })

      const property1 = DeviceProperty.createFromObject({
        id: '100',
        samplingMediaName: 'Air',
        samplingMediaUri: 'medium/air',
        compartmentName: 'C1',
        compartmentUri: 'compartment/c1',
        propertyName: 'Temperature',
        propertyUri: 'property/temperature',
        unitName: 'degree',
        unitUri: 'unit/degree',
        failureValue: -999,
        measuringRange: MeasuringRange.createFromObject({
          min: -273,
          max: 100
        }),
        label: 'air_temperature',
        accuracy: 0.1,
        resolution: 0.05,
        resolutionUnitName: 'TemperatureRes',
        resolutionUnitUri: 'property/res/temperature'
      })
      const property2 = DeviceProperty.createFromObject({
        id: '101',
        samplingMediaName: 'Water',
        samplingMediaUri: 'medium/water',
        compartmentName: 'C1',
        compartmentUri: 'compartment/c1',
        propertyName: 'Temperature',
        propertyUri: 'property/temperature',
        unitName: 'degree',
        unitUri: 'unit/degree',
        failureValue: -999,
        measuringRange: MeasuringRange.createFromObject({
          min: -10,
          max: 100
        }),
        label: 'water_temperature',
        accuracy: 0.1,
        resolution: 0.05,
        resolutionUnitName: 'TemperatureRes',
        resolutionUnitUri: 'property/res/temperature'
      })

      const expectedDevice1 = Device.createFromObject({
        id: '39',
        properties: [property1, property2],
        inventoryNumber: '',
        shortName: 'Adcon wind vane',
        customFields: [],
        deviceTypeUri: '',
        createdAt: DateTime.utc(2020, 8, 28, 13, 49, 48, 799),
        manufacturerName: 'OTT Hydromet GmbH',
        attachments: [],
        dualUse: false,
        description: '',
        deviceTypeName: '',
        updatedAt: DateTime.utc(2020, 8, 29, 13, 49, 48, 799),
        manufacturerUri: '',
        longName: 'Adcon wind vane',
        serialNumber: '',
        persistentIdentifier: '',
        model: 'Wind Vane',
        website: 'www.adcon.com',
        statusUri: '',
        statusName: '',
        contacts: [],
        createdByUserId: null,
        updatedByUserId: null
      })
      const expectedDevice2 = Device.createFromObject({
        id: '40',
        properties: [],
        inventoryNumber: '',
        shortName: 'Adcon leafwetness',
        customFields: [],
        deviceTypeUri: '',
        createdAt: DateTime.utc(2020, 8, 29, 13, 49, 48, 799),
        manufacturerName: 'OTT Hydromet GmbH',
        attachments: [],
        dualUse: false,
        description: '',
        deviceTypeName: '',
        updatedAt: DateTime.utc(2020, 9, 29, 13, 49, 48, 799),
        manufacturerUri: '',
        longName: 'Adcon leafwetness',
        serialNumber: '',
        persistentIdentifier: '',
        model: 'Leaf Wetness',
        website: 'http://www.adcon.com',
        statusUri: '',
        statusName: '',
        contacts: [],
        createdByUserId: null,
        updatedByUserId: null
      })

      const expectedContact = new Contact()
      expectedContact.id = '1'
      expectedContact.givenName = 'Max'
      expectedContact.familyName = 'Mustermann'
      expectedContact.email = 'max@mustermann.xyz'
      expectedContact.website = ''

      const expectedPlatformMountAction1 = PlatformMountAction.createFromObject({
        id: '1',
        offsetX: 1.0,
        offsetY: 2.0,
        offsetZ: 3.0,
        description: '',
        platform: expectedPlatform1,
        parentPlatform: null,
        contact: expectedContact,
        date: DateTime.utc(2020, 1, 1, 13, 49, 48)
      })

      const expectedPlatformMountAction2 = PlatformMountAction.createFromObject({
        id: '2',
        offsetX: 4.0,
        offsetY: 5.0,
        offsetZ: 6.0,
        description: '',
        platform: expectedPlatform2,
        parentPlatform: expectedPlatform1,
        contact: expectedContact,
        date: DateTime.utc(2020, 1, 1, 14, 49, 48)
      })

      const expectedPlatformMountAction3 = PlatformMountAction.createFromObject({
        id: '3',
        offsetX: 13.0,
        offsetY: 14.0,
        offsetZ: 15.0,
        description: 'mount',
        platform: expectedPlatform3,
        parentPlatform: null,
        contact: expectedContact,
        date: DateTime.utc(2020, 1, 1, 15, 49, 48)
      })

      const expectedPlatformUnmountAction1 = PlatformUnmountAction.createFromObject({
        id: '1',
        platform: expectedPlatform3,
        contact: expectedContact,
        description: 'unmount',
        date: DateTime.utc(2021, 1, 1, 15, 49, 48)
      })

      const expectedDeviceMountAction1 = DeviceMountAction.createFromObject({
        id: '1',
        offsetX: 7.0,
        offsetY: 8.0,
        offsetZ: 9.0,
        description: '',
        device: expectedDevice1,
        parentPlatform: expectedPlatform2,
        contact: expectedContact,
        date: DateTime.utc(2020, 1, 1, 16, 49, 48)
      })

      const expectedDeviceMountAction2 = DeviceMountAction.createFromObject({
        id: '2',
        offsetX: 10.0,
        offsetY: 11.0,
        offsetZ: 12.0,
        description: 'device mount',
        device: expectedDevice2,
        parentPlatform: expectedPlatform2,
        contact: expectedContact,
        date: DateTime.utc(2020, 1, 1, 17, 49, 48)
      })

      const expectedDeviceUnmountAction1 = DeviceUnmountAction.createFromObject({
        id: '1',
        device: expectedDevice2,
        date: DateTime.utc(2021, 1, 1, 17, 49, 48),
        description: 'device unmount',
        contact: expectedContact
      })

      const expectedStaticLocationBeginAction1 = StaticLocationBeginAction.createFromObject({
        id: '1111',
        beginDate: DateTime.utc(2021, 1, 1, 17, 49, 48),
        description: 'start static action',
        epsgCode: '4326',
        elevationDatumName: 'MSL',
        elevationDatumUri: 'some/uri',
        contact: expectedContact,
        x: 1.0,
        y: 2.0,
        z: 3.0
      })

      const expectedStaticLocationEndAction1 = StaticLocationEndAction.createFromObject({
        id: '2222',
        endDate: DateTime.utc(2021, 1, 2, 17, 49, 48),
        description: 'stop static action',
        contact: expectedContact
      })

      const expectedDynamicLocationBeginAction1 = DynamicLocationBeginAction.createFromObject({
        id: '3333',
        beginDate: DateTime.utc(2021, 1, 3, 17, 49, 48),
        description: 'start static action',
        epsgCode: '4326',
        elevationDatumName: 'MSL',
        elevationDatumUri: 'some/uri',
        contact: expectedContact,
        x: property1,
        y: property2,
        z: null
      })

      const expectedDynamicLocationEndAction1 = DynamicLocationEndAction.createFromObject({
        id: '4444',
        endDate: DateTime.utc(2021, 1, 4, 17, 49, 48),
        description: 'stop dynamic action',
        contact: expectedContact
      })

      const expectedConfiguration1 = new Configuration()
      expectedConfiguration1.id = '1'
      expectedConfiguration1.location = DynamicLocation.createFromObject({
        longitude: property1,
        latitude: property2,
        elevation: null
      })
      expectedConfiguration1.startDate = DateTime.utc(2020, 8, 28, 13, 49, 48, 15)
      expectedConfiguration1.endDate = DateTime.utc(2020, 8, 29, 13, 49, 48, 15)
      expectedConfiguration1.projectUri = 'projects/Tereno-NO'
      expectedConfiguration1.projectName = 'Tereno NO'
      expectedConfiguration1.label = 'Tereno NO Boeken'
      expectedConfiguration1.status = 'draft'
      expectedConfiguration1.platformMountActions = [
        expectedPlatformMountAction1,
        expectedPlatformMountAction2,
        expectedPlatformMountAction3
      ]
      expectedConfiguration1.platformUnmountActions = [expectedPlatformUnmountAction1]
      expectedConfiguration1.deviceMountActions = [
        expectedDeviceMountAction1,
        expectedDeviceMountAction2
      ]
      expectedConfiguration1.deviceUnmountActions = [expectedDeviceUnmountAction1]
      expectedConfiguration1.staticLocationBeginActions = [expectedStaticLocationBeginAction1]
      expectedConfiguration1.staticLocationEndActions = [expectedStaticLocationEndAction1]
      expectedConfiguration1.dynamicLocationBeginActions = [expectedDynamicLocationBeginAction1]
      expectedConfiguration1.dynamicLocationEndActions = [expectedDynamicLocationEndAction1]

      const expectedConfiguration2 = new Configuration()
      expectedConfiguration2.id = '2'
      expectedConfiguration2.location = new DynamicLocation()
      expectedConfiguration2.status = 'draft'

      const expectedConfiguration3 = new Configuration()
      expectedConfiguration3.id = '3'

      const expectedConfiguration4 = new Configuration()
      expectedConfiguration4.id = '4'
      expectedConfiguration4.location = StationaryLocation.createFromObject({
        longitude: 13.0,
        latitude: 52.0,
        elevation: 100.0
      })

      const serializer = new ConfigurationSerializer()
      const configurationsWithMeta = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)
      const configurations = configurationsWithMeta.map((x: IConfigurationWithMeta) => {
        return x.configuration
      })

      expect(Array.isArray(configurations)).toBeTruthy()
      expect(configurations.length).toEqual(4)

      expect(configurations[0]).toEqual(expectedConfiguration1)
      expect(configurations[0].deviceMountActions.length).toEqual(2)
      expect(configurations[0].platformMountActions.length).toEqual(3)
      expect(configurations[0].deviceUnmountActions.length).toEqual(1)
      expect(configurations[0].platformUnmountActions.length).toEqual(1)
      expect(configurations[1]).toEqual(expectedConfiguration2)
      expect(configurations[1].deviceMountActions.length).toEqual(0)
      expect(configurations[1].platformMountActions.length).toEqual(0)
      expect(configurations[1].deviceUnmountActions.length).toEqual(0)
      expect(configurations[1].platformUnmountActions.length).toEqual(0)
      expect(configurations[2]).toEqual(expectedConfiguration3)
      expect(configurations[3]).toEqual(expectedConfiguration4)

      const missingContactIds = configurationsWithMeta.map((x: IConfigurationWithMeta) => {
        return x.missing.contacts.ids
      })

      expect(Array.isArray(missingContactIds)).toBeTruthy()
      expect(missingContactIds.length).toEqual(4)
      expect(missingContactIds[0]).toEqual([])
      expect(missingContactIds[1]).toEqual([])
      expect(missingContactIds[2]).toEqual([])
      expect(missingContactIds[3]).toEqual([])
    })
  })
  describe('#convertJsonApiObjectToModel', () => {
    it('should convert a json api object to a configuration model', () => {
      const jsonApiObject: any = {
        data: {
          type: 'configuration',
          attributes: {
            start_date: '2020-08-28T13:49:48.015620+00:00',
            end_date: '2020-08-29T13:49:48.015620+00:00',
            location_type: LocationType.Stationary,
            longitude: 13.0,
            latitude: 52.0,
            elevation: 100.0,
            project_uri: 'projects/Tereno-NO',
            project_name: 'Tereno NO',
            label: 'Tereno NO Boeken',
            status: 'draft'
          },
          relationships: {
            // no contacts, as we expect an empty case here
          },
          id: '1'
        },
        jsonapi: {
          version: '1.0'
        }
      }
      const expectedConfiguration = new Configuration()
      expectedConfiguration.id = '1'
      expectedConfiguration.location = StationaryLocation.createFromObject({
        longitude: 13.0,
        latitude: 52.0,
        elevation: 100.0
      })
      expectedConfiguration.startDate = DateTime.utc(2020, 8, 28, 13, 49, 48, 15)
      expectedConfiguration.endDate = DateTime.utc(2020, 8, 29, 13, 49, 48, 15)
      expectedConfiguration.projectUri = 'projects/Tereno-NO'
      expectedConfiguration.projectName = 'Tereno NO'
      expectedConfiguration.label = 'Tereno NO Boeken'
      expectedConfiguration.status = 'draft'

      const serializer = new ConfigurationSerializer()
      const configurationWithMeta = serializer.convertJsonApiObjectToModel(jsonApiObject)
      const configuration = configurationWithMeta.configuration

      expect(configuration).toEqual(expectedConfiguration)
      expect(configurationWithMeta.missing.contacts.ids).toEqual([])
    })
    it('should also convert a configuration with information for contacts', () => {
      const jsonApiObject: any = {
        data: {
          type: 'configuration',
          attributes: {
            start_date: '2020-08-28T13:49:48.015620+00:00',
            end_date: '2020-08-29T13:49:48.015620+00:00',
            location_type: LocationType.Stationary,
            longitude: 13.0,
            latitude: 52.0,
            elevation: 100.0,
            project_uri: 'projects/Tereno-NO',
            project_name: 'Tereno NO',
            label: 'Tereno NO Boeken',
            status: 'draft'
          },
          relationships: {
            contacts: {
              data: [{
                type: 'contact',
                id: '1'
              }, {
                type: 'contact',
                id: '2'
              }]
            }
          },
          id: '1'
        },
        included: [{
          type: 'contact',
          attributes: {
            given_name: 'Max',
            email: 'test@test.test',
            website: null,
            family_name: 'Mustermann'
          },
          id: '1'
        }, {
          type: 'contact',
          attributes: {
            given_name: 'Mux',
            email: 'test@tost.test',
            website: null,
            family_name: 'Mastermann'
          },
          id: '2'
        }],
        jsonapi: {
          version: '1.0'
        }
      }
      const expectedConfiguration = new Configuration()
      expectedConfiguration.id = '1'
      expectedConfiguration.location = StationaryLocation.createFromObject({
        longitude: 13.0,
        latitude: 52.0,
        elevation: 100.0
      })
      expectedConfiguration.startDate = DateTime.utc(2020, 8, 28, 13, 49, 48, 15)
      expectedConfiguration.endDate = DateTime.utc(2020, 8, 29, 13, 49, 48, 15)
      expectedConfiguration.projectUri = 'projects/Tereno-NO'
      expectedConfiguration.projectName = 'Tereno NO'
      expectedConfiguration.label = 'Tereno NO Boeken'
      expectedConfiguration.status = 'draft'
      expectedConfiguration.contacts = [
        Contact.createFromObject({
          id: '1',
          givenName: 'Max',
          familyName: 'Mustermann',
          website: '',
          email: 'test@test.test'
        }),
        Contact.createFromObject({
          id: '2',
          givenName: 'Mux',
          familyName: 'Mastermann',
          website: '',
          email: 'test@tost.test'
        })
      ]

      const serializer = new ConfigurationSerializer()
      const configurationWithMeta = serializer.convertJsonApiObjectToModel(jsonApiObject)
      const configuration = configurationWithMeta.configuration

      expect(configuration).toEqual(expectedConfiguration)
      expect(configurationWithMeta.missing.contacts.ids).toEqual([])
    })
  })
  describe('#convertJsonApiDataToModel', () => {
    it('should convert a json api data to a configuration model', () => {
      const jsonApiData: any = {
        attributes: {
          start_date: '2020-08-28T13:49:48.015620+00:00',
          end_date: '2020-08-29T13:49:48.015620+00:00',
          location_type: LocationType.Stationary,
          longitude: 13.0,
          latitude: 52.0,
          elevation: 100.0,
          project_uri: 'projects/Tereno-NO',
          project_name: 'Tereno NO',
          label: 'Tereno NO Boeken',
          status: 'draft'
        },
        relationships: {
          contacts: {
            data: [] // no contacts in this case
          }
        },
        id: '1'
      }

      const expectedConfiguration = new Configuration()
      expectedConfiguration.id = '1'
      expectedConfiguration.location = StationaryLocation.createFromObject({
        longitude: 13.0,
        latitude: 52.0,
        elevation: 100.0
      })
      expectedConfiguration.startDate = DateTime.utc(2020, 8, 28, 13, 49, 48, 15)
      expectedConfiguration.endDate = DateTime.utc(2020, 8, 29, 13, 49, 48, 15)
      expectedConfiguration.projectUri = 'projects/Tereno-NO'
      expectedConfiguration.projectName = 'Tereno NO'
      expectedConfiguration.label = 'Tereno NO Boeken'
      expectedConfiguration.status = 'draft'

      const included: any[] = []

      const serializer = new ConfigurationSerializer()
      const configurationWithMeta = serializer.convertJsonApiDataToModel(jsonApiData, included)
      const configuration = configurationWithMeta.configuration

      expect(configuration).toEqual(expectedConfiguration)
      expect(configurationWithMeta.missing.contacts.ids).toEqual([])
    })
    it('should convert a json api data to a configuration model without lat&lon', () => {
      const jsonApiData: any = {
        attributes: {
          start_date: '2020-08-28T13:49:48.015620+00:00',
          end_date: '2020-08-29T13:49:48.015620+00:00',
          location_type: LocationType.Stationary,
          longitude: null,
          latitude: null,
          elevation: null,
          project_uri: 'projects/Tereno-NO',
          project_name: 'Tereno NO',
          label: 'Tereno NO Boeken',
          status: 'draft'
        },
        relationships: {
          contacts: {
            data: [] // no contacts in this case
          }
        },
        id: '1'
      }

      const expectedConfiguration = new Configuration()
      expectedConfiguration.id = '1'
      expectedConfiguration.location = new StationaryLocation()
      expectedConfiguration.startDate = DateTime.utc(2020, 8, 28, 13, 49, 48, 15)
      expectedConfiguration.endDate = DateTime.utc(2020, 8, 29, 13, 49, 48, 15)
      expectedConfiguration.projectUri = 'projects/Tereno-NO'
      expectedConfiguration.projectName = 'Tereno NO'
      expectedConfiguration.label = 'Tereno NO Boeken'
      expectedConfiguration.status = 'draft'

      const included: any[] = []

      const serializer = new ConfigurationSerializer()
      const configurationWithMeta = serializer.convertJsonApiDataToModel(jsonApiData, included)
      const configuration = configurationWithMeta.configuration

      expect(configuration).toEqual(expectedConfiguration)
      expect(configurationWithMeta.missing.contacts.ids).toEqual([])
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should convert a model to json data object', () => {
      const configuration = new Configuration()
      expect(configuration.id).toEqual('')
      configuration.label = 'ABC'
      configuration.projectUri = 'projects/tereno-no'
      configuration.projectName = 'TERENO NO'
      configuration.location = StationaryLocation.createFromObject({
        longitude: 12.0,
        latitude: 51.0,
        elevation: 60.0
      })
      configuration.startDate = DateTime.utc(2020, 8, 28, 13, 49, 48, 15)
      configuration.endDate = DateTime.utc(2021, 8, 28, 13, 49, 48, 15)
      configuration.contacts = [
        Contact.createFromObject({
          id: '1',
          givenName: 'Max',
          familyName: 'Mustermann',
          website: '',
          email: 'test@test.test'
        }),
        Contact.createFromObject({
          id: '2',
          givenName: 'Mux',
          familyName: 'Mastermann',
          website: '',
          email: 'test@fost.test'
        })
      ]
      const serializer = new ConfigurationSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(configuration)

      expect(typeof jsonApiData).toEqual('object')

      expect(jsonApiData).not.toHaveProperty('id')
      expect(jsonApiData.type).toEqual('configuration')
      expect(jsonApiData).toHaveProperty('attributes')
      const attributes = jsonApiData.attributes

      expect(attributes).toHaveProperty('label')
      expect(attributes.label).toEqual('ABC')
      expect(attributes).toHaveProperty('project_uri')
      expect(attributes.project_uri).toEqual('projects/tereno-no')
      expect(attributes).toHaveProperty('project_name')
      expect(attributes.project_name).toEqual('TERENO NO')
      expect(attributes).toHaveProperty('location_type')
      expect(attributes.location_type).toEqual(LocationType.Stationary)
      expect(attributes).toHaveProperty('longitude')
      expect(attributes.longitude).toEqual(12.0)
      expect(attributes).toHaveProperty('latitude')
      expect(attributes.latitude).toEqual(51.0)
      expect(attributes).toHaveProperty('elevation')
      expect(attributes.elevation).toEqual(60.0)
      expect(attributes).toHaveProperty('start_date')
      expect(attributes.start_date).toEqual('2020-08-28T13:49:48.015Z')
      expect(attributes).toHaveProperty('end_date')
      expect(attributes.end_date).toEqual('2021-08-28T13:49:48.015Z')

      expect(jsonApiData).toHaveProperty('relationships')
      expect(typeof jsonApiData.relationships).toEqual('object')
      expect(jsonApiData.relationships).toHaveProperty('contacts')
      expect(typeof jsonApiData.relationships?.contacts).toEqual('object')
      expect(jsonApiData.relationships?.contacts).toHaveProperty('data')

      // we test for the inner structure of the result anyway
      // this cast is just to tell typescript that
      // we have an array of data, so that it doesn't show
      // typeerrors here
      const contactObject = jsonApiData.relationships?.contacts as IJsonApiEntityWithoutDetailsDataDictList

      const contactData = contactObject.data
      expect(Array.isArray(contactData)).toBeTruthy()
      expect(contactData.length).toEqual(2)
      expect(contactData[0]).toEqual({
        id: '1',
        type: 'contact'
      })
      expect(contactData[1]).toEqual({
        id: '2',
        type: 'contact'
      })
    })
    it('should set an id if given for the configuration', () => {
      const configuration = new Configuration()
      configuration.id = '1'
      const serializer = new ConfigurationSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(configuration)

      expect(jsonApiData).toHaveProperty('id')
      expect(jsonApiData.id).toEqual('1')
    })
    it('should also work with a dynamic location type', () => {
      const configuration = new Configuration()
      expect(configuration.id).toEqual('')

      const property1 = DeviceProperty.createFromObject({
        id: '100',
        samplingMediaName: 'Air',
        samplingMediaUri: 'medium/air',
        compartmentName: 'C1',
        compartmentUri: 'compartment/c1',
        propertyName: 'Temperature',
        propertyUri: 'property/temperature',
        unitName: 'degree',
        unitUri: 'unit/degree',
        failureValue: -999,
        measuringRange: MeasuringRange.createFromObject({
          min: -273,
          max: 100
        }),
        label: 'air_temperature',
        accuracy: 0.1,
        resolution: 0.05,
        resolutionUnitName: 'TemperatureRes',
        resolutionUnitUri: 'property/res/temperature'
      })
      const property2 = DeviceProperty.createFromObject({
        id: '101',
        samplingMediaName: 'Water',
        samplingMediaUri: 'medium/water',
        compartmentName: 'C1',
        compartmentUri: 'compartment/c1',
        propertyName: 'Temperature',
        propertyUri: 'property/temperature',
        unitName: 'degree',
        unitUri: 'unit/degree',
        failureValue: -999,
        measuringRange: MeasuringRange.createFromObject({
          min: -10,
          max: 100
        }),
        label: 'water_temperature',
        accuracy: 0.1,
        resolution: 0.05,
        resolutionUnitName: 'TemperatureRes',
        resolutionUnitUri: 'property/res/temperature'
      })

      configuration.location = new DynamicLocation()
      configuration.location.latitude = property1
      configuration.location.longitude = property2
      configuration.location.elevation = null

      const serializer = new ConfigurationSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(configuration)

      expect(typeof jsonApiData).toEqual('object')

      expect(jsonApiData).not.toHaveProperty('id')
      expect(jsonApiData.type).toEqual('configuration')
      expect(jsonApiData).toHaveProperty('attributes')
      const attributes = jsonApiData.attributes

      expect(attributes).toHaveProperty('location_type')
      expect(attributes.location_type).toEqual(LocationType.Dynamic)
      expect(jsonApiData).toHaveProperty('relationships')
      const relationships = jsonApiData.relationships
      expect(relationships).toHaveProperty('src_longitude')
      const lonSrcProperty = relationships?.src_longitude as IJsonApiEntityWithoutDetailsDataDict
      expect(lonSrcProperty).toHaveProperty('data')
      expect(lonSrcProperty.data).toHaveProperty('id')
      expect(lonSrcProperty.data.id).toEqual('101')
      expect(lonSrcProperty.data).toHaveProperty('type')
      expect(lonSrcProperty.data.type).toEqual('device_property')
      expect(relationships).toHaveProperty('src_latitude')
      const latSrcProperty = relationships?.src_latitude as IJsonApiEntityWithoutDetailsDataDict
      expect(latSrcProperty).toHaveProperty('data')
      expect(latSrcProperty.data).toHaveProperty('id')
      expect(latSrcProperty.data.id).toEqual('100')
      expect(latSrcProperty.data).toHaveProperty('type')
      expect(latSrcProperty.data.type).toEqual('device_property')
      // TODO check how it must look like to delete them later...
      expect(relationships).not.toHaveProperty('src_elevation')
    })
    it('should also work with an empty stationary location type', () => {
      const configuration = new Configuration()
      expect(configuration.id).toEqual('')
      configuration.location = new StationaryLocation()

      const serializer = new ConfigurationSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(configuration)

      expect(typeof jsonApiData).toEqual('object')

      expect(jsonApiData).not.toHaveProperty('id')
      expect(jsonApiData.type).toEqual('configuration')
      expect(jsonApiData).toHaveProperty('attributes')
      const attributes = jsonApiData.attributes

      expect(attributes).toHaveProperty('location_type')
      expect(attributes.location_type).toEqual(LocationType.Stationary)
      expect(attributes).toHaveProperty('longitude')
      expect(attributes.longitude).toEqual(null)
      expect(attributes).toHaveProperty('latitude')
      expect(attributes.latitude).toEqual(null)
      expect(attributes).toHaveProperty('elevation')
      expect(attributes.elevation).toEqual(null)
    })
  })
  // in earlier versions, the test to serialize the configuration hierarchy
  // was here. As we don't handle a single hierarchy anymore, but the
  // the list of mpunt & unmount actions it is no longer representative.
  // (And the actions themselves are handled as entities of the JSON:API
  // on their own, so there is really no point in checking them for the
  // serializer).
})
describe('configurationWithMetaToConfigurationByThrowingErrorOnMissing', () => {
  it('should work without missing data', () => {
    const configuration = new Configuration()
    const missing = {
      contacts: {
        ids: []
      }
    }

    const result = configurationWithMetaToConfigurationByThrowingErrorOnMissing({
      configuration,
      missing
    })

    expect(result).toEqual(configuration)
    expect(result.contacts).toEqual([])
  })
  it('should also work if there is an contact', () => {
    const configuration = new Configuration()
    const contact = Contact.createFromObject({
      id: '1',
      familyName: 'Mustermann',
      givenName: 'Max',
      website: '',
      email: 'max@mustermann.de'
    })
    configuration.contacts.push(contact)

    const missing = {
      contacts: {
        ids: []
      }
    }
    const result = configurationWithMetaToConfigurationByThrowingErrorOnMissing({
      configuration,
      missing
    })

    expect(result).toEqual(configuration)
    expect(result.contacts).toEqual([contact])
  })
  it('should throw an error if there are missing data', () => {
    const configuration = new Configuration()
    const missing = {
      contacts: {
        ids: ['1']
      }
    }

    try {
      configurationWithMetaToConfigurationByThrowingErrorOnMissing({
        configuration,
        missing
      })
      fail('There must be an error')
    } catch (error: any) {
      expect(error.toString()).toMatch(/Contacts are missing/)
    }
  })
})
describe('configurationWithMetaToConfigurationByAddingDummyObjects', () => {
  it('should leave the data as it is if there are no missing data', () => {
    const configuration = new Configuration()
    const missing = {
      contacts: {
        ids: []
      }
    }

    const result = configurationWithMetaToConfigurationByAddingDummyObjects({
      configuration,
      missing
    })

    expect(result).toEqual(configuration)
    expect(result.contacts).toEqual([])
  })
  it('should stay with existing contacts without adding dummy data', () => {
    const configuration = new Configuration()
    const contact = Contact.createFromObject({
      id: '1',
      familyName: 'Mustermann',
      givenName: 'Max',
      website: '',
      email: 'max@mustermann.de'
    })
    configuration.contacts.push(contact)
    const missing = {
      contacts: {
        ids: []
      }
    }

    const result = configurationWithMetaToConfigurationByAddingDummyObjects({
      configuration,
      missing
    })

    expect(result).toEqual(configuration)
    expect(result.contacts).toEqual([contact])
  })
  it('should add a dummy contact', () => {
    const configuration = new Configuration()
    const contact = Contact.createFromObject({
      id: '1',
      familyName: 'Mustermann',
      givenName: 'Max',
      website: '',
      email: 'max@mustermann.de'
    })
    configuration.contacts.push(contact)
    const missing = {
      contacts: {
        ids: ['2']
      }
    }

    const newExpectedContact = new Contact()
    newExpectedContact.id = '2'

    const result = configurationWithMetaToConfigurationByAddingDummyObjects({
      configuration,
      missing
    })

    expect(result).toEqual(configuration)
    expect(result.contacts).toEqual([contact, newExpectedContact])
  })
})
