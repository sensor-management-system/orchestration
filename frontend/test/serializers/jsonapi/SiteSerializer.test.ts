/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tim Eder (UFZ, tim.eder@ufz.de)
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
