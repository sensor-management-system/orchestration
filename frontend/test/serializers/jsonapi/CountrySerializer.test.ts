/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2023 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { Country } from '@/models/Country'
import { CountrySerializer } from '@/serializers/jsonapi/CountrySerializer'

describe('CountrySerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [
          {
            id: '1',
            type: 'Country',
            attributes: {
              term: 'Albania'
            }
          },
          {
            id: '2',
            type: 'Country',
            attributes: {
              term: 'France'
            }
          }
        ]
      }

      const expectedCountry1 = Country.createFromObject({
        id: '1',
        name: 'Albania'
      })
      const expectedCountry2 = Country.createFromObject({
        id: '2',
        name: 'France'
      })

      const serializer = new CountrySerializer()

      const countries = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(countries)).toBeTruthy()
      expect(countries.length).toEqual(2)
      expect(countries[0]).toEqual(expectedCountry1)
      expect(countries[1]).toEqual(expectedCountry2)
    })
  })
})
