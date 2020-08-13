import { CustomTextField } from '@/models/CustomTextField'

describe('CustomTextField', () => {
  test('create a CustomTextField from an object', () => {
    const textfield = CustomTextField.createFromObject({ key: 'foo', value: 'bar' })
    expect(typeof textfield).toBe('object')
    expect(textfield).toHaveProperty('key', 'foo')
    expect(textfield).toHaveProperty('value', 'bar')
  })
})
