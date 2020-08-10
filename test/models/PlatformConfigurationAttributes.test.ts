import Platform from '@/models/Platform'
import { PlatformConfigurationAttributes } from '@/models/PlatformConfigurationAttributes'

describe('PlatformConfigurationAttributes', () => {
  it('should create a PlatformConfigurationAttributes object', () => {
    const platform = new Platform()
    platform.id = 1

    const attributes = new PlatformConfigurationAttributes(platform)
    expect(attributes).toHaveProperty('platform', platform)
    expect(attributes).toHaveProperty('id', 1)
  })

  it('should create a PlatformConfigurationAttributes from an object', () => {
    const platform = new Platform()
    platform.id = 1

    const attributes = PlatformConfigurationAttributes.createFromObject({ platform, offsetX: 1, offsetY: 1, offsetZ: 1 })
    expect(typeof attributes).toBe('object')
    expect(attributes).toHaveProperty('platform', platform)
    expect(attributes).toHaveProperty('id', 1)
    expect(attributes).toHaveProperty('offsetX', 1)
    expect(attributes).toHaveProperty('offsetY', 1)
    expect(attributes).toHaveProperty('offsetZ', 1)
  })

  it('should set a property by its path', () => {
    const platform = new Platform()
    platform.id = 1

    const attributes = new PlatformConfigurationAttributes(platform)
    attributes.setPath('offsetX', 1)
    attributes.setPath('offsetY', 1)
    attributes.setPath('offsetZ', 1)

    expect(attributes).toHaveProperty('id', 1)
    expect(attributes).toHaveProperty('offsetX', 1)
    expect(attributes).toHaveProperty('offsetY', 1)
    expect(attributes).toHaveProperty('offsetZ', 1)
  })

  it('should throw an error when using a invalid path', () => {
    const platform = new Platform()
    platform.id = 1

    const attributes = new PlatformConfigurationAttributes(platform)
    expect(() => attributes.setPath('id', 2)).toThrow(TypeError)
  })
})
