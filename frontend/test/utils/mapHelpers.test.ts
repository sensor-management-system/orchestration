/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { hasSelfIntersection } from '@/utils/mapHelpers'

describe('hasSelfIntersection', () => {
  it('should return false for a line with 2 or less points', () => {
    const coords = [
      { lat: 0, lng: 0 },
      { lat: 1, lng: 1 }
    ]
    expect(hasSelfIntersection(coords)).toBe(false)
  })

  it('should return true for a self-intersecting line', () => {
    const coords = [
      { lat: 0, lng: 0 },
      { lat: 1, lng: 1 },
      { lat: 1, lng: 0 },
      { lat: 0, lng: 1 },
      { lat: 0, lng: 0 }
    ]
    expect(hasSelfIntersection(coords)).toBe(true)
  })

  it('should return false for a non-self-intersecting line', () => {
    const coords = [
      { lat: 0, lng: 0 },
      { lat: 1, lng: 1 },
      { lat: 2, lng: 2 },
      { lat: 3, lng: 3 }
    ]
    expect(hasSelfIntersection(coords)).toBe(false)
  })
})
