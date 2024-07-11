/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2021 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

import { ParameterChangeAction } from '@/models/ParameterChangeAction'
import { ParameterChangeActionSerializer, ParameterChangeActionRelationEntityType } from '@/serializers/jsonapi/ParameterChangeActionSerializer'
import { IJsonApiEntityWithOptionalId } from '@/serializers/jsonapi/JsonApiTypes'

export class ParameterChangeActionApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: ParameterChangeActionSerializer

  constructor (axiosInstance: AxiosInstance, basePath: string, serializer: ParameterChangeActionSerializer) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
    this.serializer = serializer
  }

  async findByIdWithRelation (id: string, entityType: ParameterChangeActionRelationEntityType): Promise<ParameterChangeAction> {
    const params = {
      include: [
        'contact',
        entityType
      ].join(',')
    }
    const response = await this.axiosApi.get(this.basePath + '/' + id, { params })
    return this.serializer.convertJsonApiObjectToModel(response.data)
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }

  async addWithRelation (entityId: string, entityType: ParameterChangeActionRelationEntityType, parameterChangeAction: ParameterChangeAction): Promise<ParameterChangeAction> {
    const url = this.basePath
    const data: IJsonApiEntityWithOptionalId = this.serializer.convertModelToJsonApiData(
      parameterChangeAction,
      {
        entityType,
        id: entityId
      }
    )
    const response = await this.axiosApi.post(url, { data })
    return this.serializer.convertJsonApiObjectToModel(response.data)
  }

  async updateWithRelation (entityId: string, entityType: ParameterChangeActionRelationEntityType, parameterChangeAction: ParameterChangeAction): Promise<ParameterChangeAction> {
    if (!parameterChangeAction.id) {
      throw new Error('property id of parameterChangeAction must not be empty')
    }
    const data: IJsonApiEntityWithOptionalId = this.serializer.convertModelToJsonApiData(
      parameterChangeAction,
      {
        entityType,
        id: entityId
      }
    )
    const response = await this.axiosApi.patch(this.basePath + '/' + parameterChangeAction.id, { data })
    return this.serializer.convertJsonApiObjectToModel(response.data)
  }
}
