/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2022
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
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { Visibility } from '@/models/Visibility'
import { MountingActionsSerializer } from '@/serializers/custom/MountingActionsSerializer'
import { ConfigurationsTree } from '@/viewmodels/ConfigurationsTree'
import { DeviceNode } from '@/viewmodels/DeviceNode'
import { PlatformNode } from '@/viewmodels/PlatformNode'

describe('MountingActionsSerializer', () => {
  describe('convertApiObjectToTree', () => {
    it('should return an empty tree when it gets an empty list', () => {
      const examplePayload: any[] = []
      const serializer = new MountingActionsSerializer()
      const tree = serializer.convertApiObjectToTree(examplePayload, [])

      const expected = new ConfigurationsTree()

      expect(tree).toEqual(expected)
    })
    it('should handle a list of mounts', () => {
      const date1 = DateTime.fromISO('2022-04-11T12:08:13Z', { zone: 'UTC' })
      const date2 = DateTime.fromISO('2022-04-14T12:08:13Z', { zone: 'UTC' })
      const examplePayload = [
        {
          action: {
            data: {
              id: '1',
              type: 'platform_mount_action',
              attributes: {
                offset_x: 1,
                offset_y: 2,
                offset_z: 3,
                begin_date: date1.toISO(),
                begin_description: 'First action'
              },
              relationships: {
                configuration: {
                  data: {
                    type: 'configuration',
                    id: '2'
                  }
                },
                platform: {
                  data: {
                    type: 'platform',
                    id: '3'
                  }
                },
                begin_contact: {
                  data: {
                    type: 'contact',
                    id: '4'
                  }
                }
              }
            }
          },
          entity: {
            data: {
              id: '3',
              type: 'platform',
              attributes: {
                serial_number: '000123',
                model: '0815',
                description: 'Soil Moisture station Boeken_BF1',
                platform_type_uri: 'type/Station',
                status_uri: 'status/inuse',
                website: 'http://www.tereno.net',
                long_name: 'Soil moisture station Boeken BF1, Germany',
                inventory_number: '0001234',
                manufacturer_name: 'XYZ',
                short_name: 'boeken_BF1',
                status_name: 'in use',
                platform_type_name: 'Station',
                persistent_identifier: 'boeken_BF1',
                manufacturer_uri: 'manufacturer/xyz',
                archived: false
              },
              relationships: {
                created_by: {
                  data: null
                }
              }
            }
          },
          children: []
        },
        {
          action: {
            data: {
              id: '6',
              type: 'device_mount_action',
              attributes: {
                offset_x: 5,
                offset_y: 6,
                offset_z: 7,
                begin_date: date2.toISO(),
                begin_description: 'Second action'
              },
              relationships: {
                configuration: {
                  data: {
                    type: 'configuration',
                    id: '2'
                  }
                },
                device: {
                  data: {
                    type: 'device',
                    id: '7'
                  }
                },
                begin_contact: {
                  data: {
                    type: 'contact',
                    id: '8'
                  }
                }
              }
            }
          },
          entity: {
            data: {
              id: '7',
              type: 'device',
              attributes: {
                serial_number: '100123',
                model: '1815',
                description: 'Soil Moisture station device Boeken_BF1',
                device_type_uri: 'type/device',
                status_uri: 'status/existing',
                website: 'http://www.tereno.net/abc',
                long_name: 'Soil moisture station device Boeken BF1, Germany',
                inventory_number: '1001234',
                manufacturer_name: 'ABC-XYZ',
                short_name: 'boeken_BF11',
                status_name: 'existing',
                device_type_name: 'Device',
                persistent_identifier: 'boeken_BF11',
                manufacturer_uri: 'manufacturer/xy',
                dualuse: false,
                archived: false
              },
              relationships: {
                created_by: {
                  data: null
                }
              }
            }
          },
          children: []
        }
      ]

      const contacts = [
        Contact.createFromObject({
          id: '4',
          givenName: 'Max',
          familyName: 'Mustermann',
          email: 'max@muster.mann',
          website: ''
        }),
        Contact.createFromObject({
          id: '8',
          givenName: 'Humer',
          familyName: 'Simson',
          email: 'humer@j.fuxnews',
          website: ''
        })
      ]

      const serializer = new MountingActionsSerializer()
      const tree = serializer.convertApiObjectToTree(examplePayload, contacts)

      const expected = new ConfigurationsTree()
      expected.push(new PlatformNode(
        PlatformMountAction.createFromObject({
          id: '1',
          offsetX: 1,
          offsetY: 2,
          offsetZ: 3,
          beginContact: contacts[0],
          endContact: null,
          beginDescription: 'First action',
          endDescription: '',
          beginDate: date1,
          endDate: null,
          platform: Platform.createFromObject({
            id: '3',
            serialNumber: '000123',
            model: '0815',
            description: 'Soil Moisture station Boeken_BF1',
            platformTypeUri: 'type/Station',
            statusUri: 'status/inuse',
            website: 'http://www.tereno.net',
            longName: 'Soil moisture station Boeken BF1, Germany',
            inventoryNumber: '0001234',
            manufacturerName: 'XYZ',
            shortName: 'boeken_BF1',
            statusName: 'in use',
            platformTypeName: 'Station',
            persistentIdentifier: 'boeken_BF1',
            manufacturerUri: 'manufacturer/xyz',
            contacts: [],
            createdBy: null,
            createdByUserId: null,
            createdAt: null,
            updatedAt: null,
            updateDescription: '',
            updatedBy: null,
            permissionGroups: [],
            visibility: Visibility.Internal,
            archived: false,
            attachments: []
          }),
          parentPlatform: null
        })
      ))

      expected.push(new DeviceNode(
        DeviceMountAction.createFromObject({
          id: '6',
          offsetX: 5,
          offsetY: 6,
          offsetZ: 7,
          beginContact: contacts[1],
          endContact: null,
          beginDescription: 'Second action',
          endDescription: '',
          beginDate: date2,
          endDate: null,
          device: Device.createFromObject({
            id: '7',
            serialNumber: '100123',
            model: '1815',
            description: 'Soil Moisture station device Boeken_BF1',
            deviceTypeUri: 'type/device',
            statusUri: 'status/existing',
            website: 'http://www.tereno.net/abc',
            longName: 'Soil moisture station device Boeken BF1, Germany',
            inventoryNumber: '1001234',
            manufacturerName: 'ABC-XYZ',
            shortName: 'boeken_BF11',
            statusName: 'existing',
            deviceTypeName: 'Device',
            persistentIdentifier: 'boeken_BF11',
            manufacturerUri: 'manufacturer/xy',
            contacts: [],
            createdBy: null,
            createdByUserId: null,
            createdAt: null,
            updatedAt: null,
            updateDescription: '',
            updatedBy: null,
            permissionGroups: [],
            visibility: Visibility.Internal,
            attachments: [],
            customFields: [],
            properties: [],
            dualUse: false,
            archived: false
          }),
          parentPlatform: null
        })
      ))

      expect(tree).toEqual(expected)
    })
    it('should handle children in the hierarchy', () => {
      const date1 = DateTime.fromISO('2022-04-11T12:08:13Z', { zone: 'UTC' })
      const date2 = DateTime.fromISO('2022-04-14T12:08:13Z', { zone: 'UTC' })
      const examplePayload = [
        {
          action: {
            data: {
              id: '1',
              type: 'platform_mount_action',
              attributes: {
                offset_x: 1,
                offset_y: 2,
                offset_z: 3,
                begin_date: date1.toISO(),
                begin_description: 'First action'
              },
              relationships: {
                configuration: {
                  data: {
                    type: 'configuration',
                    id: '2'
                  }
                },
                platform: {
                  data: {
                    type: 'platform',
                    id: '3'
                  }
                },
                begin_contact: {
                  data: {
                    type: 'contact',
                    id: '4'
                  }
                }
              }
            }
          },
          entity: {
            data: {
              id: '3',
              type: 'platform',
              attributes: {
                serial_number: '000123',
                model: '0815',
                description: 'Soil Moisture station Boeken_BF1',
                platform_type_uri: 'type/Station',
                status_uri: 'status/inuse',
                website: 'http://www.tereno.net',
                long_name: 'Soil moisture station Boeken BF1, Germany',
                inventory_number: '0001234',
                manufacturer_name: 'XYZ',
                short_name: 'boeken_BF1',
                status_name: 'in use',
                platform_type_name: 'Station',
                persistent_identifier: 'boeken_BF1',
                manufacturer_uri: 'manufacturer/xyz',
                archived: false
              },
              relationships: {
                created_by: {
                  data: null
                }
              }
            }
          },
          children: [
            {
              action: {
                data: {
                  id: '6',
                  type: 'device_mount_action',
                  attributes: {
                    offset_x: 5,
                    offset_y: 6,
                    offset_z: 7,
                    begin_date: date2.toISO(),
                    begin_description: 'Second action'
                  },
                  relationships: {
                    configuration: {
                      data: {
                        type: 'configuration',
                        id: '2'
                      }
                    },
                    device: {
                      data: {
                        type: 'device',
                        id: '7'
                      }
                    },
                    parent_platform: {
                      data: {
                        type: 'platform',
                        id: '3'
                      }
                    },
                    begin_contact: {
                      data: {
                        type: 'contact',
                        id: '8'
                      }
                    }
                  }
                }
              },
              entity: {
                data: {
                  id: '7',
                  type: 'device',
                  attributes: {
                    serial_number: '100123',
                    model: '1815',
                    description: 'Soil Moisture station device Boeken_BF1',
                    device_type_uri: 'type/device',
                    status_uri: 'status/existing',
                    website: 'http://www.tereno.net/abc',
                    long_name: 'Soil moisture station device Boeken BF1, Germany',
                    inventory_number: '1001234',
                    manufacturer_name: 'ABC-XYZ',
                    short_name: 'boeken_BF11',
                    status_name: 'existing',
                    device_type_name: 'Device',
                    persistent_identifier: 'boeken_BF11',
                    manufacturer_uri: 'manufacturer/xy',
                    dualuse: false,
                    archived: false
                  },
                  relationships: {
                    created_by: {
                      data: null
                    }
                  }
                }
              },
              children: []
            }
          ]
        }
      ]

      const contacts = [
        Contact.createFromObject({
          id: '4',
          givenName: 'Max',
          familyName: 'Mustermann',
          email: 'max@muster.mann',
          website: ''
        }),
        Contact.createFromObject({
          id: '8',
          givenName: 'Humer',
          familyName: 'Simson',
          email: 'humer@j.fuxnews',
          website: ''
        })
      ]

      const serializer = new MountingActionsSerializer()
      const tree = serializer.convertApiObjectToTree(examplePayload, contacts)

      const expected = new ConfigurationsTree()
      const platform = Platform.createFromObject({
        id: '3',
        serialNumber: '000123',
        model: '0815',
        description: 'Soil Moisture station Boeken_BF1',
        platformTypeUri: 'type/Station',
        statusUri: 'status/inuse',
        website: 'http://www.tereno.net',
        longName: 'Soil moisture station Boeken BF1, Germany',
        inventoryNumber: '0001234',
        manufacturerName: 'XYZ',
        shortName: 'boeken_BF1',
        statusName: 'in use',
        platformTypeName: 'Station',
        persistentIdentifier: 'boeken_BF1',
        manufacturerUri: 'manufacturer/xyz',
        contacts: [],
        createdBy: null,
        createdByUserId: null,
        createdAt: null,
        updatedAt: null,
        updateDescription: '',
        updatedBy: null,
        permissionGroups: [],
        visibility: Visibility.Internal,
        archived: false,
        attachments: []
      })
      const deviceMountNode = new DeviceNode(
        DeviceMountAction.createFromObject({
          id: '6',
          offsetX: 5,
          offsetY: 6,
          offsetZ: 7,
          beginContact: contacts[1],
          endContact: null,
          beginDescription: 'Second action',
          endDescription: '',
          beginDate: date2,
          endDate: null,
          device: Device.createFromObject({
            id: '7',
            serialNumber: '100123',
            model: '1815',
            description: 'Soil Moisture station device Boeken_BF1',
            deviceTypeUri: 'type/device',
            statusUri: 'status/existing',
            website: 'http://www.tereno.net/abc',
            longName: 'Soil moisture station device Boeken BF1, Germany',
            inventoryNumber: '1001234',
            manufacturerName: 'ABC-XYZ',
            shortName: 'boeken_BF11',
            statusName: 'existing',
            deviceTypeName: 'Device',
            persistentIdentifier: 'boeken_BF11',
            manufacturerUri: 'manufacturer/xy',
            contacts: [],
            createdBy: null,
            createdByUserId: null,
            createdAt: null,
            updatedAt: null,
            updateDescription: '',
            updatedBy: null,
            permissionGroups: [],
            visibility: Visibility.Internal,
            archived: false,
            attachments: [],
            customFields: [],
            properties: [],
            dualUse: false
          }),
          parentPlatform: platform
        })
      )
      const platformMountNode = new PlatformNode(
        PlatformMountAction.createFromObject({
          id: '1',
          offsetX: 1,
          offsetY: 2,
          offsetZ: 3,
          beginContact: contacts[0],
          endContact: null,
          beginDescription: 'First action',
          endDescription: '',
          beginDate: date1,
          endDate: null,
          platform,
          parentPlatform: null
        })
      )
      platformMountNode.children = [deviceMountNode]
      expected.push(platformMountNode)

      expect(tree).toEqual(expected)
    })
  })
})
