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

import { SiteSerializer } from '@/serializers/jsonapi/SiteSerializer'

const serializer = new SiteSerializer()

describe('SiteSerializer', () => {
  describe('convertGeomToWKT', () => {
    it('should convert a geometry array to a WKT string', () => {
      const geom = [{ lat: 2.2, lng: 1.1 }, { lat: 4.4, lng: 3.3 }, { lat: 6.6, lng: 5.5 }, { lat: 8.8, lng: 7.7 }, { lat: 2.2, lng: 1.1 }]
      const result = serializer.convertGeomToWKT(geom)
      expect(result).toEqual('POLYGON((1.1 2.2,3.3 4.4,5.5 6.6,7.7 8.8,1.1 2.2,1.1 2.2))')
    })

    it('should return null if the geometry array has fewer than 3 coordinates', () => {
      const geom = [{ lat: 2.2, lng: 1.1 }, { lat: 4.4, lng: 3.3 }]
      const result = serializer.convertGeomToWKT(geom)
      expect(result).toBeNull()
    })
  })

  describe('convertWKTToGeom', () => {
    it('should convert a WKT string to a geometry array', () => {
      const wkt = 'POLYGON((1.1 2.2,3.3 4.4,5.5 6.6,7.7 8.8,1.1 2.2))'
      const result = serializer.convertWKTToGeom(wkt)
      expect(result).toEqual([
        { lat: 2.2, lng: 1.1 },
        { lat: 4.4, lng: 3.3 },
        { lat: 6.6, lng: 5.5 },
        { lat: 8.8, lng: 7.7 }
      ])
    })

    it('should return an empty array if the WKT string is not a valid POLYGON', () => {
      const wkt = 'POINT(1.1 2.2)'
      const result = serializer.convertWKTToGeom(wkt)
      expect(result).toEqual([])
    })
  })
})
