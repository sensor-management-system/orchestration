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
