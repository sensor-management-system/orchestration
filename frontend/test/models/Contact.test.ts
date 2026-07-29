/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * - Nils Brinckmann <nils.brinckmann@gfz.de>
 * - GFZ - Helmholtz Centre for Geosciences (GFZ, https://www.gfz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { Contact } from '@/models/Contact'

describe('Contact', () => {
  describe('#composedCity', () => {
    it('should be empty if we don\'t have any city information', () => {
      const contact = new Contact()
      const result = contact.composedCity
      expect(result).toEqual('')
    })
    it('should be composed if we have a lot of information', () => {
      const contact = new Contact()
      contact.city = 'Potsdam'
      contact.zipCode = '14473'
      contact.administrativeArea = 'Brandenburg'
      const result = contact.composedCity
      expect(result).toEqual('14473 Potsdam, Brandenburg')
    })
    it('should work without administrative area', () => {
      const contact = new Contact()
      contact.city = 'Potsdam'
      contact.zipCode = '14473'
      const result = contact.composedCity
      expect(result).toEqual('14473 Potsdam')
    })
    it('should work with just the city', () => {
      const contact = new Contact()
      contact.city = 'Potsdam'
      const result = contact.composedCity
      expect(result).toEqual('Potsdam')
    })
  })
})
