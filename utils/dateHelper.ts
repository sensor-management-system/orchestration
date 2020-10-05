export const dateToString = (aDate: Date | null): string => {
  if (!aDate) {
    return ''
  }
  const year = aDate.getFullYear()
  const month = aDate.getMonth() + 1
  const day = aDate.getDate()

  return year + '-' + month.toString().padStart(2, '0') + '-' + day.toString().padStart(2, '0')
}

export const stringToDate = (aDate: string): Date => {
  const newDate: Date = new Date(aDate)
  newDate.setHours(0, 0, 0)
  return newDate
}
