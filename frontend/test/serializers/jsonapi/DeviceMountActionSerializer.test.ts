/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2021 - 2024
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

import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Platform } from '@/models/Platform'

import { DeviceMountActionSerializer } from '@/serializers/jsonapi/DeviceMountActionSerializer'
import { IJsonApiEntityListEnvelope } from '@/serializers/jsonapi/JsonApiTypes'

describe('DeviceMountActionSerializer', () => {
  describe('#convertModelToJsonApiData', () => {
    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.de'

    const device = new Device()
    device.id = '2'
    device.shortName = 'device'

    const configurationId = '3'

    let deviceMountAction: DeviceMountAction

    beforeEach(() => {
      const device1 = new Device()
      device1.id = '2'
      device1.shortName = 'Device 1'

      deviceMountAction = DeviceMountAction.createFromObject({
        id: '',
        device: device1,
        parentPlatform: null,
        parentDevice: null,
        beginDate: DateTime.utc(2020, 1, 1),
        endDate: null,
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        epsgCode: '',
        x: null,
        y: null,
        z: null,
        elevationDatumName: '',
        elevationDatumUri: '',
        beginContact: contact,
        endContact: null,
        beginDescription: 'Device mount',
        endDescription: ''
      })
    })

    it('should work if the deviceMountAction has no id', () => {
      const serializer = new DeviceMountActionSerializer()

      const output = serializer.convertModelToJsonApiData(configurationId, deviceMountAction)

      const expectedOutput = {
        type: 'device_mount_action',
        attributes: {
          offset_x: 0,
          offset_y: 0,
          offset_z: 0,
          begin_description: 'Device mount',
          end_description: '',
          begin_date: '2020-01-01T00:00:00.000Z',
          end_date: null,
          epsg_code: '',
          x: null,
          y: null,
          z: null,
          elevation_datum_name: '',
          elevation_datum_uri: ''
        },
        relationships: {
          device: {
            data: {
              type: 'device',
              id: '2'
            }
          },
          begin_contact: {
            data: {
              type: 'contact',
              id: '1'
            }
          },
          configuration: {
            data: {
              type: 'configuration',
              id: '3'
            }
          }
        }
      }
      expect(output).toEqual(expectedOutput)
    })
    it('should work if the deviceMountAction has no id and a parent platform', () => {
      const parentPlatform = new Platform()
      parentPlatform.id = '4'

      const deviceMountAction = DeviceMountAction.createFromObject({
        id: '',
        device,
        parentPlatform,
        parentDevice: null,
        beginDate: DateTime.utc(2020, 1, 1),
        endDate: null,
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        epsgCode: 'epsg:4326',
        x: 12.5,
        y: 52.1,
        z: 0.0,
        elevationDatumName: 'MSL',
        elevationDatumUri: 'http://cv/el/1',
        beginContact: contact,
        endContact: null,
        beginDescription: 'Device mount',
        endDescription: ''
      })

      const serializer = new DeviceMountActionSerializer()

      const output = serializer.convertModelToJsonApiData(configurationId, deviceMountAction)

      const expectedOutput = {
        type: 'device_mount_action',
        attributes: {
          offset_x: 0,
          offset_y: 0,
          offset_z: 0,
          begin_description: 'Device mount',
          end_description: '',
          begin_date: '2020-01-01T00:00:00.000Z',
          end_date: null,
          epsg_code: 'epsg:4326',
          x: 12.5,
          y: 52.1,
          z: 0.0,
          elevation_datum_name: 'MSL',
          elevation_datum_uri: 'http://cv/el/1'
        },
        relationships: {
          device: {
            data: {
              type: 'device',
              id: '2'
            }
          },
          begin_contact: {
            data: {
              type: 'contact',
              id: '1'
            }
          },
          configuration: {
            data: {
              type: 'configuration',
              id: '3'
            }
          },
          parent_platform: {
            data: {
              type: 'platform',
              id: '4'
            }
          }
        }
      }
      expect(output).toEqual(expectedOutput)
    })
    it('should work if the deviceMountAction has no id and a parent device', () => {
      const parentDevice = new Device()
      parentDevice.id = '4'

      const deviceMountAction = DeviceMountAction.createFromObject({
        id: '',
        device,
        parentPlatform: null,
        parentDevice,
        beginDate: DateTime.utc(2020, 1, 1),
        endDate: null,
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        epsgCode: '',
        x: null,
        y: null,
        z: null,
        elevationDatumName: '',
        elevationDatumUri: '',
        beginContact: contact,
        endContact: null,
        beginDescription: 'Device mount',
        endDescription: ''
      })

      const serializer = new DeviceMountActionSerializer()

      const output = serializer.convertModelToJsonApiData(configurationId, deviceMountAction)

      const expectedOutput = {
        type: 'device_mount_action',
        attributes: {
          offset_x: 0,
          offset_y: 0,
          offset_z: 0,
          begin_description: 'Device mount',
          end_description: '',
          begin_date: '2020-01-01T00:00:00.000Z',
          end_date: null,
          epsg_code: '',
          x: null,
          y: null,
          z: null,
          elevation_datum_name: '',
          elevation_datum_uri: ''
        },
        relationships: {
          device: {
            data: {
              type: 'device',
              id: '2'
            }
          },
          begin_contact: {
            data: {
              type: 'contact',
              id: '1'
            }
          },
          configuration: {
            data: {
              type: 'configuration',
              id: '3'
            }
          },
          parent_device: {
            data: {
              type: 'device',
              id: '4'
            }
          }
        }
      }
      expect(output).toEqual(expectedOutput)
    })
    it('should also work with an existing id', () => {
      deviceMountAction.id = '5'

      const serializer = new DeviceMountActionSerializer()

      const output = serializer.convertModelToJsonApiData(configurationId, deviceMountAction)

      const expectedOutput = {
        type: 'device_mount_action',
        id: '5',
        attributes: {
          offset_x: 0,
          offset_y: 0,
          offset_z: 0,
          begin_description: 'Device mount',
          end_description: '',
          begin_date: '2020-01-01T00:00:00.000Z',
          end_date: null,
          epsg_code: '',
          x: null,
          y: null,
          z: null,
          elevation_datum_name: '',
          elevation_datum_uri: ''
        },
        relationships: {
          device: {
            data: {
              type: 'device',
              id: '2'
            }
          },
          begin_contact: {
            data: {
              type: 'contact',
              id: '1'
            }
          },
          configuration: {
            data: {
              type: 'configuration',
              id: '3'
            }
          }
        }
      }
      expect(output).toEqual(expectedOutput)
    })
  })

  describe('#convertJsonApiObjectListToModelList', () => {
    it('should return a list of mount actions with devices and parent platforms', () => {
      // Example request:
      // GET /backend/api/v1/configurations/1/device-mount-actions?page[size]=10000&include=begin_contact,end_contact,parent_platform,device
      const response: IJsonApiEntityListEnvelope = {
        data: [
          {
            type: 'device_mount_action',
            attributes: {
              begin_date: '2022-08-02T14:02:28.289000',
              offset_y: 2.0,
              end_date: '2022-08-03T14:02:00',
              created_at: '2022-08-02T14:03:02.756277',
              updated_at: null,
              end_description: 'end of mount',
              offset_x: 1.0,
              offset_z: 3.0,
              begin_description: 'begin of mount',
              epsg_code: 'epsg:4326',
              x: 12.5,
              y: 52.1,
              z: 0.0,
              elevation_datum_name: 'MSL',
              elevation_datum_uri: 'http://cv/el/1'
            },
            relationships: {
              parent_platform: {
                data: undefined
              },
              begin_contact: {
                links: {
                  related: '/backend/api/v1/contacts/1'
                },
                data: {
                  type: 'contact',
                  id: '1'
                }
              },
              device: {
                links: {
                  related: '/backend/api/v1/devices/3'
                },
                data: {
                  type: 'device',
                  id: '3'
                }
              },
              end_contact: {
                links: {
                  related: '/backend/api/v1/contacts/1'
                },
                data: {
                  type: 'contact',
                  id: '1'
                }
              }
            },
            id: '1',
            links: {
              self: '/backend/api/v1/device-mount-actions/1'
            }
          },
          {
            type: 'device_mount_action',
            attributes: {
              begin_date: '2022-08-03T06:18:52.768000',
              offset_y: 5.0,
              end_date: null,
              created_at: '2022-08-03T06:20:28.479636',
              updated_at: null,
              end_description: null,
              offset_x: 4.0,
              offset_z: 6.0,
              begin_description: 'begin of another mount'
            },
            relationships: {
              parent_platform: {
                links: {
                  related: '/backend/api/v1/platforms/1'
                },
                data: {
                  type: 'platform',
                  id: '1'
                }
              },
              begin_contact: {
                links: {
                  related: '/backend/api/v1/contacts/1'
                },
                data: {
                  type: 'contact',
                  id: '1'
                }
              },
              device: {
                links: {
                  related: '/backend/api/v1/devices/2'
                },
                data: {
                  type: 'device',
                  id: '2'
                }
              }
            },
            id: '2',
            links: {
              self: '/backend/api/v1/device-mount-actions/2'
            }
          },
          {
            type: 'device_mount_action',
            attributes: {
              begin_date: '2022-08-03T06:18:52.768000',
              offset_y: 5.0,
              end_date: null,
              created_at: '2022-08-03T06:20:28.479636',
              updated_at: null,
              end_description: null,
              offset_x: 4.0,
              offset_z: 6.0,
              begin_description: 'begin of another mount'
            },
            relationships: {
              parent_device: {
                links: {
                  related: '/backend/api/v1/devices/4'
                },
                data: {
                  type: 'device',
                  id: '4'
                }
              },
              begin_contact: {
                links: {
                  related: '/backend/api/v1/contacts/1'
                },
                data: {
                  type: 'contact',
                  id: '1'
                }
              },
              device: {
                links: {
                  related: '/backend/api/v1/devices/2'
                },
                data: {
                  type: 'device',
                  id: '2'
                }
              }
            },
            id: '3',
            links: {
              self: '/backend/api/v1/device-mount-actions/2'
            }
          }
        ],
        included: [
          {
            type: 'contact',
            attributes: {
              active: true,
              family_name: 'Musterfrau',
              website: null,
              given_name: 'Mary',
              email: 'mary.musterfrau@foo.bar'
            },
            relationships: {
              user: {
                links: {
                  related: '/backend/api/v1/users/1'
                }
              }
            },
            id: '1',
            links: {
              self: '/backend/api/v1/contacts/1'
            }
          },
          {
            type: 'device',
            relationships: {},
            attributes: {
              updated_at: '2022-05-13T09:29:38.778893',
              website: '',
              manufacturer_name: 'Ackermann KG',
              serial_number: '456',
              device_type_name: 'Accelerometer',
              manufacturer_uri: 'http://rz-vm64.gfz-potsdam.de/cv/api/v1/manufacturers/22/',
              dual_use: false,
              status_name: 'In Use',
              is_internal: true,
              short_name: 'Test internal',
              created_at: '2022-05-13T09:28:10.732032',
              inventory_number: '',
              description: '',
              model: '123',
              persistent_identifier: null,
              is_public: false,
              long_name: '',
              status_uri: 'http://rz-vm64.gfz-potsdam.de/cv/api/v1/equipmentstatus/2/',
              device_type_uri: 'http://rz-vm64.gfz-potsdam.de/cv/api/v1/equipmenttypes/48/',
              group_ids: [
                '1317'
              ],
              is_private: false
            },
            id: '3',
            links: {
              self: '/backend/api/v1/devices/3'
            }
          },
          {
            type: 'platform',
            attributes: {
              updated_at: '2022-07-13T09:30:58.046603',
              website: '',
              manufacturer_name: '',
              serial_number: '12345',
              platform_type_name: '',
              manufacturer_uri: '',
              is_internal: true,
              status_name: 'Maintenance',
              short_name: 'Foo!',
              created_at: '2022-05-11T10:07:34.551479',
              inventory_number: '',
              description: '',
              model: '',
              persistent_identifier: null,
              is_public: false,
              long_name: 'Foo Platform',
              status_uri: 'http://rz-vm64.gfz-potsdam.de/cv/api/v1/equipmentstatus/7/',
              group_ids: [
                '1318'
              ],
              is_private: false,
              platform_type_uri: ''
            },
            relationships: {},
            id: '1',
            links: {
              self: '/backend/api/v1/platforms/1'
            }
          },
          {
            type: 'device',
            relationships: {},
            attributes: {
              updated_at: '2022-07-13T09:38:27.713539',
              website: '',
              manufacturer_name: '',
              serial_number: '',
              device_type_name: '',
              manufacturer_uri: '',
              dual_use: false,
              status_name: '',
              is_internal: true,
              short_name: 'New test!',
              created_at: '2022-05-11T15:17:32.759436',
              inventory_number: '',
              description: '',
              model: '',
              persistent_identifier: null,
              is_public: false,
              long_name: 'new Test device',
              status_uri: '',
              device_type_uri: '',
              group_ids: [
                '1317',
                '1318'
              ],
              is_private: false
            },
            id: '2',
            links: {
              self: '/backend/api/v1/devices/2'
            }
          },
          {
            type: 'device',
            relationships: {},
            attributes: {
              updated_at: '2022-07-13T09:38:27.713539',
              website: '',
              manufacturer_name: '',
              serial_number: '',
              device_type_name: '',
              manufacturer_uri: '',
              dual_use: false,
              status_name: '',
              is_internal: true,
              short_name: 'New test!',
              created_at: '2022-05-11T15:17:32.759436',
              inventory_number: '',
              description: '',
              model: '',
              persistent_identifier: null,
              is_public: false,
              long_name: 'new Test device',
              status_uri: '',
              device_type_uri: '',
              group_ids: [
                '1317',
                '1318'
              ],
              is_private: false
            },
            id: '4',
            links: {
              self: '/backend/api/v1/devices/2'
            }
          }
        ],
        links: {
          self: 'http://backend:5000/backend/api/v1/device-mount-actions?page%5Bsize%5D=10000&include=begin_contact%2Cend_contact%2Cparent_platform%2Cdevice'
        },
        meta: {
          count: 5
        },
        jsonapi: {
          version: '1.0'
        }
      }

      // we don't check the included entities for all attributes,
      // as we expect that the other serializers work (and have their own tests)
      const contact = new Contact()
      contact.id = '1'

      const device1 = new Device()
      device1.id = '3'

      const device2 = new Device()
      device2.id = '2'

      const platform = new Platform()
      platform.id = '1'

      const parentDevice = new Device()
      parentDevice.id = '4'

      const deviceMountAction1 = new DeviceMountAction(
        '1',
        device1,
        null,
        null,
        DateTime.fromISO('2022-08-02T14:02:28.289000', { zone: 'UTC' }),
        DateTime.fromISO('2022-08-03T14:02:00', { zone: 'UTC' }),
        1.0,
        2.0,
        3.0,
        'epsg:4326',
        12.5,
        52.1,
        0.0,
        'MSL',
        'http://cv/el/1',
        contact,
        contact,
        'begin of mount',
        'end of mount'
      )

      const deviceMountAction2 = new DeviceMountAction(
        '2',
        device2,
        platform,
        null,
        DateTime.fromISO('2022-08-03T06:18:52.768000', { zone: 'UTC' }),
        null,
        4.0,
        5.0,
        6.0,
        '',
        null,
        null,
        null,
        '',
        '',
        contact,
        null,
        'begin of another mount',
        null
      )

      const deviceMountAction3 = new DeviceMountAction(
        '3',
        device2,
        null,
        parentDevice,
        DateTime.fromISO('2022-08-03T06:18:52.768000', { zone: 'UTC' }),
        null,
        4.0,
        5.0,
        6.0,
        '',
        null,
        null,
        null,
        '',
        '',
        contact,
        null,
        'begin of another mount',
        null
      )

      const serializer = new DeviceMountActionSerializer()
      const mountActions = serializer.convertJsonApiObjectListToModelList(response)

      expect(mountActions.length).toBe(3)
      // mount action 1
      expect(mountActions[0].id).toBe(deviceMountAction1.id)
      expect(mountActions[0].device.id).toBe(deviceMountAction1.device.id)
      expect(mountActions[0].parentPlatform).toBeNull()
      expect(mountActions[0].parentDevice).toBeNull()
      expect(mountActions[0].beginDate).toStrictEqual(deviceMountAction1.beginDate)
      expect(mountActions[0].endDate).not.toBeNull()
      expect(mountActions[0].endDate).toStrictEqual(deviceMountAction1.endDate)
      expect(mountActions[0].offsetX).toBe(deviceMountAction1.offsetX)
      expect(mountActions[0].offsetY).toBe(deviceMountAction1.offsetY)
      expect(mountActions[0].offsetZ).toBe(deviceMountAction1.offsetZ)
      expect(mountActions[0].beginContact.id).toBe(deviceMountAction1.beginContact.id)
      expect(mountActions[0].endContact).not.toBeNull()
      expect(mountActions[0].endContact?.id).toBe(deviceMountAction1.endContact?.id)
      expect(mountActions[0].beginDescription).toBe(deviceMountAction1.beginDescription)
      expect(mountActions[0].endDescription).not.toBeNull()
      expect(mountActions[0].endDescription).toBe(deviceMountAction1.endDescription)
      expect(mountActions[0].epsgCode).toBe(deviceMountAction1.epsgCode)
      expect(mountActions[0].x).toBe(deviceMountAction1.x)
      expect(mountActions[0].y).toBe(deviceMountAction1.y)
      expect(mountActions[0].z).toBe(deviceMountAction1.z)
      expect(mountActions[0].elevationDatumName).toBe(deviceMountAction1.elevationDatumName)
      expect(mountActions[0].elevationDatumUri).toBe(deviceMountAction1.elevationDatumUri)
      // mount action 2
      expect(mountActions[1].id).toBe(deviceMountAction2.id)
      expect(mountActions[1].device.id).toBe(deviceMountAction2.device.id)
      expect(mountActions[1].parentPlatform).not.toBeNull()
      expect(mountActions[1].parentPlatform?.id).toBe(platform.id)
      expect(mountActions[1].parentDevice).toBeNull()
      expect(mountActions[1].beginDate).toStrictEqual(deviceMountAction2.beginDate)
      expect(mountActions[1].endDate).toBeNull()
      expect(mountActions[1].offsetX).toBe(deviceMountAction2.offsetX)
      expect(mountActions[1].offsetY).toBe(deviceMountAction2.offsetY)
      expect(mountActions[1].offsetZ).toBe(deviceMountAction2.offsetZ)
      expect(mountActions[1].beginContact.id).toBe(deviceMountAction2.beginContact.id)
      expect(mountActions[1].endContact).toBeNull()
      expect(mountActions[1].beginDescription).toBe(deviceMountAction2.beginDescription)
      expect(mountActions[1].endDescription).toBe('')
      expect(mountActions[1].epsgCode).toBe('')
      expect(mountActions[1].x).toBeNull()
      expect(mountActions[1].y).toBeNull()
      expect(mountActions[1].z).toBeNull()
      expect(mountActions[1].elevationDatumName).toBe('')
      expect(mountActions[1].elevationDatumUri).toBe('')

      // mount action 3
      expect(mountActions[2].id).toBe(deviceMountAction3.id)
      expect(mountActions[2].device.id).toBe(deviceMountAction3.device.id)
      expect(mountActions[2].parentPlatform).toBeNull()
      expect(mountActions[2].parentDevice).not.toBeNull()
      expect(mountActions[2].parentDevice?.id).toBe(parentDevice.id)
      expect(mountActions[2].beginDate).toStrictEqual(deviceMountAction3.beginDate)
      expect(mountActions[2].endDate).toBeNull()
      expect(mountActions[2].offsetX).toBe(deviceMountAction3.offsetX)
      expect(mountActions[2].offsetY).toBe(deviceMountAction3.offsetY)
      expect(mountActions[2].offsetZ).toBe(deviceMountAction3.offsetZ)
      expect(mountActions[2].beginContact.id).toBe(deviceMountAction3.beginContact.id)
      expect(mountActions[2].endContact).toBeNull()
      expect(mountActions[2].beginDescription).toBe(deviceMountAction3.beginDescription)
      expect(mountActions[2].endDescription).toBe('')
      expect(mountActions[2].epsgCode).toBe('')
      expect(mountActions[2].x).toBeNull()
      expect(mountActions[2].y).toBeNull()
      expect(mountActions[2].z).toBeNull()
      expect(mountActions[2].elevationDatumName).toBe('')
      expect(mountActions[2].elevationDatumUri).toBe('')
    })
  })
})
