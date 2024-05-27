/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { MeasuringRange } from '@/models/MeasuringRange'

describe('MeasuringRange Models', () => {
  test('create a MeasuringRange from an object', () => {
    const range = MeasuringRange.createFromObject({ min: 10, max: 10 })
    expect(typeof range).toBe('object')
    expect(range).toHaveProperty('min', 10)
    expect(range).toHaveProperty('max', 10)
  })
})
