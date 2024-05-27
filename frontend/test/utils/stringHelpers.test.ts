/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
*/

import { coalesce, capitalize } from '@/utils/stringHelpers'

describe('coalesce', () => {
  it('should return the first string if defined', () => {
    expect(coalesce('A', 'B')).toEqual('A')
  })
  it('should return the second string if the first is null', () => {
    expect(coalesce(null, 'B')).toEqual('B')
  })
  it('should return the second string if the first is undefined', () => {
    expect(coalesce(undefined, 'B')).toEqual('B')
  })
  it('should return the second string if the first is empty', () => {
    expect(coalesce('', 'B')).toEqual('B')
  })
})

describe('capitalize', () => {
  it('should return an empty string, if an empty string was provided', () => {
    expect(capitalize('')).toEqual('')
  })
  it('should return a string with the first letter in captial, if it was lowercase', () => {
    expect(capitalize('a')).toEqual('A')
  })
  it('should return a string with the first letter in captial, if it was uppercase', () => {
    expect(capitalize('A')).toEqual('A')
  })
  it('should return a string with the first letter in captial and does not change the other letters', () => {
    expect(capitalize('abc')).toEqual('Abc')
    expect(capitalize('ABC')).toEqual('ABC')
  })
})
