/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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
import { Platform } from '@/models/Platform'
import { Attachment } from '@/models/Attachment'

import { PlatformSerializer, IPlatformWithMeta, platformWithMetaToPlatformByThrowingErrorOnMissing, platformWithMetaToPlatformByAddingDummyObjects } from '@/serializers/jsonapi/PlatformSerializer'
import { IJsonApiTypeIdDataList } from '@/serializers/jsonapi/JsonApiTypes'

const createTestPlatform = () => {
  const platform = new Platform()
  platform.description = 'This is a dummy description'
  platform.shortName = 'Dummy short name'
  platform.longName = 'Dummy long long long name'
  platform.serialNumber = '12345'
  platform.inventoryNumber = '6789'
  platform.manufacturerUri = 'manufacturer/manu1'
  platform.manufacturerName = 'Manu1'
  platform.platformTypeUri = 'platformType/typeA'
  platform.platformTypeName = 'Type A'
  platform.statusUri = 'status/Ok'
  platform.statusName = 'Okay'
  platform.model = '0815'
  platform.persistentIdentifier = 'doi:4354545'
  platform.website = 'http://gfz-potsdam.de'
  platform.createdAt = DateTime.utc(2020, 8, 28, 13, 49, 48, 15)
  platform.updatedAt = DateTime.utc(2020, 8, 30, 13, 49, 48, 15)

  platform.attachments = [
    Attachment.createFromObject({
      id: '2',
      label: 'GFZ',
      url: 'http://www.gfz-potsdam.de'
    }),
    Attachment.createFromObject({
      id: null,
      label: 'UFZ',
      url: 'http://www.ufz.de'
    })
  ]

  platform.contacts = [
    Contact.createFromObject({
      id: '4',
      givenName: 'Max',
      familyName: 'Mustermann',
      email: 'max@mustermann.de',
      website: ''
    }),
    Contact.createFromObject({
      id: '5',
      givenName: 'Mux',
      familyName: 'Mastermunn',
      email: 'mux@mastermunn.de',
      website: ''
    })
  ]
  return platform
}

