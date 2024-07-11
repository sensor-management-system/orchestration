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

import { PermissionGroup } from '@/models/PermissionGroup'
import { PermissionGroupSerializer } from '@/serializers/jsonapi/PermissionGroupSerializer'

export class PermissionGroupApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: PermissionGroupSerializer
  private cachedItems: PermissionGroup[] = []

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    this.axiosApi = axiosInstance
    this.basePath = basePath
    this.serializer = new PermissionGroupSerializer()
  }

  async findAll (useFrontendCache: boolean = false, skipBackendCache: boolean = false): Promise<PermissionGroup[]> {
    const response = await this.axiosApi.get(this.basePath, { params: { skip_cache: skipBackendCache } })
    if (useFrontendCache && this.cachedItems.length) {
      return this.cachedItems
    }
    this.cachedItems = this.serializer.convertJsonApiObjectListToModelList(response.data)
    return this.cachedItems
  }
}
