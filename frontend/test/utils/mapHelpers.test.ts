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
import { LatLng } from 'leaflet'
import { hasSelfIntersection, calculatePolygonArea } from '@/utils/mapHelpers'

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

describe('calculatePolygonArea', () => {
  it('calculates area of a triangle', () => {
    // A triangle with vertices (0,0), (4,0), (4,3)
    const triangle: LatLng[] = [
      new LatLng(0, 0),
      new LatLng(4, 0),
      new LatLng(4, 3)
    ]

    // The expected area is 6 (triangle area formula: 1/2 * base * height)
    const area = calculatePolygonArea(triangle)
    expect(area).toBeCloseTo(6)
  })

  it('calculates area of a square', () => {
    // A square with side length 4, vertices (0,0), (4,0), (4,4), (0,4)
    const square: LatLng[] = [
      new LatLng(0, 0),
      new LatLng(4, 0),
      new LatLng(4, 4),
      new LatLng(0, 4)
    ]

    // The expected area is 16 (square area: side^2)
    const area = calculatePolygonArea(square)
    expect(area).toBeCloseTo(16)
  })

  it('returns 0 for no coordinates (empty array)', () => {
    const empty: LatLng[] = []

    // No polygon, so the area should be 0
    const area = calculatePolygonArea(empty)
    expect(area).toBe(0)
  })

  it('returns 0 for a single point', () => {
    const singlePoint: LatLng[] = [new LatLng(0, 0)]

    // A single point doesn't form a polygon, area should be 0
    const area = calculatePolygonArea(singlePoint)
    expect(area).toBe(0)
  })

  it('returns 0 for two points (line segment)', () => {
    const twoPoints: LatLng[] = [
      new LatLng(0, 0),
      new LatLng(4, 0)
    ]

    // Two points form a line, not a polygon, so the area should be 0
    const area = calculatePolygonArea(twoPoints)
    expect(area).toBe(0)
  })

  it('returns 0 for collinear points', () => {
    const collinearPoints: LatLng[] = [
      new LatLng(0, 0),
      new LatLng(2, 0),
      new LatLng(4, 0)
    ]

    // Collinear points (all on a straight line) should form no polygon, so the area is 0
    const area = calculatePolygonArea(collinearPoints)
    expect(area).toBe(0)
  })

  it('calculates area of a complex polygon (pentagon)', () => {
    const pentagon: LatLng[] = [
      new LatLng(0, 0),
      new LatLng(4, 0),
      new LatLng(5, 3),
      new LatLng(2, 5),
      new LatLng(-1, 3)
    ]

    const expectedArea = 21
    const area = calculatePolygonArea(pentagon)
    expect(area).toBeCloseTo(expectedArea)
  })
})
