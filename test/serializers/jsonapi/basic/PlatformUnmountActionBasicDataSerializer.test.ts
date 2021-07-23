/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2021
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

import { PlatformUnmountActionBasicData } from '@/models/basic/PlatformUnmountActionBasicData'

import { PlatformUnmountActionBasicDataSerializer } from '@/serializers/jsonapi/basic/PlatformUnmountActionBasicDataSerializer'

const date = DateTime.utc(2020, 1, 1, 12, 0, 0)

describe('PlatformUnmountActionBasicDataSerializer', () => {
  describe('#convertJsonApiDataToModel', () => {
    it('should covnert a single json api data object to a platform unmount action', () => {
      const jsonApiData: any = {
        type: 'platform_unmount_action',
        attributes: {
          description: 'Platform unmount',
          end_date: '2020-01-01T12:00:00.000Z'
        },
        id: '1'
      }

      const expectedPlatformUnmountAction = PlatformUnmountActionBasicData.createFromObject({
        id: '1',
        date,
        description: 'Platform unmount'
      })

      const serializer = new PlatformUnmountActionBasicDataSerializer()
      const platformUnmountAction = serializer.convertJsonApiDataToModel(jsonApiData)

      expect(platformUnmountAction).toEqual(expectedPlatformUnmountAction)
    })
  })
})
