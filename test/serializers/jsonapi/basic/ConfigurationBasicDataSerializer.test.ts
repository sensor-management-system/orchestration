/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2022
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
      expectedConfiguration.status = 'draft'
      expectedConfiguration.archived = true

      const serializer = new ConfigurationBasicDataSerializer()
      const configuration = serializer.convertJsonApiDataToModel(jsonApiData)

      expect(configuration).toEqual(expectedConfiguration)
    })
  })
})