describe('PlatformSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a json api object with multiple entries to a platform model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          type: 'platform',
          attributes: {
            serial_number: '000123',
            model: '0815',
            description: 'Soil Moisture station Boeken_BF1',
            attachments: [{
              label: 'GFZ',
              url: 'http://www.gfz-potsdam.de',
              id: '12'
            }],
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
            manufacturer_uri: 'manufacturer/xyz'
          },
          relationships: {
            updated_by: {
              links: {
                self: '/rdm/svm-api/v1/platforms/37/relationships/updatedUser'
              }
            },
            contacts: {
              links: {
                self: '/rdm/svm-api/v1/platforms/37/relationships/contacts',
                related: '/rdm/svm-api/v1/platforms/37/contacts'
              },
              data: [{
                type: 'contact',
                id: '1'
              }]
            },
            platform_attachments: {
              links: {
                self: '/rdm/svm-api/v1/platforms/37/relationships/platform-attachments',
                related: '/rdm/svm-api/v1/platforms/37/platform-attachments'
              },
              data: [{
                type: 'platform_attachment',
                id: '12'
              }]
            },
            created_by: {
              links: {
                self: '/rdm/svm-api/v1/platforms/37/relationships/createdUser'
              }
            }
          },
          id: '37',
          links: {
            self: '/rdm/svm-api/v1/platforms/37'
          }
        }, {
          type: 'platform',
          attributes: {
            serial_number: null,
            model: null,
            description: 'Groundwater level KleinTrebbow',
            platform_type_uri: 'Station',
            status_uri: null,
            website: null,
            long_name: 'Groundwater level KleinTrebbow',
            inventory_number: null,
            manufacturer_name: null,
            short_name: 'klein_trebbow',
            status_name: null,
            platform_type_name: 'Station',
            persistent_identifier: null,
            manufacturer_uri: null
          },
          relationships: {
            updated_by: {
              links: {
                self: '/rdm/svm-api/v1/platforms/52/relationships/updatedUser'
              }
            },
            contacts: {
              links: {
                self: '/rdm/svm-api/v1/platforms/52/relationships/contacts',
                related: '/rdm/svm-api/v1/platforms/52/contacts'
              },
              data: []
            },
            platform_attachments: {
              links: {
                self: '/rdm/svm-api/v1/platforms/52/relationships/platform-attachments',
                related: '/rdm/svm-api/v1/platforms/52/platform-attachments'
              },
              data: []
            },
            created_by: {
              links: {
                self: '/rdm/svm-api/v1/platforms/52/relationships/createdUser'
              }
            }
          },
          id: '52',
          links: {
            self: '/rdm/svm-api/v1/platforms/52'
          }
        }],
        links: {
          self: 'http://rz-vm64.gfz-potsdam.de:5000/rdm/svm-api/v1/platforms?include=contacts&filter=%5B%7B%22name%22%3A%22short_name%22%2C%22op%22%3A%22ilike%22%2C%22val%22%3A%22%25bo%25%25%22%7D%5D'
        },
        included: [
          {
            type: 'contact',
            relationships: {
              configurations: {
                links: {
                  self: '/rdm/svm-api/v1/contacts/1/relationships/configurations',
                  related: '/rdm/svm-api/v1/configurations?contact_id=1'
                }
              },
              user: {
                links: {
                  self: '/rdm/svm-api/v1/contacts/1/relationships/user',
                  related: '/rdm/svm-api/v1/contacts/1/users'
                },
                data: {
                  type: 'user',
                  id: '[<User 1>]'
                }
              },
              devices: {
                links: {
                  self: '/rdm/svm-api/v1/contacts/1/relationships/devices',
                  related: '/rdm/svm-api/v1/devices?contact_id=1'
                }
              },
              platforms: {
                links: {
                  self: '/rdm/svm-api/v1/contacts/1/relationships/platforms',
                  related: '/rdm/svm-api/v1/contacts/1/platforms'
                }
              }
            },
            attributes: {
              given_name: 'Max',
              email: 'test@test.test',
              website: null,
              family_name: 'Mustermann'
            },
            id: '1',
            links: {
              self: '/rdm/svm-api/v1/contacts/1'
            }
          },
          {
            type: 'platform_attachment',
            attributes: {
              url: 'http://test.test',
              label: 'test label'
            },
            relationships: {
              platform: {
                links: {
                  self: '/rdm/svm-api/v1/platform-attachments/1/relationships/platform',
                  related: '/rdm/svm-api/v1/platforms/52'
                },
                data: {
                  type: 'platform',
                  id: '52'
                }
              }
            },
            id: '12',
            links: {
              self: '/rdm/svm-api/v1/platform-attachments/1'
            }
          }
        ],
        meta: {
          count: 2
        },
        jsonapi: {
          version: '1.0'
        }
      }

      const expectedPlatform1 = new Platform()
      expectedPlatform1.id = '37'
      expectedPlatform1.serialNumber = '000123'
      expectedPlatform1.model = '0815'
      expectedPlatform1.description = 'Soil Moisture station Boeken_BF1'
      expectedPlatform1.attachments = [Attachment.createFromObject({
        id: '12',
        label: 'test label',
        url: 'http://test.test'
      })]
      expectedPlatform1.platformTypeUri = 'type/Station'
      expectedPlatform1.statusUri = 'status/inuse'
      expectedPlatform1.website = 'http://www.tereno.net'
      // expectedPlatform1.updatedAt = DateTime.utc(2020, 8, 29, 13, 48, 35, 740)
      expectedPlatform1.longName = 'Soil moisture station Boeken BF1, Germany'
      // expectedPlatform1.createdAt = DateTime.utc(2020, 8, 28, 13, 48, 35, 740)
      expectedPlatform1.inventoryNumber = '0001234'
      expectedPlatform1.manufacturerName = 'XYZ'
      expectedPlatform1.shortName = 'boeken_BF1'
      expectedPlatform1.statusName = 'in use'
      expectedPlatform1.platformTypeName = 'Station'
      expectedPlatform1.persistentIdentifier = 'boeken_BF1'
      expectedPlatform1.manufacturerUri = 'manufacturer/xyz'
      expectedPlatform1.contacts = [Contact.createFromObject({
        id: '1',
        givenName: 'Max',
        email: 'test@test.test',
        website: '',
        familyName: 'Mustermann'
      })]

      const expectedPlatform2 = new Platform()
      expectedPlatform2.id = '52'
      expectedPlatform2.serialNumber = ''
      expectedPlatform2.model = ''
      expectedPlatform2.description = 'Groundwater level KleinTrebbow'
      expectedPlatform2.attachments = []
      expectedPlatform2.platformTypeUri = 'Station'
      expectedPlatform2.statusUri = ''
      expectedPlatform2.website = ''
      expectedPlatform2.updatedAt = null
      expectedPlatform2.longName = 'Groundwater level KleinTrebbow'
      expectedPlatform2.createdAt = null
      expectedPlatform2.inventoryNumber = ''
      expectedPlatform2.manufacturerName = ''
      expectedPlatform2.shortName = 'klein_trebbow'
      expectedPlatform2.statusName = ''
      expectedPlatform2.platformTypeName = 'Station'
      expectedPlatform2.persistentIdentifier = ''
      expectedPlatform2.manufacturerUri = ''
      expectedPlatform2.contacts = []

      const serializer = new PlatformSerializer()

      const platformsWithMeta = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)
      const platforms = platformsWithMeta.map((x: IPlatformWithMeta) => x.platform)
      expect(Array.isArray(platforms)).toBeTruthy()
      expect(platforms.length).toEqual(2)

      expect(platforms[0]).toEqual(expectedPlatform1)
      expect(platforms[1]).toEqual(expectedPlatform2)

      const missingContactIds = platformsWithMeta.map((x: IPlatformWithMeta) => {
        return x.missing.contacts.ids
      })

      expect(Array.isArray(missingContactIds)).toBeTruthy()
      expect(missingContactIds.length).toEqual(2)

      expect(missingContactIds[0]).toEqual([])
      expect(missingContactIds[1]).toEqual([])
    })
  })
  describe('#convertJsonApiObjectToModel', () => {
    it('should convert a json api objet to a platform model', () => {
      const jsonApiObject: any = {
        data: {
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
          relationships: {
            updated_by: {
              links: {
                self: '/rdm/svm-api/v1/platforms/37/relationships/updatedUser'
              }
            },
            contacts: {
              links: {
                self: '/rdm/svm-api/v1/platforms/37/relationships/contacts',
                related: '/rdm/svm-api/v1/platforms/37/contacts'
              },
              data: [{
                type: 'contact',
                id: '1'
              }]
            },
            platform_attachments: {
              links: {
                self: '/rdm/svm-api/v1/platforms/52/relationships/platform-attachments',
                related: '/rdm/svm-api/v1/platforms/52/platform-attachments'
              },
              data: [{
                type: 'platform_attachment',
                id: '12'
              }]
            },
            created_by: {
              links: {
                self: '/rdm/svm-api/v1/platforms/37/relationships/createdUser'
              }
            }
          },
          id: '37',
          links: {
            self: '/rdm/svm-api/v1/platforms/37'
          }
        },
        included: [
          {
            type: 'contact',
            relationships: {
              configurations: {
                links: {
                  self: '/rdm/svm-api/v1/contacts/1/relationships/configurations',
                  related: '/rdm/svm-api/v1/configurations?contact_id=1'
                }
              },
              user: {
                links: {
                  self: '/rdm/svm-api/v1/contacts/1/relationships/user',
                  related: '/rdm/svm-api/v1/contacts/1/users'
                },
                data: {
                  type: 'user',
                  id: '[<User 1>]'
                }
              },
              devices: {
                links: {
                  self: '/rdm/svm-api/v1/contacts/1/relationships/devices',
                  related: '/rdm/svm-api/v1/devices?contact_id=1'
                }
              },
              platforms: {
                links: {
                  self: '/rdm/svm-api/v1/contacts/1/relationships/platforms',
                  related: '/rdm/svm-api/v1/contacts/1/platforms'
                }
              }
            },
            attributes: {
              given_name: 'Max',
              email: 'test@test.test',
              website: null,
              family_name: 'Mustermann'
            },
            id: '1',
            links: {
              self: '/rdm/svm-api/v1/contacts/1'
            }
          },
          {
            type: 'platform_attachment',
            attributes: {
              url: 'http://www.gfz-potsdam.de',
              label: 'GFZ'
            },
            relationships: {
              platform: {
                links: {
                  self: '/rdm/svm-api/v1/platform-attachments/1/relationships/platform',
                  related: '/rdm/svm-api/v1/platforms/52'
                },
                data: {
                  type: 'platform',
                  id: '52'
                }
              }
            },
            id: '12',
            links: {
              self: '/rdm/svm-api/v1/platform-attachments/1'
            }
          }
        ],
        meta: {
          count: 2
        },
        jsonapi: {
          version: '1.0'
        }
      }

      const expectedPlatform = new Platform()
      expectedPlatform.id = '37'
      expectedPlatform.serialNumber = '000123'
      expectedPlatform.model = '0815'
      expectedPlatform.description = 'Soil Moisture station Boeken_BF1'
      expectedPlatform.attachments = [Attachment.createFromObject({
        id: '12',
        label: 'GFZ',
        url: 'http://www.gfz-potsdam.de'
      })]
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
      expectedPlatform.contacts = [Contact.createFromObject({
        id: '1',
        givenName: 'Max',
        email: 'test@test.test',
        website: '',
        familyName: 'Mustermann'
      })]

      const serializer = new PlatformSerializer()

      const platformWithMeta = serializer.convertJsonApiObjectToModel(jsonApiObject)
      const platform = platformWithMeta.platform

      expect(platform).toEqual(expectedPlatform)

      const missingContactIds = platformWithMeta.missing.contacts.ids
      expect(Array.isArray(missingContactIds)).toBeTruthy()
      expect(missingContactIds.length).toEqual(0)
    })
  })
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
        relationships: {
          updated_by: {
            links: {
              self: '/rdm/svm-api/v1/platforms/37/relationships/updatedUser'
            }
          },
          contacts: {
            links: {
              self: '/rdm/svm-api/v1/platforms/37/relationships/contacts',
              related: '/rdm/svm-api/v1/platforms/37/contacts'
            },
            data: [{
              type: 'contact',
              id: '1'
            }]
          },
          platform_attachments: {
            links: {
              self: '/rdm/svm-api/v1/platforms/37/relationships/platform-attachments',
              related: '/rdm/svm-api/v1/platforms/37/platform-attachments'
            },
            data: [
              {
                type: 'platform_attachment',
                id: '12'
              }
            ]
          },
          created_by: {
            links: {
              self: '/rdm/svm-api/v1/platforms/37/relationships/createdUser'
            }
          }
        },
        id: '37',
        links: {
          self: '/rdm/svm-api/v1/platforms/37'
        }
      }
      const included = [
        {
          type: 'contact',
          relationships: {
            configurations: {
              links: {
                self: '/rdm/svm-api/v1/contacts/1/relationships/configurations',
                related: '/rdm/svm-api/v1/configurations?contact_id=1'
              }
            },
            user: {
              links: {
                self: '/rdm/svm-api/v1/contacts/1/relationships/user',
                related: '/rdm/svm-api/v1/contacts/1/users'
              },
              data: {
                type: 'user',
                id: '[<User 1>]'
              }
            },
            devices: {
              links: {
                self: '/rdm/svm-api/v1/contacts/1/relationships/devices',
                related: '/rdm/svm-api/v1/devices?contact_id=1'
              }
            },
            platforms: {
              links: {
                self: '/rdm/svm-api/v1/contacts/1/relationships/platforms',
                related: '/rdm/svm-api/v1/contacts/1/platforms'
              }
            }
          },
          attributes: {
            given_name: 'Max',
            email: 'test@test.test',
            website: null,
            family_name: 'Mustermann'
          },
          id: '1',
          links: {
            self: '/rdm/svm-api/v1/contacts/1'
          }
        },
        {
          type: 'platform_attachment',
          attributes: {
            url: 'http://www.gfz-potsdam.de',
            label: 'GFZ'
          },
          relationships: {
            platform: {
              links: {
                self: '/rdm/svm-api/v1/platform-attachments/1/relationships/platform',
                related: '/rdm/svm-api/v1/platforms/37'
              },
              data: {
                type: 'platform',
                id: '37'
              }
            }
          },
          id: '12',
          links: {
            self: '/rdm/svm-api/v1/platform-attachments/1'
          }
        }
      ]

      const expectedPlatform = new Platform()
      expectedPlatform.id = '37'
      expectedPlatform.serialNumber = '000123'
      expectedPlatform.model = '0815'
      expectedPlatform.description = 'Soil Moisture station Boeken_BF1'
      expectedPlatform.attachments = [Attachment.createFromObject({
        id: '12',
        label: 'GFZ',
        url: 'http://www.gfz-potsdam.de'
      })]

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
      expectedPlatform.contacts = [Contact.createFromObject({
        id: '1',
        givenName: 'Max',
        email: 'test@test.test',
        website: '',
        familyName: 'Mustermann'
      })]

      const serializer = new PlatformSerializer()
      const platfromWithMeta = serializer.convertJsonApiDataToModel(jsonApiData, included)
      const platform = platfromWithMeta.platform

      expect(platform).toEqual(expectedPlatform)

      const missingContactIds = platfromWithMeta.missing.contacts.ids
      expect(Array.isArray(missingContactIds)).toBeTruthy()
      expect(missingContactIds.length).toEqual(0)
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should convert a model to json data object with all of the subelements', () => {
      const platform = createTestPlatform()

      const serializer = new PlatformSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(platform)

      expect(typeof jsonApiData).toEqual('object')

      expect(jsonApiData).not.toHaveProperty('id')

      expect(jsonApiData).toHaveProperty('type')
      expect(jsonApiData.type).toEqual('platform')

      expect(jsonApiData).toHaveProperty('attributes')
      const attributes = jsonApiData.attributes
      expect(typeof attributes).toBe('object')

      expect(attributes).toHaveProperty('description')
      expect(attributes.description).toEqual('This is a dummy description')
      expect(attributes).toHaveProperty('short_name')
      expect(attributes.short_name).toEqual('Dummy short name')
      expect(attributes).toHaveProperty('long_name')
      expect(attributes.long_name).toEqual('Dummy long long long name')
      expect(attributes).toHaveProperty('serial_number')
      expect(attributes.serial_number).toEqual('12345')
      expect(attributes).toHaveProperty('inventory_number')
      expect(attributes.inventory_number).toEqual('6789')
      expect(attributes).toHaveProperty('manufacturer_uri')
      expect(attributes.manufacturer_uri).toEqual('manufacturer/manu1')
      expect(attributes).toHaveProperty('manufacturer_name')
      expect(attributes.manufacturer_name).toEqual('Manu1')
      expect(attributes).toHaveProperty('platform_type_uri')
      expect(attributes.platform_type_uri).toEqual('platformType/typeA')
      expect(attributes).toHaveProperty('platform_type_name')
      expect(attributes.platform_type_name).toEqual('Type A')
      expect(attributes).toHaveProperty('status_uri')
      expect(attributes.status_uri).toEqual('status/Ok')
      expect(attributes).toHaveProperty('status_name')
      expect(attributes.status_name).toEqual('Okay')
      expect(attributes).toHaveProperty('model')
      expect(attributes.model).toEqual('0815')
      expect(attributes).toHaveProperty('persistent_identifier')
      expect(attributes.persistent_identifier).toEqual('doi:4354545')
      expect(attributes).toHaveProperty('website')
      expect(attributes.website).toEqual('http://gfz-potsdam.de')
      // expect(attributes).toHaveProperty('created_at')
      // expect(attributes.created_at).toEqual('2020-08-28T13:49:48.015620+00:00')
      // I wasn't able to find the exact date time format, so we use ISO date times
      // expect(attributes.created_at).toEqual('2020-08-28T13:49:48.015Z')
      // expect(attributes).toHaveProperty('updated_at')
      // expect(attributes.updated_at).toEqual('2020-08-30T13:49:48.015620+00:00')
      // again, iso date times
      // expect(attributes.updated_at).toEqual('2020-08-30T13:49:48.015Z')

      expect(jsonApiData.relationships).toHaveProperty('platform_attachments')
      const attachments = jsonApiData.relationships.platform_attachments as IJsonApiTypeIdDataList
      expect(attachments).toHaveProperty('data')
      const attachmentData = attachments.data
      expect(Array.isArray(attachmentData)).toBeTruthy()
      expect(attachmentData.length).toEqual(1)
      expect(attachmentData[0]).toEqual({
        id: '2',
        type: 'platform_attachment'
      })

      expect(jsonApiData).toHaveProperty('relationships')
      expect(typeof jsonApiData.relationships).toEqual('object')
      expect(jsonApiData.relationships).toHaveProperty('contacts')
      expect(typeof jsonApiData.relationships.contacts).toBe('object')
      // we test for the inner structure of the result anyway
      // this cast is just to tell typescript that
      // we have an array of data, so that it doesn't show
      // typeerrors here
      const contactObject = jsonApiData.relationships.contacts as IJsonApiTypeIdDataList
      expect(contactObject).toHaveProperty('data')
      const contactData = contactObject.data
      expect(Array.isArray(contactData)).toBeTruthy()
      expect(contactData.length).toEqual(2)
      expect(contactData[0]).toEqual({
        id: '4',
        type: 'contact'
      })
      expect(contactData[1]).toEqual({
        id: '5',
        type: 'contact'
      })
    })
    it('should serialize an empty string as persistent identifier as null', () => {
      const platform = createTestPlatform()
      platform.persistentIdentifier = ''

      const serializer = new PlatformSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(platform)

      expect(typeof jsonApiData).toEqual('object')
      expect(jsonApiData).toHaveProperty('attributes')
      const attributes = jsonApiData.attributes
      expect(typeof attributes).toBe('object')
      expect(attributes).toHaveProperty('persistent_identifier')
      expect(attributes.persistent_identifier).toBeNull()
    })
    it('should set an id if given for the platform', () => {
      const platform = createTestPlatform()
      platform.id = 'abc'

      const serializer = new PlatformSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(platform)

      expect(typeof jsonApiData).toEqual('object')
      expect(jsonApiData).toHaveProperty('id')
      expect(jsonApiData.id).toEqual('abc')
    })
  })
})
describe('platformWithMetaToPlatformByThrowingErrorOnMissing', () => {
  it('should work without missing data', () => {
    const platform = new Platform()
    const missing = {
      contacts: {
        ids: []
      }
    }

    const result = platformWithMetaToPlatformByThrowingErrorOnMissing({
      platform,
      missing
    })

    expect(result).toEqual(platform)
    expect(result.contacts).toEqual([])
  })
  it('should also work if there is an contact', () => {
    const platform = new Platform()
    const contact = Contact.createFromObject({
      id: '1',
      familyName: 'Mustermann',
      givenName: 'Max',
      website: '',
      email: 'max@mustermann.de'
    })
    platform.contacts.push(contact)

    const missing = {
      contacts: {
        ids: []
      }
    }

    const result = platformWithMetaToPlatformByThrowingErrorOnMissing({
      platform,
      missing
    })

    expect(result).toEqual(platform)
    expect(result.contacts).toEqual([contact])
  })
  it('should throw an error if there are missing data', () => {
    const platform = new Platform()
    const missing = {
      contacts: {
        ids: ['1']
      }
    }

    try {
      platformWithMetaToPlatformByThrowingErrorOnMissing({
        platform,
        missing
      })
      fail('There must be an error')
    } catch (error) {
      expect(error.toString()).toMatch(/Contacts are missing/)
    }
  })
})
describe('platformWithMetaToPlatformByAddingDummyObjects', () => {
  it('should leave the data as it is if there are no missing data', () => {
    const platform = new Platform()
    const missing = {
      contacts: {
        ids: []
      }
    }

    const result = platformWithMetaToPlatformByAddingDummyObjects({
      platform,
      missing
    })

    expect(result).toEqual(platform)
    expect(result.contacts).toEqual([])
  })
  it('should stay with existing contacts without adding dummy data', () => {
    const platform = new Platform()
    const contact = Contact.createFromObject({
      id: '1',
      familyName: 'Mustermann',
      givenName: 'Max',
      website: '',
      email: 'max@mustermann.de'
    })
    platform.contacts.push(contact)
    const missing = {
      contacts: {
        ids: []
      }
    }

    const result = platformWithMetaToPlatformByAddingDummyObjects({
      platform,
      missing
    })

    expect(result).toEqual(platform)
    expect(result.contacts).toEqual([contact])
  })
  it('should add a dummy contact if there are missing data', () => {
    const platform = new Platform()

    const missing = {
      contacts: {
        ids: ['2']
      }
    }

    const newExpectedContact = new Contact()
    newExpectedContact.id = '2'

    const result = platformWithMetaToPlatformByAddingDummyObjects({
      platform,
      missing
    })

    expect(result.contacts).toEqual([newExpectedContact])
  })
  it('should also add a dummy contact if there are contact data - together with the missing', () => {
    const platform = new Platform()
    const contact = Contact.createFromObject({
      id: '1',
      familyName: 'Mustermann',
      givenName: 'Max',
      website: '',
      email: 'max@mustermann.de'
    })
    platform.contacts.push(contact)

    const missing = {
      contacts: {
        ids: ['2']
      }
    }

    const newExpectedContact = new Contact()
    newExpectedContact.id = '2'

    const result = platformWithMetaToPlatformByAddingDummyObjects({
      platform,
      missing
    })

    expect(result.contacts).toEqual([contact, newExpectedContact])
  })
})
