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
