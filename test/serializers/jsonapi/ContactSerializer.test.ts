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
import Contact from '@/models/Contact'
import { ContactSerializer } from '@/serializers/jsonapi/ContactSerializer'

describe('ContactSerializer', () => {
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
            family_name: 'Mustermann'
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

      const serializer = new ContactSerializer()

      const relationships = serializer.convertModelListToJsonApiRelationshipObject(contacts)

      expect(typeof relationships).toEqual('object')
      expect(relationships).toHaveProperty('contacts')
      expect(typeof relationships.contacts).toBe('object')
      expect(relationships.contacts).toHaveProperty('data')
      const contactData = relationships.contacts.data
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
          website: ''
        }
      }, {
        type: 'contact',
        id: '3',
        attributes: {
          given_name: 'AA',
          family_name: 'BB',
          email: 'AA@BB',
          website: ''
        }
      }]

      const expectedContact = Contact.createFromObject({
        id: '1',
        givenName: 'AA',
        familyName: 'BB',
        email: 'AA@BB',
        website: ''
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
