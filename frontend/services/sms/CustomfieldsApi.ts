/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2021 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

import { CustomTextField } from '@/models/CustomTextField'
import {
  CustomTextFieldSerializer,
  CustomTextFieldRelationEntityType
} from '@/serializers/jsonapi/CustomTextFieldSerializer'
import { IJsonApiEntityWithOptionalId } from '@/serializers/jsonapi/JsonApiTypes'

export class CustomfieldsApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: CustomTextFieldSerializer

  constructor (axiosInstance: AxiosInstance, basePath: string, serializer: CustomTextFieldSerializer) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
    this.serializer = serializer
  }

  findById (id: string): Promise<CustomTextField> {
    return this.axiosApi.get(this.basePath + '/' + id, {
      // params: {}
    }).then((rawResponse) => {
      const rawData = rawResponse.data
      return this.serializer.convertJsonApiObjectToModel(rawData)
    })
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }

  addWithRelation (entityId: string, entityType: CustomTextFieldRelationEntityType, field: CustomTextField): Promise<CustomTextField> {
    const url = this.basePath
    const data: IJsonApiEntityWithOptionalId = this.serializer.convertModelToJsonApiData(
      field,
      {
        entityType,
        id: entityId
      }
    )
    return this.axiosApi.post(url, { data }).then((serverResponse) => {
      return this.serializer.convertJsonApiObjectToModel(serverResponse.data)
    })
  }

  updateWithRelation (entityId: string, entityType: CustomTextFieldRelationEntityType, field: CustomTextField): Promise<CustomTextField> {
    return new Promise<string>((resolve, reject) => {
      if (field.id) {
        resolve(field.id)
      } else {
        reject(new Error('no id for the CustomTextField'))
      }
    }).then((fieldId) => {
      const data: IJsonApiEntityWithOptionalId = this.serializer.convertModelToJsonApiData(
        field,
        {
          entityType,
          id: entityId
        }
      )
      return this.axiosApi.patch(this.basePath + '/' + fieldId, { data }).then((serverResponse) => {
        return this.serializer.convertJsonApiObjectToModel(serverResponse.data)
      })
    })
  }
}
