import { dateToString, stringToDate } from '@/utils/dateHelper'

describe('dateToString', () => {
  it('should work with by birthday', () => {
    const date = new Date('1990-09-18')
    const result = dateToString(date)

    expect(result).toBe('1990-09-18')
  })
  it('should also work with the date on that I write the tests', () => {
    const date = new Date('2020-09-25')
    const result = dateToString(date)

    expect(result).toBe('2020-09-25')
  })
})

describe('stringToDate', () => {
  it('should work with by birthday', () => {
    const day = '1990-09-18'
    const result = stringToDate(day)

    expect(result.getFullYear()).toBe(1990)
    expect(result.getMonth()).toBe(8) // it has a zero based count for months
    expect(result.getDate()).toBe(18)
  })
  it('should also work with the date on that I write the tests', () => {
    const day = '2020-09-25'
    const result = stringToDate(day)

    expect(result.getFullYear()).toBe(2020)
    expect(result.getMonth()).toBe(8) // it has a zero based count for months
    expect(result.getDate()).toBe(25)
  })
})

describe('stringToDate and dateToString', () => {
  const they = it
  they('should should work together', () => {
    const inputValue = '2020-09-25'
    const asDate = stringToDate(inputValue)
    const asStr = dateToString(asDate)

    expect(asStr).toBe(inputValue)
  })
})
