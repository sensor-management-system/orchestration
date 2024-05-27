/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'

import { ConfigurationBasicData } from '@/models/basic/ConfigurationBasicData'

import {
  ConfigurationBasicDataSerializer
} from '@/serializers/jsonapi/basic/ConfigurationBasicDataSerializer'

describe('ConfigurationBasicDataSerializer', () => {
  describe('#convertJsonApiDataToModel', () => {
    it('should convert a json api data to a configuration model', () => {
      const jsonApiData: any = {
        attributes: {
          start_date: '2020-08-28T13:49:48.015620+00:00',
          end_date: '2020-08-29T13:49:48.015620+00:00',
          label: 'Tereno NO Boeken',
          description: 'Boeken station',
          project: 'Tereno NO',
          status: 'draft',
          archived: true
        },
        id: '1'
      }

      const expectedConfiguration = new ConfigurationBasicData()
      expectedConfiguration.id = '1'
      expectedConfiguration.startDate = DateTime.utc(2020, 8, 28, 13, 49, 48, 15)
      expectedConfiguration.endDate = DateTime.utc(2020, 8, 29, 13, 49, 48, 15)
      expectedConfiguration.label = 'Tereno NO Boeken'
      expectedConfiguration.description = 'Boeken station'
      expectedConfiguration.project = 'Tereno NO'
      expectedConfiguration.status = 'draft'
      expectedConfiguration.archived = true

      const serializer = new ConfigurationBasicDataSerializer()
      const configuration = serializer.convertJsonApiDataToModel(jsonApiData)

      expect(configuration).toEqual(expectedConfiguration)
    })
  })
})
