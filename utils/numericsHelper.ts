export const parseFloatOrDefault = (value: any, defaultValue: number | null = null) => isNaN(parseFloat(value)) ? defaultValue : parseFloat(value)
export const parseIntOrDefault = (value: any, defaultValue: number | null = null) => isNaN(parseInt(value)) ? defaultValue : parseInt(value)
