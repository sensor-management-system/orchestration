/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2021-2022
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
