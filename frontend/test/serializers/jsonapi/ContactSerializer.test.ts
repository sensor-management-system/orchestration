/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'

import { Contact } from '@/models/Contact'
import { ContactSerializer } from '@/serializers/jsonapi/ContactSerializer'
import { IJsonApiEntityWithoutDetailsDataDictList } from '@/serializers/jsonapi/JsonApiTypes'

describe('ContactSerializer', () => {
  describe('#convertModelToJsonApiData', () => {
    it('should set the orcid to null of not present', () => {
      const contact = Contact.createFromObject({
        id: '',
        givenName: 'Humer',
        familyName: 'Symben',
        email: 'humer@symbsen.org',
        organization: 'Spynkfylt Nuclear',
        orcid: '',
        website: '',
        createdAt: DateTime.utc(2022, 12, 24, 12, 0, 0),
        updatedAt: DateTime.utc(2022, 12, 25, 5, 0, 0),
        createdByUserId: '123'
      })
      const serializer = new ContactSerializer()
      const payload = serializer.convertModelToJsonApiData(contact)

      expect(payload.attributes?.orcid).toBeNull()
    })
    it('should use the orcid if present', () => {
      const contact = Contact.createFromObject({
        id: '',
        givenName: 'Humer',
        familyName: 'Symben',
        email: 'humer@symbsen.org',
        organization: 'Spynkfylt Nuclear',
        orcid: 'abc',
        website: '',
        createdAt: DateTime.utc(2022, 12, 24, 12, 0, 0),
        updatedAt: DateTime.utc(2022, 12, 25, 5, 0, 0),
        createdByUserId: '123'
      })
      const serializer = new ContactSerializer()
      const payload = serializer.convertModelToJsonApiData(contact)

      expect(payload.attributes?.orcid).toEqual('abc')
    })
  })
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a json api object with multiple entries to a contact model list', () => {
      const jsonApiObjectList: any = {
        data: [{
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
            family_name: 'Mustermann',
            organization: null,
            orcid: null
          },
          id: '1',
          links: {
            self: '/rdm/svm-api/v1/contacts/1'
          }
        }],
        links: {
          self: 'http://rz-vm64.gfz-potsdam.de:5000/rdm/svm-api/v1/contacts'
        },
        meta: {
          count: 1
        },
        jsonapi: {
          version: '1.0'
        }
      }

      const expectedContact = new Contact()
      expectedContact.id = '1'
      expectedContact.givenName = 'Max'
      expectedContact.familyName = 'Mustermann'
      expectedContact.website = ''
      expectedContact.email = 'test@test.test'
      expectedContact.organization = ''
      expectedContact.orcid = ''

      const serializer = new ContactSerializer()
      const contacts = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(contacts)).toBeTruthy()
      expect(contacts.length).toEqual(1)
      expect(contacts[0]).toEqual(expectedContact)
    })
  })
  describe('#convertJsonApiObjectToModel', () => {
    it('should convert a single json api object to a contact model', () => {
      const jsonApiObject: any = {
        data: {
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
            },
            created_by: {
              data: {
                type: 'user',
                id: '123'
              }
            }
          },
          attributes: {
            given_name: 'Max',
            email: 'test@test.test',
            website: null,
            family_name: 'Mustermann',
            organization: 'Muster',
            orcid: '0000-0000-0000-0001',
            created_at: '2020-08-29T13:49:48.015620+00:00',
            updated_at: '2021-08-29T13:49:48.015620+00:00'
          },
          id: '1',
          links: {
            self: '/rdm/svm-api/v1/contacts/1'
          }
        },
        links: {
          self: '/rdm/svm-api/v1/contacts/1'
        },
        jsonapi: {
          version: '1.0'
        }
      }

      const expectedContact = new Contact()
      expectedContact.id = '1'
      expectedContact.givenName = 'Max'
      expectedContact.familyName = 'Mustermann'
      expectedContact.website = ''
      expectedContact.email = 'test@test.test'
      expectedContact.organization = 'Muster'
      expectedContact.orcid = '0000-0000-0000-0001'
      expectedContact.createdAt = DateTime.utc(2020, 8, 29, 13, 49, 48, 15)
      expectedContact.updatedAt = DateTime.utc(2021, 8, 29, 13, 49, 48, 15)
      expectedContact.createdByUserId = '123'

      const serializer = new ContactSerializer()
      const contact = serializer.convertJsonApiObjectToModel(jsonApiObject)

      expect(contact).toEqual(expectedContact)
    })
  })
  describe('#convertJsonApiDataToModel', () => {
    it('should convert a single json api data object to a contact model', () => {
      // it is basically the very same as the test for the whole json api object
      // but this time we only give the content that is in the data sub-object
      // of the convertJsonApiObjectToModel test.
      const jsonApiData: any = {
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
          organization: null,
          orcid: null,
          family_name: 'Mustermann'
        },
        id: '1',
        links: {
          self: '/rdm/svm-api/v1/contacts/1'
        }
      }

      const expectedContact = new Contact()
      expectedContact.id = '1'
      expectedContact.givenName = 'Max'
      expectedContact.familyName = 'Mustermann'
      expectedContact.website = ''
      expectedContact.email = 'test@test.test'
      expectedContact.organization = ''
      expectedContact.orcid = ''

      const serializer = new ContactSerializer()
      const contact = serializer.convertJsonApiDataToModel(jsonApiData)

      expect(contact).toEqual(expectedContact)
    })
  })
  describe('#convertModelListToJsonApiRelationshipObject', () => {
    it('should convert a list of contacts to a relationship object with ids', () => {
      const contacts = [
        Contact.createFromObject({
          id: '4',
          givenName: 'Max',
          familyName: 'Mustermann',
          email: 'max@mustermann.de',
          website: '',
          organization: '',
          orcid: '',
          createdAt: null,
          updatedAt: null,
          createdByUserId: null
        }),
        Contact.createFromObject({
          id: '5',
          givenName: 'Mux',
          familyName: 'Mastermunn',
          email: 'mux@mastermunn.de',
          website: '',
          organization: 'Muster',
          orcid: '0000-0000-0000-0001',
          createdAt: null,
          updatedAt: null,
          createdByUserId: null
        })
      ]

      const serializer = new ContactSerializer()

      const relationships = serializer.convertModelListToJsonApiRelationshipObject(contacts)

      expect(typeof relationships).toEqual('object')
      expect(relationships).toHaveProperty('contacts')
      expect(typeof relationships.contacts).toBe('object')
      // we test for the inner structure of the result anyway
      // this cast is just to tell typescript that
      // we have an array of data, so that it doesn't show
      // typeerrors here
      const contactObject = relationships.contacts as IJsonApiEntityWithoutDetailsDataDictList
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
  })
  describe('#convertJsonApiRelationshipsModelList', () => {
    it('should construct a list of contacts - and store missing ids', () => {
      const relationships = {
        contacts: {
          links: {
            related: '/foo'
          },
          data: [{
            id: '1',
            type: 'contact'
          }, {
            id: '2',
            type: 'contact'
          }]
        }
      }

      const included = [{
        type: 'contact',
        id: '1',
        attributes: {
          given_name: 'AA',
          family_name: 'BB',
          email: 'AA@BB',
          website: '',
          organization: 'CC',
          orcid: '0000-0000-0000-0001'
        }
      }, {
        type: 'contact',
        id: '3',
        attributes: {
          given_name: 'AA',
          family_name: 'BB',
          email: 'AA@BB',
          website: '',
          organization: '',
          orcid: null
        }
      }]

      const expectedContact = Contact.createFromObject({
        id: '1',
        givenName: 'AA',
        familyName: 'BB',
        email: 'AA@BB',
        website: '',
        organization: 'CC',
        orcid: '0000-0000-0000-0001',
        createdAt: null,
        updatedAt: null,
        createdByUserId: null
      })

      const serializer = new ContactSerializer()
      const contactsWithMissing = serializer.convertJsonApiRelationshipsModelList(relationships, included)
      const contacts = contactsWithMissing.contacts

      expect(Array.isArray(contacts)).toBeTruthy()
      expect(contacts.length).toEqual(1)
      expect(contacts[0]).toEqual(expectedContact)

      const missingIds = contactsWithMissing.missing.ids
      expect(Array.isArray(missingIds)).toBeTruthy()
      expect(missingIds.length).toEqual(1)
      expect(missingIds[0]).toEqual('2')
    })
  })
})
