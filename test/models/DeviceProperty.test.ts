import { MeasuringRange } from '../../models/MeasuringRange'
import { DeviceProperty } from '../../models/DeviceProperty'

describe('DeviceProperty Models', () => {
  it('should create a DeviceProperty from an object', () => {
    const prop = DeviceProperty.createFromObject({
      compartment: 'test',
      label: 'test',
      samplingMedia: 'water',
      unit: 'mm',
      variable: 'foo.bar',
      measuringRange: {
        min: 10,
        max: 1000
      },
      accuracy: 0.1,
      failureValue: 0.01
    })
    expect(typeof prop).toBe('object')
    expect(prop).toHaveProperty('compartment', 'test')
    expect(prop).toHaveProperty('label', 'test')
    expect(prop).toHaveProperty('samplingMedia', 'water')
    expect(prop).toHaveProperty('unit', 'mm')
    expect(prop).toHaveProperty('variable', 'foo.bar')
    expect(prop).toHaveProperty('accuracy', 0.1)
    expect(prop).toHaveProperty('failureValue', 0.01)
    expect(prop.measuringRange instanceof MeasuringRange).toBe(true)
  })

  it('should set a property by its path', () => {
    const prop = new DeviceProperty()
    prop.setPath('compartment', 'test')
    prop.setPath('label', 'foo')
    prop.setPath('samplingMedia', 'water')
    prop.setPath('unit', 'mm')
    prop.setPath('variable', 'foo.bar')
    prop.setPath('measuringRange.min', 10)
    prop.setPath('measuringRange.max', 20)
    prop.setPath('accuracy', 0.1)
    prop.setPath('failureValue', 0.01)

    expect(prop).toHaveProperty('compartment', 'test')
    expect(prop).toHaveProperty('label', 'foo')
    expect(prop).toHaveProperty('samplingMedia', 'water')
    expect(prop).toHaveProperty('unit', 'mm')
    expect(prop).toHaveProperty('variable', 'foo.bar')
    expect(prop).toHaveProperty('accuracy', 0.1)
    expect(prop).toHaveProperty('failureValue', 0.01)
    expect(prop.measuringRange).toHaveProperty('min', 10)
    expect(prop.measuringRange).toHaveProperty('max', 20)
  })
})
