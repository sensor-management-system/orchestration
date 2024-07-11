/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'
import { IDateCompareable, isDateCompareable, DateComparator } from '@/modelUtils/Compareables'

describe('DateCompareables and DateComparator', () => {
  describe('DateCompareable', () => {
    describe('#isDateCompareable', () => {
      it('should return true when an object implements a `date` property of type DateTime', () => {
        const dateObject: IDateCompareable = {
          date: DateTime.now()
        }
        expect(isDateCompareable(dateObject)).toBeTruthy()
      })
      it('should return false when an object does not implement a `date` property', () => {
        const falseObject = {
          foo: 'bar'
        }
        // @ts-ignore
        expect(isDateCompareable(falseObject)).toBeFalsy()
      })
      it('should return false when an object implements a `date` property which is not of type DateTime', () => {
        const simpleObject = {
          date: 'foo'
        }
        // @ts-ignore
        expect(isDateCompareable(simpleObject)).toBeFalsy()
      })
    })
  })
  describe('DateComparator', () => {
    describe('#compare', () => {
      it('should return -1 when first argument is less than second argument', () => {
        const a = {
          date: DateTime.fromISO('2020-06-01T10:00:00.000')
        }
        const b = {
          date: DateTime.fromISO('2020-06-02T10:00:00.000')
        }
        const comparator = new DateComparator()

        expect(comparator.compare(a, b)).toBe(-1)
      })
      it('should return 1 when first argument is greater than second argument', () => {
        const a = {
          date: DateTime.fromISO('2020-06-02T10:00:00.000')
        }
        const b = {
          date: DateTime.fromISO('2020-06-01T10:00:00.000')
        }
        const comparator = new DateComparator()

        expect(comparator.compare(a, b)).toBe(1)
      })
      it('should return 0 when both arguments are equal', () => {
        const a = {
          date: DateTime.fromISO('2020-06-02T10:00:01.000')
        }
        const b = {
          date: DateTime.fromISO('2020-06-02T10:00:01.000')
        }
        const comparator = new DateComparator()

        expect(comparator.compare(a, b)).toBe(0)
      })
    })
  })
})
