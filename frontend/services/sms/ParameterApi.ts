/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2021 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import axios, { AxiosInstance } from 'axios'

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
      if (axios.isAxiosError(error)) {
        if (error.response?.status === 409) {
          throw new HTTP409ConflictError(error.message)
        }
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
