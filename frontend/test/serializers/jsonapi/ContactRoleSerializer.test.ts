/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2022-2023
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
import { Contact } from '@/models/Contact'
import { ContactRole } from '@/models/ContactRole'
import { ContactRoleSerializer } from '@/serializers/jsonapi/ContactRoleSerializer'

describe('ContactRoleSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a json api object with multiple entries to a list of contact roles', () => {
      const jsonApiObjectList: any = {
        data: [{
          type: 'device_contact_role',
          relationships: {
            contact: {
              data: {
                type: 'contact',
                id: '1'
              }
            },
            device: {
              data: {
                type: 'device',
                id: '2'
              }
            }
          },
          attributes: {
            role_name: 'Technical Coordinator',
            role_uri: 'https://sensors.gfz-potsdam.de/cv/api/v1/contactroles/7'
          },
          id: '1'
        }, {
          type: 'device_contact_role',
          relationships: {
            contact: {
              data: {
                type: 'contact',
                id: '3'
              }
            },
            device: {
              data: {
                type: 'device',
                id: '4'
              }
            }
          },
          attributes: {
            role_name: 'PI',
            role_uri: 'https://sensors.gfz-potsdam.de/cv/api/v1/contactroles/6'
          },
          id: '2'
        }],
        included: [{
          attributes: {
            given_name: 'Max',
            email: 'test@test.test',
            website: null,
            family_name: 'Mustermann'
          },
          id: '1',
          type: 'contact'
        }, {
          attributes: {
            given_name: 'Erika',
            email: 'test2@test.test',
            website: null,
            family_name: 'Mustermann'
          },
          id: '3',
          type: 'contact'
        }],
        meta: {
          count: 1
        },
        jsonapi: {
          version: '1.0'
        }
      }

      const expectedContactRole1 = ContactRole.createFromObject({
        id: '1',
        roleName: 'Technical Coordinator',
        roleUri: 'https://sensors.gfz-potsdam.de/cv/api/v1/contactroles/7',
        contact: Contact.createFromObject({
          id: '1',
          givenName: 'Max',
          familyName: 'Mustermann',
          website: '',
          email: 'test@test.test',
          organization: '',
          orcid: '',
          createdByUserId: null,
          createdAt: null,
          updatedAt: null
        })
      })
      const expectedContactRole2 = ContactRole.createFromObject({
        id: '2',
        roleName: 'PI',
        roleUri: 'https://sensors.gfz-potsdam.de/cv/api/v1/contactroles/6',
        contact: Contact.createFromObject({
          id: '3',
          givenName: 'Erika',
          familyName: 'Mustermann',
          website: '',
          organization: '',
          orcid: '',
          email: 'test2@test.test',
          createdByUserId: null,
          createdAt: null,
          updatedAt: null
        })
      })

      const serializer = new ContactRoleSerializer()
      const contactRoles = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(contactRoles)).toBeTruthy()
      expect(contactRoles.length).toEqual(2)
      expect(contactRoles[0]).toEqual(expectedContactRole1)
      expect(contactRoles[1]).toEqual(expectedContactRole2)
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should prepare the payload for the server', () => {
      const contactRole = ContactRole.createFromObject({
        id: '1',
        roleName: 'Technical Coordinator',
        roleUri: 'https://sensors.gfz-potsdam.de/cv/api/v1/contactroles/7',
        contact: Contact.createFromObject({
          id: '2',
          givenName: 'Max',
          familyName: 'Mustermann',
          website: '',
          organization: '',
          email: 'test@test.test',
          orcid: '',
          createdByUserId: null,
          createdAt: null,
          updatedAt: null
        })
      })

      const serializer = new ContactRoleSerializer()

      const output = serializer.convertModelToJsonApiData(contactRole, 'device_contact_role', 'device', '55')

      const expectedOutput = {
        type: 'device_contact_role',
        attributes: {
          role_uri: 'https://sensors.gfz-potsdam.de/cv/api/v1/contactroles/7',
          role_name: 'Technical Coordinator'
        },
        relationships: {
          contact: {
            data: {
              type: 'contact',
              id: '2'
            }
          },
          device: {
            data: {
              type: 'device',
              id: '55'
            }
          }
        }
      }

      expect(expectedOutput).toEqual(output)
    })
  })
})
