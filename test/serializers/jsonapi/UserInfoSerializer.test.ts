/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2022
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
import { UserInfo } from '@/models/UserInfo'
import { UserInfoSerializer } from '@/serializers/jsonapi/UserInfoSerializer'

describe('UserInfoSerializer', () => {
  describe('#convertJsonApiDataToModel', () => {
    it('should convert an entry to the model', () => {
      const jsonApiObject: any = {
        data: {
          attributes: {
            active: true,
            is_superuser: false,
            member: ['123', '456'],
            admin: ['789']
          },
          id: '1',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/units/1/'
          },
          relationships: {
            contact: {
              data: {
                type: 'contact',
                id: 1234
              }
            }
          },
          type: 'user'
        },
        included: []
      }

      const expectedResult = UserInfo.createFromObject({
        id: '1',
        active: true,
        isSuperUser: false,
        member: ['123', '456'],
        admin: ['789'],
        contactId: '1234'
      })

      const serializer = new UserInfoSerializer()

      const userinfo = serializer.convertJsonApiDataToModel(jsonApiObject.data)

      expect(userinfo).toEqual(expectedResult)
    })
  })
})
