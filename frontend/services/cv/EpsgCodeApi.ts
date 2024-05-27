/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { EpsgCode } from '@/models/EpsgCode'

export class EpsgCodeApi {
  findAll (): Promise<EpsgCode[]> {
    return new Promise((resolve) => {
      resolve([
        EpsgCode.createFromObject({
          code: '4326', text: 'WGS84 - EPSG:4326'
        })
      ])
    })
  }
}
