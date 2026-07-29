/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * - Nils Brinckmann <nils.brinckmann@gfz.de>
 * - GFZ - Helmholtz Centre for Geosciences (GFZ, https://www.gfz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { Site } from '@/models/Site'

describe('Site', () => {
  describe('#composedCity', () => {
    it('should be empty if we don\'t have any city information', () => {
      const site = new Site()
      const result = site.composedCity
      expect(result).toEqual('')
    })
    it('should be composed if we have a lot of information', () => {
      const site = new Site()
      site.address = {
        city: 'Potsdam',
        zipCode: '14473',
        administrativeArea: 'Brandenburg'
      }
      const result = site.composedCity
      expect(result).toEqual('14473 Potsdam, Brandenburg')
    })
    it('should work without administrative area', () => {
      const site = new Site()
      site.address = {
        city: 'Potsdam',
        zipCode: '14473'
      }
      const result = site.composedCity
      expect(result).toEqual('14473 Potsdam')
    })
    it('should work with just the city', () => {
      const site = new Site()
      site.address = {
        city: 'Potsdam'
      }
      const result = site.composedCity
      expect(result).toEqual('Potsdam')
    })
  })
})
