/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2023 - 2024
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

/*
 * The code from this file is adapted from the Laboratory Instrument Inventory.
 * https://git.gfz-potsdam.de/li-geo.x/li2/-/blob/master/portal-frontend/test/utils/orcid.test.ts
 *
 * As Marc was the author there, it should be ok to reuse the code as it is.
 */
import {
  calculateOrcidChecksum,
  stripOrcidDividers,
  isValidOrcid,
  orcidHasValidChecksum
} from '@/utils/orcidHelpers'

describe('ORCID helper', () => {
  describe('#stripOrcidDividers()', () => {
    it('should return an ORCID without the dividers', () => {
      const orcid = '0000-0001-5272-4674'
      const orcidWithoutDivider = '0000000152724674'

      expect(stripOrcidDividers(orcid)).toEqual(orcidWithoutDivider)
    })
  })
  describe('#isValidOrcid()', () => {
    it('should return true when an ORCID is valid', () => {
      const validOrcid = '0000-0001-5272-4674'

      expect(isValidOrcid(validOrcid)).toBeTruthy()
    })
    it('should return false when an ORCID is invalid', () => {
      const invalidOrcid1 = '000A-000B-000C-000D'
      const invalidOrcid2 = '0000/0001/5272/4674'
      const orcidWithInvalidChecksum = '1234-1234-1234-1234'

      expect(isValidOrcid(invalidOrcid1)).toBeFalsy()
      expect(isValidOrcid(invalidOrcid2)).toBeFalsy()
      expect(isValidOrcid(orcidWithInvalidChecksum)).toBeFalsy()
    })
  })
  describe('#orcidHasValidChecksum()', () => {
    it('should return true when an ORCID is has a valid checksum', () => {
      const validOrcid = '0000-0001-5272-4674'

      expect(orcidHasValidChecksum(validOrcid)).toBeTruthy()
    })
    it('should return false when an ORCID is has an invalid checksum', () => {
      const invalidOrcid = '0000-0001-5272-4679'

      expect(orcidHasValidChecksum(invalidOrcid)).toBeFalsy()
    })
    it('should return false when the length of an ORCID is lower than 19', () => {
      const invalidOrcid = '0000-0001-5272'

      expect(orcidHasValidChecksum(invalidOrcid)).toBeFalsy()
    })
  })
  describe('#calculateOrcidChecksum()', () => {
    it('should return the correct checksum', () => {
      const orcid1 = '0000-0001-5272-4674'
      const checksum1 = '4'
      const falseChecksums1 = ['1', '2', '3', '5', '6', '7', '8', '9', 'X']
      const orcid2 = '0000-0002-5765-0245'
      const checksum2 = '5'
      const falseChecksums2 = ['1', '2', '3', '4', '6', '7', '8', '9', 'X']
      const orcid3 = '0000-0002-0174-594X'
      const checksum3 = 'X'
      const falseChecksums3 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

      expect(calculateOrcidChecksum(orcid1)).toEqual(checksum1)
      falseChecksums1.forEach((checksum) => {
        expect(calculateOrcidChecksum(orcid1)).not.toEqual(checksum)
      })

      expect(calculateOrcidChecksum(orcid2)).toEqual(checksum2)
      falseChecksums2.forEach((checksum) => {
        expect(calculateOrcidChecksum(orcid2)).not.toEqual(checksum)
      })

      expect(calculateOrcidChecksum(orcid3)).toEqual(checksum3)
      falseChecksums3.forEach((checksum) => {
        expect(calculateOrcidChecksum(orcid3)).not.toEqual(checksum)
      })
    })
  })
})
