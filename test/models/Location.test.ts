import { StationaryLocation, DynamicLocation } from '@/models/Location'
import { DeviceProperty } from '@/models/DeviceProperty'

describe('StationaryLocation', () => {
  it('should create a StationaryLocation from an object', () => {
    const location = StationaryLocation.createFromObject({ type: 'stationary', latitude: 50.986451, longitude: 12.973538, elevation: 280 })
    expect(typeof location).toBe('object')
    expect(location).toHaveProperty('type', 'stationary')
    expect(location).toHaveProperty('latitude', 50.986451)
    expect(location).toHaveProperty('longitude', 12.973538)
    expect(location).toHaveProperty('elevation', 280)
  })

  it('should set a property by its path', () => {
    const location = new StationaryLocation()
    location.setPath('latitude', 50.986451)
    location.setPath('longitude', 12.973538)
    location.setPath('elevation', 280)

    expect(location).toHaveProperty('type', 'stationary')
    expect(location).toHaveProperty('latitude', 50.986451)
    expect(location).toHaveProperty('longitude', 12.973538)
    expect(location).toHaveProperty('elevation', 280)
  })

  it('should throw an error when using a invalid path', () => {
    const location = new StationaryLocation()
    expect(() => location.setPath('foo', 'bar')).toThrow(TypeError)
  })
})

describe('DynamicLocation', () => {
  it('should create a DynamicLocation from an object', () => {
    const latitude = new DeviceProperty()
    const longitude = new DeviceProperty()
    const elevation = new DeviceProperty()

    const location = DynamicLocation.createFromObject({ type: 'dynamic', latitude, longitude, elevation })
    expect(typeof location).toBe('object')
    expect(location).toHaveProperty('type', 'dynamic')
    expect(location).toHaveProperty('latitude', latitude)
    expect(location).toHaveProperty('longitude', longitude)
    expect(location).toHaveProperty('elevation', elevation)
  })
})
