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

import { DateTime } from 'luxon'
import { Contact } from '@/models/Contact'
import { StaticLocationAction } from '@/models/StaticLocationAction'
import { StaticLocationActionSerializer } from '@/serializers/jsonapi/StaticLocationActionSerializer'
import { IJsonApiEntityListEnvelope } from '@/serializers/jsonapi/JsonApiTypes'

describe('StaticLocationActionSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should read the label attribute', () => {
      const payload: IJsonApiEntityListEnvelope = {
        data: [
          {
            id: '1',
            type: 'configuration_static_location_action',
            attributes: {
              begin_date: '2023-02-28T12:13:14+00:00',
              label: 'some example location'
            },
            relationships: {
              begin_contact: {
                data: {
                  id: '123',
                  type: 'contact'
                }
              },
              configuration: {
                data: {
                  id: '124',
                  type: 'configuration'
                }
              }
            }
          }
        ],
        included: [
          {
            id: '123',
            type: 'contact',
            attributes: {
              given_name: 'Max',
              family_name: 'Mustermann',
              email: 'max.mustermann@localhost',
              created_at: '2023-02-26T00:00:00+00:00',
              updated_at: '2023-02-27T00:00:00+00:00'
            }
          }
        ]
      }
      const expectedContact = Contact.createFromObject({
        id: '123',
        givenName: 'Max',
        familyName: 'Mustermann',
        email: 'max.mustermann@localhost',
        orcid: '',
        organization: '',
        website: '',
        createdAt: DateTime.utc(2023, 2, 26, 0, 0, 0),
        updatedAt: DateTime.utc(2023, 2, 27, 0, 0, 0),
        createdByUserId: null
      })
      const expectedAction = StaticLocationAction.createFromObject({
        id: '1',
        beginContact: expectedContact,
        beginDate: DateTime.utc(2023, 2, 28, 12, 13, 14),
        label: 'some example location',
        endDate: null,
        endContact: null,
        x: null,
        y: null,
        z: null,
        epsgCode: '4326',
        elevationDatumName: 'MSL',
        elevationDatumUri: '',
        beginDescription: '',
        endDescription: '',
        configurationId: '124'
      })
      const serializer = new StaticLocationActionSerializer()

      const result = serializer.convertJsonApiObjectListToModelList(payload)

      expect(result).toEqual([expectedAction])
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should write out the label', () => {
      const contact = Contact.createFromObject({
        id: '123',
        givenName: 'Max',
        familyName: 'Mustermann',
        email: 'max.mustermann@localhost',
        orcid: '',
        organization: '',
        website: '',
        createdAt: DateTime.utc(2023, 2, 26, 0, 0, 0),
        updatedAt: DateTime.utc(2023, 2, 27, 0, 0, 0),
        createdByUserId: null
      })
      const action = StaticLocationAction.createFromObject({
        id: '1',
        beginContact: contact,
        beginDate: DateTime.utc(2023, 2, 28, 12, 13, 14),
        label: 'some example location',
        endDate: null,
        endContact: null,
        x: null,
        y: null,
        z: null,
        epsgCode: '4326',
        elevationDatumName: 'MSL',
        elevationDatumUri: '',
        beginDescription: '',
        endDescription: '',
        configurationId: '124'
      })
      const configurationId = '456'

      const expectedResult = {
        type: 'configuration_static_location_action',
        id: '1',
        attributes: {
          begin_date: '2023-02-28T12:13:14.000Z',
          end_date: null,
          label: 'some example location',
          begin_description: '',
          end_description: '',
          epsg_code: '4326',
          elevation_datum_name: 'MSL',
          elevation_datum_uri: '',
          x: null,
          y: null,
          z: null
        },
        relationships: {
          begin_contact: {
            data: {
              id: '123',
              type: 'contact'
            }
          },
          end_contact: {
            data: null
          },
          configuration: {
            data: {
              id: configurationId,
              type: 'configuration'
            }
          }
        }
      }
      const serializer = new StaticLocationActionSerializer()
      const result = serializer.convertModelToJsonApiData(configurationId, action)

      expect(result).toEqual(expectedResult)
    })
  })
})
