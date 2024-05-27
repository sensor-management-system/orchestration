/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'
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
            is_export_control: true,
            member: ['123', '456'],
            admin: ['789'],
            terms_of_use_agreement_date: null
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
        isExportControl: true,
        member: ['123', '456'],
        admin: ['789'],
        contactId: '1234',
        termsOfUseAgreementDate: null
      })

      const serializer = new UserInfoSerializer()

      const userinfo = serializer.convertJsonApiDataToModel(jsonApiObject.data)

      expect(userinfo).toEqual(expectedResult)
    })
    it('should should also parse a date for agreement', () => {
      const jsonApiObject: any = {
        data: {
          attributes: {
            active: true,
            is_superuser: false,
            is_export_control: false,
            member: ['123', '456'],
            admin: ['789'],
            terms_of_use_agreement_date: '2023-02-28T16:15:14+00:00'
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
        isExportControl: false,
        member: ['123', '456'],
        admin: ['789'],
        contactId: '1234',
        termsOfUseAgreementDate: DateTime.utc(2023, 2, 28, 16, 15, 14)
      })

      const serializer = new UserInfoSerializer()

      const userinfo = serializer.convertJsonApiDataToModel(jsonApiObject.data)

      expect(userinfo).toEqual(expectedResult)
    })
  })
})
