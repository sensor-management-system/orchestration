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
import { AxiosInstance } from 'axios'

import { Manufacturer } from '@/models/Manufacturer'
import { ManufacturerSerializer } from '@/serializers/jsonapi/ManufacturerSerializer'

export class ManufacturerApi {
  private axiosApi: AxiosInstance
  private serializer: ManufacturerSerializer

  constructor (axiosInstance: AxiosInstance) {
    this.axiosApi = axiosInstance
    this.serializer = new ManufacturerSerializer()
  }

  newSearchBuilder (): ManufacturerSearchBuilder {
    return new ManufacturerSearchBuilder(this.axiosApi, this.serializer)
  }

  findAll (): Promise<Manufacturer[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export class ManufacturerSearchBuilder {
  private axiosApi: AxiosInstance
  private serializer: ManufacturerSerializer

  constructor (axiosApi: AxiosInstance, serializer: ManufacturerSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
  }

  build (): ManufacturerSearcher {
    return new ManufacturerSearcher(this.axiosApi, this.serializer)
  }
}

export class ManufacturerSearcher {
  private axiosApi: AxiosInstance
  private serializer: ManufacturerSerializer

  constructor (axiosApi: AxiosInstance, serializer: ManufacturerSerializer) {
    this.axiosApi = axiosApi
    this.serializer = serializer
  }

  findMatchingAsList (): Promise<Manufacturer[]> {
    return this.axiosApi.get(
      '',
      {
        params: {
          'page[size]': 10000,
          'filter[status.icontains]': 'ACCEPTED',
          sort: 'term'
        }
      }
    ).then((rawResponse) => {
      const response = rawResponse.data
      return this.serializer.convertJsonApiObjectListToModelList(response)
    })
  }
}
