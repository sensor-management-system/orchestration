/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'
import { availabilityReason } from '@/utils/mountHelper'
import { Availability } from '@/models/Availability'
import { dateToString } from '@/utils/dateHelper'

describe('availabilityReason', () => {
  it('should return "Not available" when availability is undefined', () => {
    expect(availabilityReason()).toEqual('Not available')
  })

  test('should return configuration ID if label is not present', () => {
    const availability = new Availability()
    availability.configurationID = 'config-123'

    expect(availabilityReason(availability)).toContain('config-123')
  })

  test('should return configuration label if present', () => {
    const availability = new Availability()
    availability.configurationID = 'config-123'
    availability.configurationLabel = 'Label XYZ'
    expect(availabilityReason(availability)).toContain('Label XYZ')
  })

  test('should return "indefinitely" if endDate is missing', () => {
    const availability = new Availability()
    availability.configurationID = 'config-123'
    expect(availabilityReason(availability)).toContain('indefinitely')
  })

  test('should return "indefinitely" if endDate is invalid', () => {
    const availability = new Availability()
    availability.configurationID = 'config-123'
    availability.endDate = DateTime.invalid('Invalid date')
    expect(availabilityReason(availability)).toContain('indefinitely')
  })

  test('should include formatted end date if endDate is valid', () => {
    const availability = new Availability()
    availability.configurationID = 'config-123'
    availability.endDate = DateTime.fromISO('2025-12-31')

    expect(availabilityReason(availability)).toContain(`until ${dateToString(availability.endDate)}`)
  })

  test('should include formatted begin date if beginDate is valid', () => {
    const availability = new Availability()
    availability.configurationID = 'config-123'
    availability.beginDate = DateTime.fromISO('2024-01-01')

    expect(availabilityReason(availability)).toContain(`from ${dateToString(availability.beginDate)}`)
  })

  test('should include both begin and end dates when valid', () => {
    const availability = new Availability()
    availability.configurationID = 'config-123'
    availability.beginDate = DateTime.fromISO('2024-01-01')
    availability.endDate = DateTime.fromISO('2025-12-31')

    const result = availabilityReason(availability)

    expect(result).toContain(`from ${dateToString(availability.beginDate)}`)
    expect(result).toContain(`until ${dateToString(availability.endDate)}`)
  })
})
