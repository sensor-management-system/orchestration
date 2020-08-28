// eslint-disable-next-line
import { AxiosInstance, Method } from 'axios'

import { Configuration } from '@/models/Configuration'

// eslint-disable-next-line
import { IFlaskJSONAPIFilter } from '@/utils/JSONApiInterfaces'

import {
  // eslint-disable-next-line
  IPaginationLoader, FilteredPaginationedLoader
} from '@/utils/PaginatedLoader'

export default class ConfigurationApi {
  private axiosApi: AxiosInstance

  constructor (axiosInstance: AxiosInstance) {
    this.axiosApi = axiosInstance
  }

  findById (id: string): Promise<Configuration> {
    return new Promise((resolve) => {
      const configuration = this._createDemoConfiguration()
      configuration.id = parseInt(id)
      resolve(configuration)
    })
  }

  // eslint-disable-next-line
  deleteById (id: number) : Promise<void> {
    return new Promise((resolve) => {
      resolve()
    })
  }

  save (configuration: Configuration): Promise<Configuration> {
    return new Promise((resolve) => {
      resolve(configuration)
    })
  }

  _createDemoConfiguration (): Configuration {
    return new Configuration()
  }
}

// eslint-disable-next-line
export function serverResponseToEntity (entry: any) : Configuration {
  throw new Error('not implemented')
}
