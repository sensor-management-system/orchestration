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

import { Contact } from '@/models/Contact'
import { Platform } from '@/models/Platform'
import { PlatformMountAction } from '@/models/PlatformMountAction'

import { PlatformMountActionSerializer } from '@/serializers/jsonapi/PlatformMountActionSerializer'
import { IJsonApiEntityListEnvelope } from '@/serializers/jsonapi/JsonApiTypes'

describe('PlatformMountActionSerializer', () => {
  describe('#convertModelToJsonApiData', () => {
    const contact = new Contact()
    contact.id = '1'
    contact.givenName = 'Max'
    contact.familyName = 'Mustermann'
    contact.email = 'max@mustermann.de'

    const platform = new Platform()
    platform.id = '2'
    platform.shortName = 'platform'

    const configurationId = '3'

    const date = DateTime.utc(2020, 1, 1, 12, 0, 0)
    it('should work if the platformMountAction has no id', () => {
      const platformMountAction = PlatformMountAction.createFromObject({
        id: '',
        platform,
        parentPlatform: null,
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
        beginDate: date,
        endDate: null,
        beginDescription: 'Platform mount',
        endDescription: '',
        label: 'Mount'
      })

      const serializer = new PlatformMountActionSerializer()

      const output = serializer.convertModelToJsonApiData(configurationId, platformMountAction)

      const expectedOutput = {
        type: 'platform_mount_action',
        attributes: {
          offset_x: 0,
          offset_y: 0,
          offset_z: 0,
          begin_description: 'Platform mount',
          end_description: '',
          begin_date: '2020-01-01T12:00:00.000Z',
          end_date: null,
          epsg_code: '',
          x: null,
          y: null,
          z: null,
          elevation_datum_name: '',
          elevation_datum_uri: '',
          label: 'Mount'
        },
        relationships: {
          platform: {
            data: {
              type: 'platform',
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
    it('should work if the platformMountAction has no id and a parent platform', () => {
      const parentPlatform = new Platform()
      parentPlatform.id = '4'
      const platformMountAction = PlatformMountAction.createFromObject({
        id: '',
        platform,
        parentPlatform,
        offsetX: 1,
        offsetY: 2,
        offsetZ: 3,
        epsgCode: 'epsg:4326',
        x: 4,
        y: 5,
        z: 6,
        elevationDatumName: 'MSL',
        elevationDatumUri: 'http://cv/el/1',
        beginContact: contact,
        endContact: null,
        beginDate: date,
        endDate: null,
        beginDescription: 'Platform mount',
        endDescription: '',
        label: ''
      })

      const serializer = new PlatformMountActionSerializer()

      const output = serializer.convertModelToJsonApiData(configurationId, platformMountAction)

      const expectedOutput = {
        type: 'platform_mount_action',
        attributes: {
          offset_x: 1,
          offset_y: 2,
          offset_z: 3,
          begin_description: 'Platform mount',
          end_description: '',
          begin_date: '2020-01-01T12:00:00.000Z',
          end_date: null,
          epsg_code: 'epsg:4326',
          x: 4,
          y: 5,
          z: 6,
          elevation_datum_name: 'MSL',
          elevation_datum_uri: 'http://cv/el/1',
          label: ''
        },
        relationships: {
          platform: {
            data: {
              type: 'platform',
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
    it('should also work with an existing id', () => {
      const platformMountAction = PlatformMountAction.createFromObject({
        id: '5',
        platform,
        parentPlatform: null,
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
        beginDate: date,
        endDate: null,
        beginDescription: 'Platform mount',
        endDescription: '',
        label: ''
      })

      const serializer = new PlatformMountActionSerializer()

      const output = serializer.convertModelToJsonApiData(configurationId, platformMountAction)

      const expectedOutput = {
        type: 'platform_mount_action',
        id: '5',
        attributes: {
          offset_x: 0,
          offset_y: 0,
          offset_z: 0,
          begin_description: 'Platform mount',
          end_description: '',
          begin_date: '2020-01-01T12:00:00.000Z',
          end_date: null,
          epsg_code: '',
          x: null,
          y: null,
          z: null,
          elevation_datum_name: '',
          elevation_datum_uri: '',
          label: ''
        },
        relationships: {
          platform: {
            data: {
              type: 'platform',
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
    it('should return a list of mount actions with platforms and parent platforms', () => {
      // Example request:
      // GET /backend/api/v1/configurations/1/platform-mount-actions?page[size]=10000&include=begin_contact,end_contact,parent_platform,platform
      const response: IJsonApiEntityListEnvelope = {
        data: [
          {
            type: 'platform_mount_action',
            attributes: {
              begin_date: '2022-08-03T06:16:22.641000',
              offset_y: 2.0,
              end_date: null,
              created_at: '2022-08-03T06:17:24.369916',
              updated_at: null,
              end_description: null,
              offset_x: 1.0,
              offset_z: 3.0,
              begin_description: 'begin of mount',
              epsg_code: 'epsg:4326',
              x: 12.5,
              y: 52.1,
              z: 0.0,
              elevation_datum_name: 'MSL',
              elevation_datum_uri: 'http://cv/el/1',
              label: 'Mount'
            },
            relationships: {
              parent_platform: {
                data: undefined
              },
              platform: {
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
                  related: '/backend/api/v1/contacts/4'
                },
                data: {
                  type: 'contact',
                  id: '4'
                }
              }
            },
            id: '1',
            links: {
              self: '/backend/api/v1/platform-mount-actions/1'
            }
          },
          {
            type: 'platform_mount_action',
            attributes: {
              begin_date: '2022-08-03T06:16:22.641000',
              offset_y: 5.0,
              end_date: '2022-08-04T10:10:10.000000',
              created_at: '2022-08-03T06:17:24.369916',
              updated_at: null,
              end_description: 'end of mount',
              offset_x: 4.0,
              offset_z: 6.0,
              begin_description: 'begin of mount',
              label: null
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
              platform: {
                links: {
                  related: '/backend/api/v1/platforms/2'
                },
                data: {
                  type: 'platform',
                  id: '2'
                }
              },
              begin_contact: {
                links: {
                  related: '/backend/api/v1/contacts/4'
                },
                data: {
                  type: 'contact',
                  id: '4'
                }
              },
              end_contact: {
                links: {
                  related: '/backend/api/v1/contacts/4'
                },
                data: {
                  type: 'contact',
                  id: '4'
                }
              }
            },
            id: '2',
            links: {
              self: '/backend/api/v1/platform-mount-actions/1'
            }
          }
        ],
        included: [
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
            type: 'platform',
            attributes: {
              updated_at: '2022-07-13T09:30:58.046603',
              website: '',
              manufacturer_name: '',
              serial_number: '6789',
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
            id: '2',
            links: {
              self: '/backend/api/v1/platforms/2'
            }
          },
          {
            type: 'contact',
            attributes: {
              active: true,
              family_name: 'Mustermann',
              website: null,
              given_name: 'Max',
              email: 'max.mustermann@foo.bar'
            },
            relationships: {},
            id: '4',
            links: {
              self: '/backend/api/v1/contacts/4'
            }
          }
        ],
        links: {
          self: 'http://backend:5000/backend/api/v1/platform-mount-actions?page%5Bsize%5D=10000&include=begin_contact%2Cend_contact%2Cparent_platform%2Cplatform'
        },
        meta: {
          count: 2
        },
        jsonapi: {
          version: '1.0'
        }
      }

      // we don't check the included entities for all attributes,
      // as we expect that the other serializers work (and have their own tests)
      const contact = new Contact()
      contact.id = '4'

      const platform1 = new Platform()
      platform1.id = '1'

      const platform2 = new Platform()
      platform2.id = '2'

      const platformMountAction1 = new PlatformMountAction(
        '1',
        platform1,
        null,
        DateTime.fromISO('2022-08-03T06:16:22.641000', { zone: 'UTC' }),
        null,
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
        null,
        'begin of mount',
        null,
        'Mount'
      )

      const platformMountAction2 = new PlatformMountAction(
        '2',
        platform2,
        platform1,
        DateTime.fromISO('2022-08-03T06:16:22.641000', { zone: 'UTC' }),
        DateTime.fromISO('2022-08-04T10:10:10.000000', { zone: 'UTC' }),
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
        contact,
        'begin of mount',
        'end of mount',
        ''
      )

      const serializer = new PlatformMountActionSerializer()
      const mountActions = serializer.convertJsonApiObjectListToModelList(response)

      expect(mountActions.length).toBe(2)
      // mount action 1
      expect(mountActions[0].id).toBe(platformMountAction1.id)
      expect(mountActions[0].platform.id).toBe(platformMountAction1.platform.id)
      expect(mountActions[0].parentPlatform).toBeNull()
      expect(mountActions[0].beginDate).toStrictEqual(platformMountAction1.beginDate)
      expect(mountActions[0].endDate).toBeNull()
      expect(mountActions[0].offsetX).toBe(platformMountAction1.offsetX)
      expect(mountActions[0].offsetY).toBe(platformMountAction1.offsetY)
      expect(mountActions[0].offsetZ).toBe(platformMountAction1.offsetZ)
      expect(mountActions[0].beginContact.id).toBe(platformMountAction1.beginContact.id)
      expect(mountActions[0].endContact).toBeNull()
      expect(mountActions[0].beginDescription).toBe(platformMountAction1.beginDescription)
      expect(mountActions[0].endDescription).toBe('')
      expect(mountActions[0].epsgCode).toBe(platformMountAction1.epsgCode)
      expect(mountActions[0].x).toBe(platformMountAction1.x)
      expect(mountActions[0].y).toBe(platformMountAction1.y)
      expect(mountActions[0].z).toBe(platformMountAction1.z)
      expect(mountActions[0].elevationDatumName).toBe(platformMountAction1.elevationDatumName)
      expect(mountActions[0].elevationDatumUri).toBe(platformMountAction1.elevationDatumUri)
      expect(mountActions[0].label).toBe(platformMountAction1.label)
      // mount action 2
      expect(mountActions[1].id).toBe(platformMountAction2.id)
      expect(mountActions[1].platform.id).toBe(platformMountAction2.platform.id)
      expect(mountActions[1].parentPlatform).not.toBeNull()
      expect(mountActions[1].parentPlatform?.id).toBe(platform1.id)
      expect(mountActions[1].beginDate).toStrictEqual(platformMountAction2.beginDate)
      expect(mountActions[1].endDate).not.toBeNull()
      expect(mountActions[1].endDate).toStrictEqual(platformMountAction2.endDate)
      expect(mountActions[1].offsetX).toBe(platformMountAction2.offsetX)
      expect(mountActions[1].offsetY).toBe(platformMountAction2.offsetY)
      expect(mountActions[1].offsetZ).toBe(platformMountAction2.offsetZ)
      expect(mountActions[1].beginContact.id).toBe(platformMountAction2.beginContact.id)
      expect(mountActions[1].endContact).not.toBeNull()
      expect(mountActions[1].endContact?.id).toBe(platformMountAction2.endContact?.id)
      expect(mountActions[1].beginDescription).toBe(platformMountAction2.beginDescription)
      expect(mountActions[1].endDescription).toBe(platformMountAction2.endDescription)
      expect(mountActions[1].epsgCode).toBe('')
      expect(mountActions[1].x).toBeNull()
      expect(mountActions[1].y).toBeNull()
      expect(mountActions[1].z).toBeNull()
      expect(mountActions[1].elevationDatumName).toBe('')
      expect(mountActions[1].elevationDatumUri).toBe('')
      expect(mountActions[1].label).toBe(platformMountAction2.label)
    })
  })
})
