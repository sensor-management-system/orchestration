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
import { DeviceCalibrationActionAttachmentSerializer } from '@/serializers/jsonapi/DeviceCalibrationActionAttachmentSerializer'
import { AbstractActionAttachmentApi } from '@/services/sms/ActionAttachmentApi'

export class DeviceCalibrationActionAttachmentApi extends AbstractActionAttachmentApi {
  private _serializer: IActionAttachmentSerializer

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance, basePath)
    this._serializer = new DeviceCalibrationActionAttachmentSerializer()
  }

  get serializer (): IActionAttachmentSerializer {
    return this._serializer
  }
}
