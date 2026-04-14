/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2023 - 2026
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de) *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { trueFalseDefaultText } from '@/utils/booleanHelpers'

describe('trueFalseDefaultText', () => {
  it('should return the yes string if the value is true', () => {
    const result = trueFalseDefaultText(true, 'Yes', 'No', 'Unknown')
    expect(result).toEqual('Yes')
  })
  it('should return the no string if the value is false', () => {
    const result = trueFalseDefaultText(false, 'Yes', 'No', 'Unknown')
    expect(result).toEqual('No')
  })
  it('should return the unknown string if the value is null', () => {
    const result = trueFalseDefaultText(null, 'Yes', 'No', 'Unknown')
    expect(result).toEqual('Unknown')
  })
  it('should return the unknown string if the value is undefined', () => {
    const result = trueFalseDefaultText(undefined, 'Yes', 'No', 'Unknown')
    expect(result).toEqual('Unknown')
  })
})
