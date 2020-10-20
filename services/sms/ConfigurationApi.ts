/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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

// eslint-disable-next-line
import { AxiosInstance, Method } from 'axios'

import { Configuration } from '@/models/Configuration'

// eslint-disable-next-line
import { IFlaskJSONAPIFilter } from '@/utils/JSONApiInterfaces'

import {
  // eslint-disable-next-line
  IPaginationLoader, FilteredPaginationedLoader
} from '@/utils/PaginatedLoader'

export class ConfigurationApi {
  private axiosApi: AxiosInstance

  constructor (axiosInstance: AxiosInstance) {
    this.axiosApi = axiosInstance
  }

  findById (id: string): Promise<Configuration> {
    return new Promise((resolve) => {
      const configuration = this._createDemoConfiguration()
      configuration.id = id
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
