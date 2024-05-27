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
import { PlatformAttachmentSerializer } from '@/serializers/jsonapi/PlatformAttachmentSerializer'

export class DeviceSoftwareUpdateActionAttachmentSerializer extends AbstractActionAttachmentSerializer {
  private _attachmentSerializer: IAttachmentSerializer

  constructor () {
    super()
    this._attachmentSerializer = new DeviceAttachmentSerializer()
  }

  getActionTypeName (): string {
    return 'device_software_update_action'
  }

  getActionAttachmentTypeName (): string {
    return 'device_software_update_action_attachment'
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

export class PlatformSoftwareUpdateActionAttachmentSerializer extends AbstractActionAttachmentSerializer {
  private _attachmentSerializer: IAttachmentSerializer

  constructor () {
    super()
    this._attachmentSerializer = new PlatformAttachmentSerializer()
  }

  getActionTypeName (): string {
    return 'platform_software_update_action'
  }

  getActionAttachmentTypeName (): string {
    return 'platform_software_update_action_attachment'
  }

  getActionAttachmentTypeNamePlural (): string {
    return this.getActionAttachmentTypeName() + 's'
  }

  getAttachmentTypeName (): string {
    return 'platform_attachment'
  }

  get attachmentSerializer (): IAttachmentSerializer {
    return this._attachmentSerializer
  }
}
