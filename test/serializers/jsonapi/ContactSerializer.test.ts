import Contact from '@/models/Contact'
import ContactSerializer from '@/serializers/jsonapi/ContactSerializer'

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
})
