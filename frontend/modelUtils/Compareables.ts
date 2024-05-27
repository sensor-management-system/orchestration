/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2021
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'

export interface IComparator<T> {
  compare (a: T, b: T): number
}

export interface IDateCompareable {
  date: DateTime | null
}

export function isDateCompareable (i: any): i is IDateCompareable {
  if (i && typeof i === 'object' && 'date' in i && DateTime.isDateTime(i.date)) {
    return true
  }
  return false
}

export class DateComparator implements IComparator<IDateCompareable> {
  compare (a: IDateCompareable, b: IDateCompareable): number {
    if (!a.date && !b.date) {
      return 0
    }
    if (!a.date || (b.date && a.date < b.date)) {
      return -1
    }
    if (!b.date || (a.date && a.date > b.date)) {
      return 1
    }
    return 0
  }
}
