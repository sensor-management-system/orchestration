/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
          organization: '',
          website: '',
          orcid: '',
          createdAt: null,
          updatedAt: null,
          createdByUserId: null
        }),
        Contact.createFromObject({
          id: '8',
          givenName: 'Humer',
          familyName: 'Simson',
          email: 'humer@j.fuxnews',
          organization: '',
          website: '',
          orcid: '',
          createdAt: null,
          updatedAt: null,
          createdByUserId: null
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
          epsgCode: '',
          x: null,
          y: null,
          z: null,
          elevationDatumName: '',
          elevationDatumUri: '',
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
            country: '',
            attachments: [],
            images: [],
            parameters: [],
            keywords: []
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
          epsgCode: '',
          x: null,
          y: null,
          z: null,
          elevationDatumName: '',
          elevationDatumUri: '',
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
            images: [],
            customFields: [],
            properties: [],
            parameters: [],
            archived: false,
            keywords: [],
            country: ''
          }),
          parentPlatform: null,
          parentDevice: null
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
          website: '',
          organization: '',
          orcid: '',
          createdAt: null,
          updatedAt: null,
          createdByUserId: null
        }),
        Contact.createFromObject({
          id: '8',
          givenName: 'Humer',
          familyName: 'Simson',
          email: 'humer@j.fuxnews',
          organization: '',
          orcid: '',
          website: '',
          createdAt: null,
          updatedAt: null,
          createdByUserId: null
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
        country: '',
        attachments: [],
        images: [],
        parameters: [],
        keywords: []
      })
      const deviceMountNode = new DeviceNode(
        DeviceMountAction.createFromObject({
          id: '6',
          offsetX: 5,
          offsetY: 6,
          offsetZ: 7,
          epsgCode: '',
          x: null,
          y: null,
          z: null,
          elevationDatumName: '',
          elevationDatumUri: '',
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
            images: [],
            customFields: [],
            properties: [],
            parameters: [],
            keywords: [],
            country: ''
          }),
          parentPlatform: platform,
          parentDevice: null
        })
      )
      const platformMountNode = new PlatformNode(
        PlatformMountAction.createFromObject({
          id: '1',
          offsetX: 1,
          offsetY: 2,
          offsetZ: 3,
          epsgCode: '',
          x: null,
          y: null,
          z: null,
          elevationDatumName: '',
          elevationDatumUri: '',
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

    it('should handle children in the hierarchy without platforms too', () => {
      const date1 = DateTime.fromISO('2022-04-11T12:08:13Z', { zone: 'UTC' })
      const date2 = DateTime.fromISO('2022-04-14T12:08:13Z', { zone: 'UTC' })
      const examplePayload = [
        {
          action: {
            data: {
              id: '1',
              type: 'device_mount_action',
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
                device: {
                  data: {
                    type: 'device',
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
              type: 'device',
              attributes: {
                serial_number: '000123',
                model: '0815',
                description: 'Soil Moisture station Boeken_BF1',
                device_type_uri: 'type/Station',
                status_uri: 'status/inuse',
                website: 'http://www.tereno.net',
                long_name: 'Soil moisture station Boeken BF1, Germany',
                inventory_number: '0001234',
                manufacturer_name: 'XYZ',
                short_name: 'boeken_BF1',
                status_name: 'in use',
                device_type_name: 'Station',
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
                    parent_device: {
                      data: {
                        type: 'device',
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
          website: '',
          organization: '',
          orcid: '',
          createdAt: null,
          updatedAt: null,
          createdByUserId: null
        }),
        Contact.createFromObject({
          id: '8',
          givenName: 'Humer',
          familyName: 'Simson',
          email: 'humer@j.fuxnews',
          organization: '',
          orcid: '',
          website: '',
          createdAt: null,
          updatedAt: null,
          createdByUserId: null
        })
      ]

      const serializer = new MountingActionsSerializer()
      const tree = serializer.convertApiObjectToTree(examplePayload, contacts)

      const expected = new ConfigurationsTree()
      const parentDevice = Device.createFromObject({
        id: '3',
        serialNumber: '000123',
        model: '0815',
        description: 'Soil Moisture station Boeken_BF1',
        deviceTypeUri: 'type/Station',
        statusUri: 'status/inuse',
        website: 'http://www.tereno.net',
        longName: 'Soil moisture station Boeken BF1, Germany',
        inventoryNumber: '0001234',
        manufacturerName: 'XYZ',
        shortName: 'boeken_BF1',
        statusName: 'in use',
        deviceTypeName: 'Station',
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
        attachments: [],
        images: [],
        parameters: [],
        customFields: [],
        properties: [],
        keywords: [],
        country: ''
      })
      const deviceMountNode = new DeviceNode(
        DeviceMountAction.createFromObject({
          id: '6',
          offsetX: 5,
          offsetY: 6,
          offsetZ: 7,
          epsgCode: '',
          x: null,
          y: null,
          z: null,
          elevationDatumName: '',
          elevationDatumUri: '',
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
            images: [],
            customFields: [],
            properties: [],
            parameters: [],
            keywords: [],
            country: ''
          }),
          parentDevice,
          parentPlatform: null
        })
      )
      const parentMountNode = new DeviceNode(
        DeviceMountAction.createFromObject({
          id: '1',
          offsetX: 1,
          offsetY: 2,
          offsetZ: 3,
          epsgCode: '',
          x: null,
          y: null,
          z: null,
          elevationDatumName: '',
          elevationDatumUri: '',
          beginContact: contacts[0],
          endContact: null,
          beginDescription: 'First action',
          endDescription: '',
          beginDate: date1,
          endDate: null,
          device: parentDevice,
          parentPlatform: null,
          parentDevice: null
        })
      )
      parentMountNode.children = [deviceMountNode]
      expected.push(parentMountNode)

      expect(tree).toEqual(expected)
    })
  })
})
