/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
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
import { DeviceProperty } from '@/models/DeviceProperty'
import { DynamicLocationBeginAction } from '@/models/DynamicLocationBeginAction'

import { DynamicLocationBeginActionSerializer } from '@/serializers/jsonapi/DynamicLocationBeginActionSerializer'

const contact = new Contact()
contact.id = '1'
contact.givenName = 'Max'
contact.familyName = 'Mustermann'
contact.email = 'max@mustermann.de'

const date = DateTime.utc(2020, 1, 1, 12, 0, 0)

const configurationId = '333'

const deviceProperty1 = new DeviceProperty()
deviceProperty1.id = 'p111'

const deviceProperty2 = new DeviceProperty()
deviceProperty2.id = 'p222'

const deviceProperty3 = new DeviceProperty()
deviceProperty3.id = 'p333'

describe('DynamicLocationBeginActionSerializer', () => {
  describe('#convertModelToJsonApiData', () => {
    it('should work if the action has no id', () => {
      const action = DynamicLocationBeginAction.createFromObject({
        x: deviceProperty1,
        y: deviceProperty2,
        z: deviceProperty3,
        contact,
        description: 'Test description',
        epsgCode: '4326',
        elevationDatumName: 'MSL',
        elevationDatumUri: 'some/uri',
        beginDate: date,
        id: ''
      })

      const serializer = new DynamicLocationBeginActionSerializer()

      const output = serializer.convertModelToJsonApiData(configurationId, action)

      const expectedOutput = {
        type: 'configuration_dynamic_location_begin_action',
        attributes: {
          epsg_code: '4326',
          description: 'Test description',
          begin_date: '2020-01-01T12:00:00.000Z',
          elevation_datum_name: 'MSL',
          elevation_datum_uri: 'some/uri'
        },
        relationships: {
          contact: {
            data: {
              type: 'contact',
              id: '1'
            }
          },
          configuration: {
            data: {
              type: 'configuration',
              id: '333'
            }
          },
          x_property: {
            data: {
              type: 'device_property',
              id: 'p111'
            }
          },
          y_property: {
            data: {
              type: 'device_property',
              id: 'p222'
            }
          },
          z_property: {
            data: {
              type: 'device_property',
              id: 'p333'
            }
          }
        }
      }
      expect(output).toEqual(expectedOutput)
    })
    it('should also work with an id and without some of the field', () => {
      const action = DynamicLocationBeginAction.createFromObject({
        x: null,
        y: null,
        z: null,
        contact,
        description: '',
        epsgCode: '4326',
        elevationDatumName: 'MSL',
        elevationDatumUri: 'some/uri',
        beginDate: date,
        id: '123'
      })

      const serializer = new DynamicLocationBeginActionSerializer()

      const output = serializer.convertModelToJsonApiData(configurationId, action)

      const expectedOutput = {
        type: 'configuration_dynamic_location_begin_action',
        id: '123',
        attributes: {
          epsg_code: '4326',
          description: '',
          begin_date: '2020-01-01T12:00:00.000Z',
          elevation_datum_name: 'MSL',
          elevation_datum_uri: 'some/uri'
        },
        relationships: {
          contact: {
            data: {
              type: 'contact',
              id: '1'
            }
          },
          configuration: {
            data: {
              type: 'configuration',
              id: '333'
            }
          }
        }
      }
      expect(output).toEqual(expectedOutput)
    })
  })
})
