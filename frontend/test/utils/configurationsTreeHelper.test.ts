/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
        endDescription: null,
        label: ''
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
        endDescription: null,
        label: ''
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
        endDescription: null,
        label: ''
      }))
    ]

    expect(sumOffsets(nodes)).toMatchObject({
      offsetX: 12,
      offsetY: 15,
      offsetZ: 18
    })
  })
})
