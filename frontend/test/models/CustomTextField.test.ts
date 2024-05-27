/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { CustomTextField } from '@/models/CustomTextField'

describe('CustomTextField', () => {
  test('create a CustomTextField from an object', () => {
    const textfield = CustomTextField.createFromObject({
      id: '2',
      key: 'foo',
      value: 'bar',
      description: 'The foo'
    })
    expect(typeof textfield).toBe('object')
    expect(textfield).toHaveProperty('id', '2')
    expect(textfield).toHaveProperty('key', 'foo')
    expect(textfield).toHaveProperty('value', 'bar')
    expect(textfield).toHaveProperty('description', 'The foo')
  })
})
