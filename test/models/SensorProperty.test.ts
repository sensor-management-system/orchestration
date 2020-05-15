import { MeasuringRange } from '../../models/MeasuringRange'
import { SensorProperty } from '../../models/SensorProperty'

describe('SensorProperty Models', () => {
  test('create a SensorProperty from an object', () => {
    const prop = SensorProperty.createFromObject({
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
})
