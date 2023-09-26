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
import { ActionCategory } from '@/models/ActionCategory'
import { ActionCategorySerializer } from '@/serializers/jsonapi/ActionCategorySerializer'

describe('ActionCategorySerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            term: 'Device',
            status: 'ACCEPTED'
          },
          id: '8',
          type: 'ActionCategory'
        }, {
          attributes: {
            term: 'Platform',
            status: 'ACCEPTED'
          },
          id: '9',
          type: 'ActionCategory'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedActionCatgory1 = ActionCategory.createFromObject({
        id: '8',
        name: 'Device'
      })
      const expectedActionCatgory2 = ActionCategory.createFromObject({
        id: '9',
        name: 'Platform'
      })

      const serializer = new ActionCategorySerializer()

      const actioncategories = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(actioncategories)).toBeTruthy()
      expect(actioncategories.length).toEqual(2)
      expect(actioncategories[0]).toEqual(expectedActionCatgory1)
      expect(actioncategories[1]).toEqual(expectedActionCatgory2)
    })
  })
})
