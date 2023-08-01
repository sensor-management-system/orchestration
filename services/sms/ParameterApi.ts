/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2021-2023
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

import { HTTP409ConflictError } from '@/services/HTTPErrors'
import { Parameter } from '@/models/Parameter'
import { ParameterSerializer, ParameterRelationEntityType } from '@/serializers/jsonapi/ParameterSerializer'
import { IJsonApiEntityWithOptionalId } from '@/serializers/jsonapi/JsonApiTypes'

export class ParameterApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: ParameterSerializer

  constructor (axiosInstance: AxiosInstance, basePath: string, serializer: ParameterSerializer) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
    this.serializer = serializer
  }

  async findById (id: string): Promise<Parameter> {
    const response = await this.axiosApi.get(this.basePath + '/' + id)
    return this.serializer.convertJsonApiObjectToModel(response.data)
  }

  async deleteById (id: string): Promise<void> {
    try {
      await this.axiosApi.delete<string, void>(this.basePath + '/' + id)
    } catch (error) {
      if (error.response.status === 409) {
        throw new HTTP409ConflictError(error.message)
      }
      throw error
    }
  }

  async addWithRelation (entityId: string, entityType: ParameterRelationEntityType, parameter: Parameter): Promise<Parameter> {
    const url = this.basePath
    const data: IJsonApiEntityWithOptionalId = this.serializer.convertModelToJsonApiData(
      parameter,
      {
        entityType,
        id: entityId
      }
    )
    const response = await this.axiosApi.post(url, { data })
    return this.serializer.convertJsonApiObjectToModel(response.data)
  }

  async updateWithRelation (entityId: string, entityType: ParameterRelationEntityType, parameter: Parameter): Promise<Parameter> {
    if (!parameter.id) {
      throw new Error('property id of parameter must not be empty')
    }
    const data: IJsonApiEntityWithOptionalId = this.serializer.convertModelToJsonApiData(
      parameter,
      {
        entityType,
        id: entityId
      }
    )
    const response = await this.axiosApi.patch(this.basePath + '/' + parameter.id, { data })
    return this.serializer.convertJsonApiObjectToModel(response.data)
  }
}
