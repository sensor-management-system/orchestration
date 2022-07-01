/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
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
import { CvContactRole } from '@/models/CvContactRole'
import { CvContactRoleSerializer } from '@/serializers/jsonapi/CvContactRoleSerializer'

describe('CvContactRoleSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            term: 'PI',
            definition: 'yada yada yada',
            provenance: null,
            provenance_uri: null,
            category: null,
            note: null,
            status: 'ACCEPTED'
          },
          id: '6',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/contactroles/6/'
          },
          relationships: {},
          type: 'ContactRole'
        }, {
          attributes: {
            term: 'Technical Coordinator',
            definition: 'A technical coordinator that does something...',
            provenance: null,
            provenance_uri: null,
            category: null,
            note: null,
            status: 'ACCEPTED'
          },
          id: '7',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/contactroles/7/'
          },
          relationships: {},
          type: 'ContactRole'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedContactRole1 = CvContactRole.createFromObject({
        id: '6',
        name: 'PI',
        definition: 'yada yada yada',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/contactroles/6/'
      })
      const expectedContactRole2 = CvContactRole.createFromObject({
        id: '7',
        name: 'Technical Coordinator',
        definition: 'A technical coordinator that does something...',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/contactroles/7/'
      })

      const serializer = new CvContactRoleSerializer()

      const contactRoles = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(contactRoles)).toBeTruthy()
      expect(contactRoles.length).toEqual(2)
      expect(contactRoles[0]).toEqual(expectedContactRole1)
      expect(contactRoles[1]).toEqual(expectedContactRole2)
    })
  })
})
