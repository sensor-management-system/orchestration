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
import { Platform } from '@/models/Platform'
import { PlatformMountAction } from '@/models/PlatformMountAction'

import { PlatformMountActionSerializer } from '@/serializers/jsonapi/PlatformMountActionSerializer'

const contact = new Contact()
contact.id = '1'
contact.givenName = 'Max'
contact.familyName = 'Mustermann'
contact.email = 'max@mustermann.de'

const platform = new Platform()
platform.id = '2'
platform.shortName = 'platform'

const configurationId = '3'

const date = DateTime.utc(2020, 1, 1, 12, 0, 0)

describe('PlatformMountActionSerializer', () => {
  describe('#convertModelToJsonApiData', () => {
    it('should work if the platformMountAction has no id', () => {
      const platformMountAction = PlatformMountAction.createFromObject({
        id: '',
        platform,
        parentPlatform: null,
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        contact,
        date,
        description: 'Platform mount'
      })

      const serializer = new PlatformMountActionSerializer()

      const output = serializer.convertModelToJsonApiData(configurationId, platformMountAction)

      const expectedOutput = {
        type: 'platform_mount_action',
        attributes: {
          offset_x: 0,
          offset_y: 0,
          offset_z: 0,
          description: 'Platform mount',
          begin_date: '2020-01-01T12:00:00.000Z'
        },
        relationships: {
          platform: {
            data: {
              type: 'platform',
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
    it('should work if the platformMountAction has no id and a parent platform', () => {
      const parentPlatform = new Platform()
      parentPlatform.id = '4'
      const platformMountAction = PlatformMountAction.createFromObject({
        id: '',
        platform,
        parentPlatform,
        offsetX: 1,
        offsetY: 2,
        offsetZ: 3,
        contact,
        date,
        description: 'Platform mount'
      })

      const serializer = new PlatformMountActionSerializer()

      const output = serializer.convertModelToJsonApiData(configurationId, platformMountAction)

      const expectedOutput = {
        type: 'platform_mount_action',
        attributes: {
          offset_x: 1,
          offset_y: 2,
          offset_z: 3,
          description: 'Platform mount',
          begin_date: '2020-01-01T12:00:00.000Z'
        },
        relationships: {
          platform: {
            data: {
              type: 'platform',
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
          },
          parent_platform: {
            data: {
              type: 'platform',
              id: '4'
            }
          }
        }
      }
      expect(output).toEqual(expectedOutput)
    })
    it('should also work with an existing id', () => {
      const platformMountAction = PlatformMountAction.createFromObject({
        id: '5',
        platform,
        parentPlatform: null,
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        contact,
        date,
        description: 'Platform mount'
      })

      const serializer = new PlatformMountActionSerializer()

      const output = serializer.convertModelToJsonApiData(configurationId, platformMountAction)

      const expectedOutput = {
        type: 'platform_mount_action',
        id: '5',
        attributes: {
          offset_x: 0,
          offset_y: 0,
          offset_z: 0,
          description: 'Platform mount',
          begin_date: '2020-01-01T12:00:00.000Z'
        },
        relationships: {
          platform: {
            data: {
              type: 'platform',
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
