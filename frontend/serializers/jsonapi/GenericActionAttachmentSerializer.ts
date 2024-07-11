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
import { ConfigurationAttachmentSerializer } from '@/serializers/jsonapi/ConfigurationAttachmentSerializer'

export class GenericDeviceActionAttachmentSerializer extends AbstractActionAttachmentSerializer {
  private _attachmentSerializer: IAttachmentSerializer

  constructor () {
    super()
    this._attachmentSerializer = new DeviceAttachmentSerializer()
  }

  getActionTypeName (): string {
    return 'generic_device_action'
  }

  getActionAttachmentTypeName (): string {
    return 'generic_device_action_attachment'
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

export class GenericPlatformActionAttachmentSerializer extends AbstractActionAttachmentSerializer {
  private _attachmentSerializer: IAttachmentSerializer

  constructor () {
    super()
    this._attachmentSerializer = new PlatformAttachmentSerializer()
  }

  getActionTypeName (): string {
    return 'generic_platform_action'
  }

  getActionAttachmentTypeName (): string {
    return 'generic_platform_action_attachment'
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

export class GenericConfigurationActionAttachmentSerializer extends AbstractActionAttachmentSerializer {
  private _attachmentSerializer: IAttachmentSerializer

  constructor () {
    super()
    this._attachmentSerializer = new ConfigurationAttachmentSerializer()
  }

  getActionTypeName (): string {
    return 'generic_configuration_action'
  }

  getActionAttachmentTypeName (): string {
    return 'generic_configuration_action_attachment'
  }

  getActionAttachmentTypeNamePlural (): string {
    return this.getActionAttachmentTypeName() + 's'
  }

  getAttachmentTypeName (): string {
    return 'configuration_attachment'
  }

  get attachmentSerializer (): IAttachmentSerializer {
    return this._attachmentSerializer
  }
}
