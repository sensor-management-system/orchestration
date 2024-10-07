/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { AxiosInstance } from 'axios'
import { TsmLinkingInvolvedDevice } from '@/models/TsmLinkingInvolvedDevice'
import { TsmLinkingInvolvedDeviceSerializer } from '@/serializers/jsonapi/TsmLinkingInvolvedDeviceSerializer'

export class TsmLinkingInvolvedDeviceApi {
  private axiosApi: AxiosInstance
  readonly basePath: string
  private serializer: TsmLinkingInvolvedDeviceSerializer

  constructor (axiosApi: AxiosInstance, basePath: string) {
    this.axiosApi = axiosApi
    this.basePath = basePath
    this.serializer = new TsmLinkingInvolvedDeviceSerializer()
  }

  async add (involvedDevice: TsmLinkingInvolvedDevice, tsmLinkingId: string) {
    const data = this.serializer.convertModelToJsonApiData(involvedDevice, tsmLinkingId)
    const url = this.basePath
    return await this.axiosApi.post(url, { data })
  }

  async update (involvedDevice: TsmLinkingInvolvedDevice, tsmLinkingId: string) {
    const data = this.serializer.convertModelToJsonApiData(involvedDevice, tsmLinkingId)
    const url = this.basePath + '/' + involvedDevice.id
    return await this.axiosApi.patch(url, { data })
  }

  async delete (involvedDevice: TsmLinkingInvolvedDevice) {
    const url = this.basePath + '/' + involvedDevice.id
    return await this.axiosApi.delete(url)
  }
}
