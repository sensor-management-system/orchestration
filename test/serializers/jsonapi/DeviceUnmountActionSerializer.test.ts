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

import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'
import { DeviceUnmountAction } from '@/models/DeviceUnmountAction'

import { DeviceUnmountActionSerializer } from '@/serializers/jsonapi/DeviceUnmountActionSerializer'

const contact = new Contact()
contact.id = '1'
contact.givenName = 'Max'
contact.familyName = 'Mustermann'
contact.email = 'max@mustermann.de'

const device = new Device()
device.id = '2'
device.shortName = 'device'

const configurationId = '3'

const date = DateTime.utc(2020, 1, 1, 12, 0, 0)

describe('DeviceUnmountActionSerializer', () => {
  describe('#convertModelToJsonApiData', () => {
    it('should work if the deviceUnmountAction has no id', () => {
      const deviceUnmountAction = DeviceUnmountAction.createFromObject({
        id: '',
        device,
        contact,
        date,
        description: 'Device unmount'
      })

      const serializer = new DeviceUnmountActionSerializer()

      const output = serializer.convertModelToJsonApiData(configurationId, deviceUnmountAction)

      const expectedOutput = {
        type: 'device_unmount_action',
        attributes: {
          description: 'Device unmount',
          end_date: '2020-01-01T12:00:00.000Z'
        },
        relationships: {
          device: {
            data: {
              type: 'device',
              id: '2'
            }
          },
          contact: {
            data: {
              type: 'contact',
              id: '1'
            }
          },
          configuration: {
            data: {
              type: 'configuration',
              id: '3'
            }
          }
        }
      }
      expect(output).toEqual(expectedOutput)
    })
    it('should also work with an existing id', () => {
      const deviceUnmountAction = DeviceUnmountAction.createFromObject({
        id: '4',
        device,
        contact,
        date,
        description: 'Device unmount'
      })

      const serializer = new DeviceUnmountActionSerializer()

      const output = serializer.convertModelToJsonApiData(configurationId, deviceUnmountAction)

      const expectedOutput = {
        type: 'device_unmount_action',
        id: '4',
        attributes: {
          description: 'Device unmount',
          end_date: '2020-01-01T12:00:00.000Z'
        },
        relationships: {
          device: {
            data: {
              type: 'device',
              id: '2'
            }
          },
          contact: {
            data: {
              type: 'contact',
              id: '1'
            }
          },
          configuration: {
            data: {
              type: 'configuration',
              id: '3'
            }
          }
        }
      }
      expect(output).toEqual(expectedOutput)
    })
  })
})
