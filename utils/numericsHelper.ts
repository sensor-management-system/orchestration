export const parseFloatOrDefault = (value: any, defaultValue: number | null = null) => isNaN(parseFloat(value)) ? defaultValue : parseFloat(value)
