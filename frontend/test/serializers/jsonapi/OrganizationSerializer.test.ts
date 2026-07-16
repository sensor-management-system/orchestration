/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * - Nils Brinckmann <nils.brinckmann@gfz.de>
 * - GFZ Helmholtz for Geosciences (GFZ, https://www.gfz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { Organization } from '@/models/Organization'
import { OrganizationSerializer } from '@/serializers/jsonapi/OrganizationSerializer'

describe('OrganizationSerializer', () => {
  describe('#convertJsonApiObjectToModel', () => {
    it('should transform all attributes for the organization', () => {
      const data = {
        data: {
          id: '1',
          type: 'organization',
          attributes: {
            name: 'GFZ Helmholtz Centre for Geosciences',
            ror: 'https://ror.org/04z8jg394',
            abbreviation: 'GFZ'
          }
        }
      }
      const result = new OrganizationSerializer().convertJsonApiObjectToModel(data)
      const expectedResult = Organization.createFromObject({
        id: '1',
        name: 'GFZ Helmholtz Centre for Geosciences',
        ror: 'https://ror.org/04z8jg394',
        abbreviation: 'GFZ'
      })
      expect(result).toEqual(expectedResult)
    })
    it('should work with minimal information', () => {
      const data = {
        data: {
          id: '1',
          type: 'organization',
          attributes: {
            name: 'G',
            ror: null,
            abbreviation: null
          }
        }
      }
      const result = new OrganizationSerializer().convertJsonApiObjectToModel(data)
      const expectedResult = Organization.createFromObject({
        id: '1',
        name: 'G',
        ror: '',
        abbreviation: ''
      })
      expect(result).toEqual(expectedResult)
    })
  })
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should transform a list', () => {
      const data = {
        data: [
          {
            id: '1',
            type: 'organization',
            attributes: {
              name: 'GFZ Helmholtz Centre for Geosciences',
              ror: 'https://ror.org/04z8jg394',
              abbreviation: 'GFZ'
            }
          },
          {
            id: '2',
            type: 'organization',
            attributes: {
              name: 'G',
              ror: null,
              abbreviation: null
            }
          }
        ]
      }
      const result = new OrganizationSerializer().convertJsonApiObjectListToModelList(data)
      const expectedResult1 = Organization.createFromObject({
        id: '1',
        name: 'GFZ Helmholtz Centre for Geosciences',
        ror: 'https://ror.org/04z8jg394',
        abbreviation: 'GFZ'
      })
      const expectedResult2 = Organization.createFromObject({
        id: '2',
        name: 'G',
        ror: '',
        abbreviation: ''
      })
      const expectedResult = [expectedResult1, expectedResult2]
      expect(result).toEqual(expectedResult)
    })
  })
  describe('convertModelToJsonApiData', () => {
    it('should transform a full set of organization data', () => {
      const organization = Organization.createFromObject({
        id: '1',
        name: 'GFZ Helmholtz Centre for Geosciences',
        ror: 'https://ror.org/04z8jg394',
        abbreviation: 'GFZ'
      })
      const result = new OrganizationSerializer().convertModelToJsonApiData(organization)
      const expectedResult = {
        id: '1',
        type: 'organization',
        attributes: {
          name: 'GFZ Helmholtz Centre for Geosciences',
          ror: 'https://ror.org/04z8jg394',
          abbreviation: 'GFZ'
        }
      }
      expect(result).toEqual(expectedResult)
    })
    it('should also work with a minimal set of data', () => {
      const organization = Organization.createFromObject({
        id: '',
        name: 'G',
        ror: '',
        abbreviation: ''
      })
      const result = new OrganizationSerializer().convertModelToJsonApiData(organization)
      const expectedResult = {
        type: 'organization',
        attributes: {
          name: 'G',
          ror: '',
          abbreviation: ''
        }
      }
      expect(result).toEqual(expectedResult)
    })
  })
})
