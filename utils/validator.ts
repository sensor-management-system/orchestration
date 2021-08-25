import { LocationType } from '@/models/Location'
import { Configuration } from '@/models/Configuration'

export default {
  validateInputForStartDate (configuration: Configuration): (v:string) => (boolean | string) {
    return (v) => {
      if (v === null || v === '' || configuration.startDate === null) {
        return true
      }
      if (!configuration.endDate) {
        return true
      }
      if (configuration.startDate <= configuration.endDate) {
        return true
      }
      return 'Start date must not be after end date'
    }
  },

  validateInputForEndDate (configuration: Configuration): (v:string) => (boolean | string) {
    return (v) => {
      if (v === null || v === '' || configuration.endDate === null) {
        return true
      }
      if (!configuration.startDate) {
        return true
      }
      if (configuration.endDate >= configuration.startDate) {
        return true
      }
      return 'End date must not be before start date'
    }
  },

  validateInputForLocationType (v: string): boolean | string {
    if (v === LocationType.Stationary) {
      return true
    }
    if (v === LocationType.Dynamic) {
      return true
    }
    return 'Location type must be set'
  },

  mustBeProvided (fieldname: string): (v: any) => boolean | string {
    return function (v: any) {
      if (v == null || v === '') {
        return fieldname + ' must be provided'
      }
      return true
    }
  }
}
