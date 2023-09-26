/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
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
