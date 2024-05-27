/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { GlobalProvenance } from '@/models/GlobalProvenance'
import { GlobalProvenanceSerializer } from '@/serializers/jsonapi/GlobalProvenanceSerializer'

describe('GlobalProvenanceSerializer', () => {
  describe('convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            name: 'SensorML',
            description: 'SensorML provenance'
          },
          id: '1',
          relationships: {},
          type: 'GlobalProvenance'
        }, {
          attributes: {
            name: 'NERC',
            description: ''
          },
          id: '2',
          relationships: {},
          type: 'GlobalProvenance'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedGlobalProvenance1 = GlobalProvenance.createFromObject({
        id: '1',
        name: 'SensorML',
        description: 'SensorML provenance'
      })
      const expectedGlobalProvenance2 = GlobalProvenance.createFromObject({
        id: '2',
        name: 'NERC',
        description: ''
      })

      const serializer = new GlobalProvenanceSerializer()

      const globalProvenances = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(globalProvenances)).toBeTruthy()
      expect(globalProvenances.length).toEqual(2)
      expect(globalProvenances[0]).toEqual(expectedGlobalProvenance1)
      expect(globalProvenances[1]).toEqual(expectedGlobalProvenance2)
    })
  })
})
