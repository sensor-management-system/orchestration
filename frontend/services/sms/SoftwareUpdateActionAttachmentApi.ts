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

import { IActionAttachmentSerializer } from '@/serializers/jsonapi/ActionAttachmentSerializer'
import { DeviceSoftwareUpdateActionAttachmentSerializer, PlatformSoftwareUpdateActionAttachmentSerializer } from '@/serializers/jsonapi/SoftwareUpdateActionAttachmentSerializer'
import { AbstractActionAttachmentApi } from '@/services/sms/ActionAttachmentApi'

export class DeviceSoftwareUpdateActionAttachmentApi extends AbstractActionAttachmentApi {
  private _serializer: IActionAttachmentSerializer

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance, basePath)
    this._serializer = new DeviceSoftwareUpdateActionAttachmentSerializer()
  }

  get serializer (): IActionAttachmentSerializer {
    return this._serializer
  }
}

export class PlatformSoftwareUpdateActionAttachmentApi extends AbstractActionAttachmentApi {
  private _serializer: IActionAttachmentSerializer

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance, basePath)
    this._serializer = new PlatformSoftwareUpdateActionAttachmentSerializer()
  }

  get serializer (): IActionAttachmentSerializer {
    return this._serializer
  }
}
