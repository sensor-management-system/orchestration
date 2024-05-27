/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { ElevationDatum } from '@/models/ElevationDatum'

export class ElevationDatumApi {
  findAll (): Promise<ElevationDatum[]> {
    return new Promise((resolve) => {
      resolve([
        ElevationDatum.createFromObject({
          name: 'MSL', uri: ''
        })
      ])
    })
  }
}
