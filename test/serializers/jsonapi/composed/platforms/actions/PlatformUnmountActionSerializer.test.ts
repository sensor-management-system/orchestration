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
import { ContactBasicData } from '@/models/basic/ContactBasicData'
import { ConfigurationBasicData } from '@/models/basic/ConfigurationBasicData'
import { PlatformUnmountActionBasicData } from '@/models/basic/PlatformUnmountActionBasicData'
import { PlatformUnmountAction } from '@/models/views/platforms/actions/PlatformUnmountAction'
import { PlatformUnmountActionSerializer } from '@/serializers/jsonapi/composed/platforms/actions/PlatformUnmountActionSerializer'
import { IJsonApiEntityListEnvelope } from '@/serializers/jsonapi/JsonApiTypes'

describe('PlatformUnmountActionSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a json api payload to a platform unmount action list', () => {
      const jsonApiObject: IJsonApiEntityListEnvelope = {
        data: [
          {
            type: 'platform_unmount_action',
            id: 'pu1',
            attributes: {
              description: 'Platform unmount',
              end_date: '2020-01-01T12:00:00.000Z'
            },
            relationships: {
              contact: {
                data: {
                  type: 'contact',
                  id: 'ct1'
                }
              },
              configuration: {
                data: {
                  type: 'configuration',
                  id: 'cf1'
                }
              }
            }
          },
          {
            type: 'platform_unmount_action',
            id: 'pu2',
            attributes: {
              description: 'Platform unmount II',
              end_date: '2020-03-01T12:00:00.000Z'
            },
            relationships: {
              contact: {
                data: {
                  type: 'contact',
                  id: 'ct2'
                }
              },
              configuration: {
                data: {
                  type: 'configuration',
                  id: 'cf1'
                }
              }
            }
          }
        ],
        included: [
          {
            type: 'configuration',
            id: 'cf1',
            attributes: {
              start_date: '2020-08-28T13:49:48.015620+00:00',
              end_date: '2020-08-29T13:49:48.015620+00:00',
              project_uri: 'projects/Tereno-NO',
              project_name: 'Tereno NO',
              label: 'Tereno NO Boeken',
              status: 'draft'
            }
          },
          {
            type: 'contact',
            id: 'ct1',
            attributes: {
              given_name: 'Max',
              email: 'test@test.test',
              website: null,
              family_name: 'Mustermann'
            }
          },
          {
            type: 'contact',
            id: 'ct2',
            attributes: {
              given_name: 'Mux',
              email: 'foo@bar.test',
              website: null,
              family_name: 'Mastermann'
            }
          }
        ]
      }

      const expectedCt1 = ContactBasicData.createFromObject({
        id: 'ct1',
        givenName: 'Max',
        familyName: 'Mustermann',
        website: '',
        email: 'test@test.test'
      })
      const expectedCt2 = ContactBasicData.createFromObject({
        id: 'ct2',
        givenName: 'Mux',
        familyName: 'Mastermann',
        website: '',
        email: 'foo@bar.test'
      })

      const expectedCf1 = ConfigurationBasicData.createFromObject({
        id: 'cf1',
        startDate: DateTime.utc(2020, 8, 28, 13, 49, 48, 15),
        endDate: DateTime.utc(2020, 8, 29, 13, 49, 48, 15),
        projectUri: 'projects/Tereno-NO',
        projectName: 'Tereno NO',
        label: 'Tereno NO Boeken',
        status: 'draft'
      })

      const expectedPu1 = PlatformUnmountActionBasicData.createFromObject({
        id: 'pu1',
        date: DateTime.utc(2020, 1, 1, 12, 0, 0),
        description: 'Platform unmount'
      })

      const expectedPu2 = PlatformUnmountActionBasicData.createFromObject({
        id: 'pu2',
        date: DateTime.utc(2020, 3, 1, 12, 0, 0),
        description: 'Platform unmount II'
      })

      const expectedResult = [
        new PlatformUnmountAction(
          expectedPu1, expectedCf1, expectedCt1
        ),
        new PlatformUnmountAction(
          expectedPu2, expectedCf1, expectedCt2
        )
      ]

      const serializer = new PlatformUnmountActionSerializer()
      const result = serializer.convertJsonApiObjectListToModelList(jsonApiObject)

      expect(result).toEqual(expectedResult)
    })
  })
})
