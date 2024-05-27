/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { ContactBasicData } from '@/models/basic/ContactBasicData'
import { ContactBasicDataSerializer } from '@/serializers/jsonapi/basic/ContactBasicDataSerializer'

describe('ContactBasicDataSerializer', () => {
  describe('#convertJsonApiDataToModel', () => {
    it('should convert a single json api data object to a contact model', () => {
      // it is basically the very same as the test for the whole json api object
      // but this time we only give the content that is in the data sub-object
      // of the convertJsonApiObjectToModel test.
      const jsonApiData: any = {
        type: 'contact',
        attributes: {
          given_name: 'Max',
          email: 'test@test.test',
          website: null,
          organization: null,
          orcid: null,
          family_name: 'Mustermann'
        },
        id: '1'
      }

      const expectedContact = new ContactBasicData()
      expectedContact.id = '1'
      expectedContact.givenName = 'Max'
      expectedContact.familyName = 'Mustermann'
      expectedContact.website = ''
      expectedContact.organization = ''
      expectedContact.orcid = ''
      expectedContact.email = 'test@test.test'

      const serializer = new ContactBasicDataSerializer()
      const contact = serializer.convertJsonApiDataToModel(jsonApiData)

      expect(contact).toEqual(expectedContact)
    })
  })
})
