import { DateTime } from 'luxon'

export interface IComparator<T> {
  compare (a: T, b: T): number
}

export interface IDateCompareable {
  date: DateTime | null
}

export function isDateCompareable (i: Partial<IDateCompareable>): i is IDateCompareable {
  if (i && typeof i === 'object' && Object.prototype.hasOwnProperty.call(i, 'date') && DateTime.isDateTime(i.date)) {
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
