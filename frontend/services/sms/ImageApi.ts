/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
