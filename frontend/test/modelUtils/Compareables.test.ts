/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
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
