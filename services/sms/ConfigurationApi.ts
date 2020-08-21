import { AxiosInstance, Method } from 'axios'

import Platform from '@/models/Platform'
import Device from '@/models/Device'
import { PlatformNode } from '@/models/PlatformNode'
import { DeviceNode } from '@/models/DeviceNode'
import { Configuration } from '@/models/Configuration'

import { IFlaskJSONAPIFilter } from '@/utils/JSONApiInterfaces'

import {
  IPaginationLoader, FilteredPaginationedLoader
} from '@/utils/PaginatedLoader'

export default class ConfigurationApi {
  private axiosApi: AxiosInstance

  constructor (axiosInstance: AxiosInstance) {
    this.axiosApi = axiosInstance
  }

  findById (id: string): Promise<Configuration> {
    return new Promise((resolve, reject) => {
      const configuration = this._createDemoConfiguration()
      configuration.id = parseInt(id)
      resolve(configuration)
    })
  }

  deleteById (id: number) : Promise<void> {
    return new Promise((resolve, reject) => {
      resolve()
    })
  }

  save (configuration: Configuration): Promise<Configuration> {
    return new Promise((resolve, reject) => {
      resolve(configuration)
    })
  }

  _createDemoConfiguration (): Configuration {
    return new Configuration()
  }
}

export function serverResponseToEntity (entry: any) : Configuration {
  throw new Error('not implemented')
}
