import { MeasuringRange } from '../../models/SensorProperty'

describe('SensorProperty Models', () => {
  test('create a MeasuringRange from an object', () => {
    const range = MeasuringRange.createFromObject({ min: 10, max: 10 })
    expect(typeof range).toBe('object')
    expect(range).toHaveProperty('min', 10)
    expect(range).toHaveProperty('max', 10)
  })
})
