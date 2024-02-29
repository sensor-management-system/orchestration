/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2024
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
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

import { ConfigurationImageSerializer, DeviceImageSerializer, IImageSerializer, PlatformImageSerializer, SiteImageSerializer } from '@/serializers/jsonapi/ImageSerializer'
import { Image } from '@/models/Image'

class GenericImageApi {
  private imageSerializer: IImageSerializer
  private axiosApi: AxiosInstance
  private basePath: string

  constructor (axiosInstance: AxiosInstance, basePath: string, imageSerializer: IImageSerializer) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
    this.imageSerializer = imageSerializer
  }

  findById (id: string): Promise<Image> {
    return this.axiosApi.get(this.basePath + '/' + id).then((rawResponse) => {
      const rawData = rawResponse.data
      return this.imageSerializer.convertJsonApiObjectToModel(rawData)
    })
  }

  deleteById (id: string): Promise<void> {
    return this.axiosApi.delete<string, void>(this.basePath + '/' + id)
  }

  add (entityId: string, entityImage: Image): Promise<Image> {
    const data = this.imageSerializer.convertModelToJsonApiData(entityImage, entityId)
    return this.axiosApi.post(this.basePath, { data }).then((serverResponse) => {
      return this.imageSerializer.convertJsonApiObjectToModel(serverResponse.data)
    })
  }

  update (entityId: string, entityImage: Image): Promise<Image> {
    return new Promise<string>((resolve, reject) => {
      if (entityImage.id) {
        resolve(entityImage.id)
      } else {
        reject(new Error('no id for the image'))
      }
    }).then((entityImageId) => {
      const data = this.imageSerializer.convertModelToJsonApiData(entityImage, entityId)
      return this.axiosApi.patch(this.basePath + '/' + entityImageId, { data }).then((serverResponse) => {
        return this.imageSerializer.convertJsonApiObjectToModel(serverResponse.data)
      })
    })
  }
}

export class DeviceImageApi extends GenericImageApi {
  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance, basePath, new DeviceImageSerializer())
  }
}

export class PlatformImageApi extends GenericImageApi {
  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance, basePath, new PlatformImageSerializer())
  }
}

export class ConfigurationImageApi extends GenericImageApi {
  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance, basePath, new ConfigurationImageSerializer())
  }
}

export class SiteImageApi extends GenericImageApi {
  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance, basePath, new SiteImageSerializer())
  }
}
