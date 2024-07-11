/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2021 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

export interface IUploadResult {
  message: string
  url: string
}

export class UploadApi {
  private axiosApi: AxiosInstance
  readonly basePath: string

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
  }

  async file (file: File, fileName?: string): Promise<IUploadResult> {
    const url = this.basePath
    const formData = new FormData()
    formData.append('file', file, fileName)
    const result = await this.axiosApi.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return result.data as IUploadResult
  }

  async blob (blob: Blob, fileName?: string): Promise<IUploadResult> {
    const url = this.basePath
    const formData = new FormData()
    formData.append('file', blob, fileName)
    const result = await this.axiosApi.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return result.data as IUploadResult
  }
}
