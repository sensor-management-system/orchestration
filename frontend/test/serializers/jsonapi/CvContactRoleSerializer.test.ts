/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
          relationships: {
            global_provenance: {
              data: null
            }
          },
          type: 'ContactRole'
        }, {
          attributes: {
            term: 'Technical Coordinator',
            definition: 'A technical coordinator that does something...',
            provenance: 'provenance',
            provenance_uri: 'provenanceuri',
            category: 'category',
            note: 'note',
            status: 'ACCEPTED'
          },
          id: '7',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/contactroles/7/'
          },
          relationships: {
            global_provenance: {
              data: {
                id: '1',
                type: 'GlobalProvenance'
              }
            }
          },
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
        provenance: '',
        provenanceUri: '',
        category: '',
        note: '',
        globalProvenanceId: null,
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/contactroles/6/'
      })
      const expectedContactRole2 = CvContactRole.createFromObject({
        id: '7',
        name: 'Technical Coordinator',
        definition: 'A technical coordinator that does something...',
        provenance: 'provenance',
        provenanceUri: 'provenanceuri',
        category: 'category',
        note: 'note',
        globalProvenanceId: '1',
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
  describe('#convertModelToJsonApiData', () => {
    it('should transform the model to json payload', () => {
      const contactRole = CvContactRole.createFromObject({
        id: '7',
        name: 'Technical Coordinator',
        definition: 'A technical coordinator that does something...',
        provenance: 'provenance',
        provenanceUri: 'provenanceuri',
        category: 'category',
        note: 'note',
        globalProvenanceId: '1',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/contactroles/7/'
      })
      const expectedResult = {
        id: '7',
        type: 'ContactRole',
        attributes: {
          term: 'Technical Coordinator',
          category: 'category',
          definition: 'A technical coordinator that does something...',
          provenance: 'provenance',
          provenance_uri: 'provenanceuri',
          note: 'note'
        },
        relationships: {
          global_provenance: {
            data: {
              id: '1',
              type: 'GlobalProvenance'
            }
          }
        }
      }

      const serializer = new CvContactRoleSerializer()
      const result = serializer.convertModelToJsonApiData(contactRole)

      expect(result).toEqual(expectedResult)
    })
  })
})
