/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2026
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

export const trueFalseDefaultText = (value: boolean | null | undefined, textIfTrue: string, textIfFalse: string, textDefault: string): string => {
  if (value === true) {
    return textIfTrue
  }
  if (value === false) {
    return textIfFalse
  }
  return textDefault
}
