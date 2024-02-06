/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2024
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
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
import { Contact } from '@/models/Contact'
import { Platform } from '@/models/Platform'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { PlatformNode } from '@/viewmodels/PlatformNode'
import { sumOffsets } from '@/utils/configurationsTreeHelper'

const contact = new Contact()
const date = DateTime.utc(2020, 2, 3, 0, 0, 0, 0)

describe('#sumOffsets', () => {
  it('should return the sum of all nodes', () => {
    const nodes = [
      new PlatformNode(PlatformMountAction.createFromObject({
        id: '',
        platform: new Platform(),
        parentPlatform: null,
        offsetX: 1,
        offsetY: 2,
        offsetZ: 3,
        epsgCode: '',
        x: null,
        y: null,
        z: null,
        elevationDatumName: '',
        elevationDatumUri: '',
        beginContact: contact,
        beginDate: date,
        beginDescription: 'Platform mount',
        endDate: null,
        endContact: null,
        endDescription: null
      })),
      new PlatformNode(PlatformMountAction.createFromObject({
        id: '',
        platform: new Platform(),
        parentPlatform: null,
        offsetX: 4,
        offsetY: 5,
        offsetZ: 6,
        epsgCode: '',
        x: null,
        y: null,
        z: null,
        elevationDatumName: '',
        elevationDatumUri: '',
        beginContact: contact,
        beginDate: date,
        beginDescription: 'Platform mount',
        endDate: null,
        endContact: null,
        endDescription: null
      })),
      new PlatformNode(PlatformMountAction.createFromObject({
        id: '',
        platform: new Platform(),
        parentPlatform: null,
        offsetX: 7,
        offsetY: 8,
        offsetZ: 9,
        epsgCode: '',
        x: null,
        y: null,
        z: null,
        elevationDatumName: '',
        elevationDatumUri: '',
        beginContact: contact,
        beginDate: date,
        beginDescription: 'Platform mount',
        endDate: null,
        endContact: null,
        endDescription: null
      }))
    ]

    expect(sumOffsets(nodes)).toMatchObject({
      offsetX: 12,
      offsetY: 15,
      offsetZ: 18
    })
  })
})
