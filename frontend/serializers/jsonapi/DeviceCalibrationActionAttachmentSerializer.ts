/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2021 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { IAttachmentSerializer } from '@/serializers/jsonapi/AttachmentSerializer'
import { AbstractActionAttachmentSerializer } from '@/serializers/jsonapi/ActionAttachmentSerializer'
import { DeviceAttachmentSerializer } from '@/serializers/jsonapi/DeviceAttachmentSerializer'

export class DeviceCalibrationActionAttachmentSerializer extends AbstractActionAttachmentSerializer {
  private _attachmentSerializer: IAttachmentSerializer

  constructor () {
    super()
    this._attachmentSerializer = new DeviceAttachmentSerializer()
  }

  getActionTypeName (): string {
    return 'device_calibration_action'
  }

  getActionAttachmentTypeName (): string {
    return 'device_calibration_attachment'
  }

  getActionAttachmentTypeNamePlural (): string {
    return this.getActionAttachmentTypeName() + 's'
  }

  getAttachmentTypeName (): string {
    return 'device_attachment'
  }

  get attachmentSerializer (): IAttachmentSerializer {
    return this._attachmentSerializer
  }
}
