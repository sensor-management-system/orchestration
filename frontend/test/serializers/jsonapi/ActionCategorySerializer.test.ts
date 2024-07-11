/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
