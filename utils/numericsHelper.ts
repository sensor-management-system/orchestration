export const parseFloatOrDefault = (value: any, defaultValue: number): number => isNaN(parseFloat(value)) ? defaultValue : parseFloat(value)
export const parseFloatOrNull = (value: any): number | null => isNaN(parseFloat(value)) ? null : parseFloat(value)
export const parseIntOrDefault = (value: any, defaultValue: number): number => isNaN(parseInt(value)) ? defaultValue : parseInt(value)
export const parseIntOrNull = (value: any): number | null => isNaN(parseInt(value)) ? null : parseInt(value)
