/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

import { UserInfo } from '@/models/UserInfo'
import { UserInfoSerializer } from '@/serializers/jsonapi/UserInfoSerializer'

export class UserInfoApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: UserInfoSerializer

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
    this.serializer = new UserInfoSerializer()
  }

  async get (skipBackendCache: boolean = false): Promise<UserInfo> {
    const response = await this.axiosApi.get(this.basePath, { params: { skip_cache: skipBackendCache } })
    return this.serializer.convertJsonApiObjectToModel(response.data)
  }
}
