/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
*/

import { round } from '@/utils/numericsHelper'

describe('round', () => {
  it('should use a default argument of 0', () => {
    expect(round(1.4)).toEqual(1)
  })
  it('should be possible to set the ndigits', () => {
    expect(round(1.4, 1)).toEqual(1.4)
  })
  it('should only take the part the point into account', () => {
    expect(round(1234.35, 1)).toEqual(1234.4)
  })
  it('should help with odd arithmetic issues', () => {
    const value = 2.7 - 1.0
    expect(value).not.toEqual(1.7)
    expect(round(value, 6)).toEqual(1.7)
  })
})
