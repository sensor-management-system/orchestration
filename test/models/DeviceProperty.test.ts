import { MeasuringRange } from '@/models/MeasuringRange'
import { DeviceProperty } from '@/models/DeviceProperty'

describe('DeviceProperty Models', () => {
  it('should create a DeviceProperty from an object', () => {
    const prop = DeviceProperty.createFromObject({
      id: null,
      label: 'test',
      compartmentUri: 'http://foo/compartment/1',
      compartmentName: 'bar',
      unitUri: 'http://foo/unit/1',
      unitName: 'mm',
      samplingMediaUri: 'http://foo/samplingMedia/1',
      samplingMediaName: 'water',
      propertyUri: 'http://foo/property/1',
      propertyName: 'foo.bar',
      measuringRange: {
        min: 10,
        max: 1000
      },
      accuracy: 0.1,
      failureValue: 0.01
    })
    expect(typeof prop).toBe('object')
    expect(prop).toHaveProperty('id', null)
    expect(prop).toHaveProperty('label', 'test')
    expect(prop).toHaveProperty('compartmentUri', 'http://foo/compartment/1')
    expect(prop).toHaveProperty('compartmentName', 'bar')
    expect(prop).toHaveProperty('unitUri', 'http://foo/unit/1')
    expect(prop).toHaveProperty('unitName', 'mm')
    expect(prop).toHaveProperty('samplingMediaUri', 'http://foo/samplingMedia/1')
    expect(prop).toHaveProperty('samplingMediaName', 'water')
    expect(prop).toHaveProperty('propertyUri', 'http://foo/property/1')
    expect(prop).toHaveProperty('propertyName', 'foo.bar')
    expect(prop).toHaveProperty('accuracy', 0.1)
    expect(prop).toHaveProperty('failureValue', 0.01)
    expect(prop.measuringRange instanceof MeasuringRange).toBe(true)
  })
})
