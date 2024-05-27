/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { byLogicOrderHighestFirst } from '@/modelUtils/mountHelpers'

describe('byLogicOrderHighestFirst', () => {
  it('should sort by logic order', () => {
    const values = [
      {
        key: 'a',
        logicOrder: 400
      },
      {
        key: 'b',
        logicOrder: 600
      },
      {
        key: 'c',
        logicOrder: 200
      }
    ]

    values.sort(byLogicOrderHighestFirst)

    expect(values[0].key).toBe('b')
    expect(values[1].key).toBe('a')
    expect(values[2].key).toBe('c')
  })
})
