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

  it('should set a property by its path', () => {
    const prop = new DeviceProperty()
    prop.setPath('id', 1)
    prop.setPath('label', 'test')
    prop.setPath('compartmentUri', 'http://foo/compartment/1')
    prop.setPath('compartmentName', 'bar')
    prop.setPath('unitUri', 'http://foo/unit/1')
    prop.setPath('unitName', 'mm')
    prop.setPath('samplingMediaUri', 'http://foo/samplingMedia/1')
    prop.setPath('samplingMediaName', 'water')
    prop.setPath('propertyUri', 'http://foo/property/1')
    prop.setPath('propertyName', 'foo.bar')
    prop.setPath('accuracy', 0.1)
    prop.setPath('failureValue', 0.01)
    prop.setPath('measuringRange.min', 10)
    prop.setPath('measuringRange.max', 20)

    expect(prop).toHaveProperty('id', 1)
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
    expect(prop.measuringRange).toHaveProperty('min', 10)
    expect(prop.measuringRange).toHaveProperty('max', 20)
  })
})
