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
import { Availability } from '@/models/Availability'
import { dateToString } from '@/utils/dateHelper'

export function availabilityReason (availability?: Availability): string {
  if (!availability) {
    return 'Not available'
  }

  let configString = availability.configurationID

  if (availability.configurationLabel) {
    configString = availability.configurationLabel
  }

  let endString = ''
  if (!availability.endDate?.isValid) {
    endString = 'indefinitely'
  } else {
    endString = `until ${dateToString(availability.endDate as DateTime)}`
  }

  let beginString = ''
  if (availability.beginDate?.isValid) {
    beginString = `from ${dateToString(availability.beginDate as DateTime)}`
  }

  return `Used in configuration "${configString}" ${beginString} ${endString}`
}
