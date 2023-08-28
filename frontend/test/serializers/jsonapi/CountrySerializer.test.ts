/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2023
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
