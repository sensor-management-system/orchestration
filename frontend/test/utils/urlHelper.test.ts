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
import { getLastPathElement, protocolsInUrl, removeBaseUrl, removeFirstSlash, removeTrailingSlash, toRouterPath } from '@/utils/urlHelpers'

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

describe('toRouterPath', () => {
  it('should remove the base url', () => {
    const callbackPath = 'https://localhost:8080/login-callback'
    const result = toRouterPath(callbackPath)
    expect(result).toEqual('/login-callback')
  })
  it('should work with another static path element', () => {
    const callbackPath = 'https://localhost:8080/static/logout-callback'
    const result = toRouterPath(callbackPath, '/static')
    expect(result).toEqual('/logout-callback')
  })
})
describe('protocolsInUrl', () => {
  it('should return true with the correct protocols', () => {
    const allowedProtocols = ['http', 'https']
    const url = 'http://www.heise.de'
    const urlSecure = 'https://www.heise.de'
    expect(protocolsInUrl(allowedProtocols, url)).toBeTruthy()
    expect(protocolsInUrl(allowedProtocols, urlSecure)).toBeTruthy()
  })
  it('should return false with a protocol that is not supported', () => {
    const allowedProtocols = ['http', 'https']
    const url = 'ftp://www.heise.de'
    expect(protocolsInUrl(allowedProtocols, url)).toBeFalsy()
  })
})
describe('getLastPathElement', () => {
  it('should work with basic file names', () => {
    const url = 'http://downloads/data/README.md'
    expect(getLastPathElement(url)).toEqual('README.md')
  })
  it('should also work with a trailing slash', () => {
    const url = 'http://files/folder/abc.csv/'
    expect(getLastPathElement(url)).toEqual('abc.csv')
  })
})
