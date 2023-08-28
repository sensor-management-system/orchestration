/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
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
