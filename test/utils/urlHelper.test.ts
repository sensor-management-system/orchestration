/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
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
import { removeBaseUrl, removeFirstSlash, removeTrailingSlash } from '@/utils/urlHelpers'

describe('removeBaseUrl', () => {
  it('should return the url if the base url is undefined', () => {
    const url = 'http://xyz.org/foo/bar'
    const baseUrl = undefined

    const result = removeBaseUrl(url, baseUrl)

    expect(result).toBe(url)
  })

  it('should return the last part of the url if the base url is given and valid for the url', () => {
    const url = 'http://xyz.org/foo/bar'
    const baseUrl = 'http://xyz.org/'

    const result = removeBaseUrl(url, baseUrl)

    expect(result).toBe('foo/bar')
  })

  it('should return the url if the base url is given but not valid for the url', () => {
    const url = 'http://xyz.org/foo/bar'
    const baseUrl = 'http://xyzk.org/'

    const result = removeBaseUrl(url, baseUrl)

    expect(result).toBe(url)
  })

  it('should also work with a real example', () => {
    const url = 'http://rz-vm64.gfz-potsdam.de:5001/api/platformtype/Station/'
    const baseUrl = 'http://rz-vm64.gfz-potsdam.de:5001/api'

    const result = removeBaseUrl(url, baseUrl)

    expect(result).toBe('platformtype/Station')
  })
})

describe('removeFirstSlash', () => {
  it('should remove a starting slash', () => {
    const input = '/foo'
    const result = removeFirstSlash(input)
    expect(result).toBe('foo')
  })

  it('should not change the string if the slash is somehere else', () => {
    const input = 'f/oo/'
    const result = removeFirstSlash(input)
    expect(result).toBe(input)
  })
})

describe('removeTrailingSlash', () => {
  it('should remove a trailing slash', () => {
    const input = 'foo/'
    const result = removeTrailingSlash(input)
    expect(result).toBe('foo')
  })

  it('should not change the string if the slash is somehere else', () => {
    const input = '/f/oo'
    const result = removeTrailingSlash(input)
    expect(result).toBe(input)
  })
})
