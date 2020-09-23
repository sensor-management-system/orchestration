import Platform from '@/models/Platform'
import { PlatformConfigurationAttributes } from '@/models/PlatformConfigurationAttributes'

describe('PlatformConfigurationAttributes', () => {
  it('should create a PlatformConfigurationAttributes object', () => {
    const platform = new Platform()
    platform.id = '1'

    const attributes = new PlatformConfigurationAttributes(platform)
    expect(attributes.platform).toBe(platform)
    expect(attributes).toHaveProperty('id', '1')
  })

  it('should create a PlatformConfigurationAttributes from an object', () => {
    const platform = new Platform()
    platform.id = '1'

    const attributes = PlatformConfigurationAttributes.createFromObject({ platform, offsetX: 1, offsetY: 1, offsetZ: 1 })
    expect(typeof attributes).toBe('object')
    expect(attributes.platform).toBe(platform)
    expect(attributes).toHaveProperty('id', '1')
    expect(attributes).toHaveProperty('offsetX', 1)
    expect(attributes).toHaveProperty('offsetY', 1)
    expect(attributes).toHaveProperty('offsetZ', 1)
  })
})
