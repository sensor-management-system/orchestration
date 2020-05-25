import { MeasuringRange } from '@/models/MeasuringRange'

describe('MeasuringRange Models', () => {
  test('create a MeasuringRange from an object', () => {
    const range = MeasuringRange.createFromObject({ min: 10, max: 10 })
    expect(typeof range).toBe('object')
    expect(range).toHaveProperty('min', 10)
    expect(range).toHaveProperty('max', 10)
  })

  it('should set a property by its path', () => {
    const range = new MeasuringRange()
    range.setPath('min', 10)
    range.setPath('max', 20)

    expect(range).toHaveProperty('min', 10)
    expect(range).toHaveProperty('max', 20)
  })
})
