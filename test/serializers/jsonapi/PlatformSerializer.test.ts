import Contact from '@/models/Contact'
import Platform from '@/models/Platform'
import {
  Attachment
} from '@/models/Attachment'

import PlatformSerializer from '@/serializers/jsonapi/PlatformSerializer'

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
  platform.createdAt = new Date('2020-08-28T13:49:48.015620+00:00')
  platform.updatedAt = new Date('2020-08-30T13:49:48.015620+00:00')

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
            updated_at: '2020-08-29T13:48:35.740944+00:00',
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
            attachments: [],
            platform_type_uri: 'Station',
            status_uri: null,
            website: null,
            updated_at: null,
            long_name: 'Groundwater level KleinTrebbow',
            created_at: null,
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
        included: [{
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
        }],
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
        label: 'GFZ',
        url: 'http://www.gfz-potsdam.de'
      })]
      expectedPlatform1.platformTypeUri = 'type/Station'
      expectedPlatform1.statusUri = 'status/inuse'
      expectedPlatform1.website = 'http://www.tereno.net'
      expectedPlatform1.updatedAt = new Date('2020-08-29T13:48:35.740944+00:00')
      expectedPlatform1.longName = 'Soil moisture station Boeken BF1, Germany'
      expectedPlatform1.createdAt = new Date('2020-08-28T13:48:35.740944+00:00')
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

      const platforms = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(platforms)).toBeTruthy()
      expect(platforms.length).toEqual(2)

      expect(platforms[0]).toEqual(expectedPlatform1)
      expect(platforms[1]).toEqual(expectedPlatform2)
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
            attachments: [{
              label: 'GFZ',
              url: 'http://www.gfz-potsdam.de',
              id: '12'
            }],
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
        included: [{
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
        }],
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
      expectedPlatform.updatedAt = new Date('2020-08-28T13:48:35.740944+00:00')
      expectedPlatform.longName = 'Soil moisture station Boeken BF1, Germany'
      expectedPlatform.createdAt = new Date('2020-08-28T13:48:35.740944+00:00')
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

      const platform = serializer.convertJsonApiObjectToModel(jsonApiObject)

      expect(platform).toEqual(expectedPlatform)
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
          attachments: [{
            label: 'GFZ',
            url: 'http://www.gfz-potsdam.de',
            id: '12'
          }],
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
      const included = [{
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
      }]

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
      expectedPlatform.updatedAt = new Date('2020-08-28T13:48:35.740944+00:00')
      expectedPlatform.longName = 'Soil moisture station Boeken BF1, Germany'
      expectedPlatform.createdAt = new Date('2020-08-28T13:48:35.740944+00:00')
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

      const platform = serializer.convertJsonApiDataToModel(jsonApiData, included)

      expect(platform).toEqual(expectedPlatform)
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
      expect(attributes).toHaveProperty('created_at')
      // expect(attributes.created_at).toEqual('2020-08-28T13:49:48.015620+00:00')
      // I wasn't able to find the exact date time format, so we use ISO date times
      expect(attributes.created_at).toEqual('2020-08-28T13:49:48.015Z')
      expect(attributes).toHaveProperty('updated_at')
      // expect(attributes.updated_at).toEqual('2020-08-30T13:49:48.015620+00:00')
      // again, iso date times
      expect(attributes.updated_at).toEqual('2020-08-30T13:49:48.015Z')

      expect(attributes).toHaveProperty('attachments')
      const attachments = attributes.attachments
      expect(Array.isArray(attachments)).toBeTruthy()
      expect(attachments.length).toEqual(2)
      expect(attachments[0]).toEqual({
        id: '2',
        label: 'GFZ',
        url: 'http://www.gfz-potsdam.de'
      })
      expect(attachments[1]).toEqual({
        label: 'UFZ',
        url: 'http://www.ufz.de'
      })

      expect(jsonApiData).toHaveProperty('relationships')
      expect(typeof jsonApiData.relationships).toEqual('object')
      expect(jsonApiData.relationships).toHaveProperty('contacts')
      expect(typeof jsonApiData.relationships.contacts).toBe('object')
      expect(jsonApiData.relationships.contacts).toHaveProperty('data')
      const contactData = jsonApiData.relationships.contacts.data
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
    it('should stay with a null createdAt/updatedAt date', () => {
      const platform = createTestPlatform()
      platform.createdAt = null
      platform.updatedAt = null

      const serializer = new PlatformSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(platform)

      expect(typeof jsonApiData).toEqual('object')
      expect(jsonApiData).toHaveProperty('attributes')
      const attributes = jsonApiData.attributes
      expect(typeof attributes).toEqual('object')
      expect(attributes).toHaveProperty('created_at')
      expect(attributes.created_at).toBeNull()
      expect(attributes).toHaveProperty('updated_at')
      expect(attributes.updated_at).toBeNull()
    })
  })
})
