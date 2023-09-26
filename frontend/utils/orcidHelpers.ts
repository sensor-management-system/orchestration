/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2023
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
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

/*
 * The code from this file is adapted from the Laboratory Instrument Inventory.
 * https://git.gfz-potsdam.de/li-geo.x/li2/-/blob/master/portal-frontend/utils/orcid.ts
 *
 * As Marc was the author there, it should be ok to reuse the code as it is.
 */

const ORCID_DIVIDER = '-'

/**
 * checks if the ORCID has an valid checksum
 *
 * @param {string} orcid - the ORCID to check for validity
 * @returns {boolean} true if the ORCID is valid, otherwise false
 */
export function orcidHasValidChecksum (orcid: string): boolean {
  if (orcid.length < 19) {
    return false
  }
  const checksum: string = calculateOrcidChecksum(stripOrcidDividers(orcid))
  const lastDigit: string = orcid.substring(18, 19)
  if (lastDigit !== checksum) {
    return false
  }
  return true
}

/**
 * tests if the ORCID is valid
 * tests for the format as well as for the checksum
 *
 * calls {@link orcidHasValidChecksum}
 *
 * @param {string} orcid - the ORCID to check for validity
 * @returns {boolean} true when the ORCID is valid, otherwise false
 */
export function isValidOrcid (orcid: string): boolean {
  if (!orcid.match(/[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]/)) {
    return false
  }
  return orcidHasValidChecksum(orcid)
}

/**
 * calculates the checksum of the ORCID
 * adapted from https://support.orcid.org/hc/en-us/articles/360006897674-Structure-of-the-ORCID-Identifier
 *
 * @param {string} orcid - the ORCID to check for validity
 * @returns {string} the checksum (last digit) of the ORCID
 */
export function calculateOrcidChecksum (orcid: string): string {
  let total: number = 0
  stripOrcidDividers(orcid).substring(0, 15).split('').forEach((character: string) => {
    const digit: number = parseInt(character, 36)
    total = (total + digit) * 2
  })
  const remainder: number = total % 11
  const result: number = (12 - remainder) % 11
  return result === 10 ? 'X' : result.toString()
}

/**
 * returns an ORCID without dividers
 *
 * @param {string} orcid - the ORCID
 * @returns {string} the ORCID without the dividers
 */
export function stripOrcidDividers (orcid: string): string {
  return orcid.replace(new RegExp(ORCID_DIVIDER, 'g'), '')
}
