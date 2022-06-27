/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2022
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tim Eder (UFZ, tim.eder@ufz.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *   (UFZ, https://www.ufz.de)
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

function * idGenerator (index: number) {
  while (true) {
    yield index.toString()
    index++
  }
}

const idIterator = idGenerator(1)

function getEntity (type: string) {
  const id = idIterator.next().value
  return {
    id,
    type: 'platform',
    attributes: {
      short_name: `${type}_${id}`
    }
  }
}

export const mockCurrentConfiguration = [
  {
    action: {
      id: idIterator.next().value,
      type: 'platform_mount_action',
      attributes: {
        offset_y: 0.0,
        description: '',
        offset_x: 0.0,
        updated_at: null,
        offset_z: 0.0,
        begin_date: '2022-04-11T12:08:13.000000'
      }
    },
    entity: getEntity('platform'),
    children: [
      {
        action: {
          id: idIterator.next().value,
          type: 'device_mount_action',
          attributes: {
            offset_y: 0.0,
            description: '',
            offset_x: 0.0,
            updated_at: null,
            offset_z: 0.0,
            begin_date: '2022-04-11T12:08:13.000000'
          }
        },
        entity: getEntity('device'),
        children: []
      },
      {
        action: {
          id: idIterator.next().value,
          type: 'platform_mount_action',
          attributes: {
            offset_y: 0.0,
            description: '',
            offset_x: 0.0,
            updated_at: null,
            offset_z: 0.0,
            begin_date: '2022-04-11T12:08:13.000000'
          }
        },
        entity: getEntity('platform'),
        children: [
          {
            action: {
              id: idIterator.next().value,
              type: 'device_mount_action',
              attributes: {
                offset_y: 0.0,
                description: '',
                offset_x: 0.0,
                updated_at: null,
                offset_z: 0.0,
                begin_date: '2022-04-11T12:08:13.000000'
              }
            },
            entity: getEntity('device'),
            children: []
          }
        ]
      }
    ]
  },
  {
    action: {
      id: idIterator.next().value,
      type: 'platform_unmount_action',
      attributes: {
        description: '',
        end_date: '2022-04-11T12:08:13.000000'
      }
    },
    entity: getEntity('platform'),
    children: []
  }
]

export const mockMountingActions = [
  {
    timepoint: DateTime.fromISO('2022-04-14T05:40:00.000Z'),
    label: '2022-04-14 05:40 - Mount | Platform X'
  },
  {
    timepoint: DateTime.fromISO('2022-05-06T06:00:00.000Z'),
    label: '2022-05-06 06:00 - Mount | Platform Y'
  }
]
