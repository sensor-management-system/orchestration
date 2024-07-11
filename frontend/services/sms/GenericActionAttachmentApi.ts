/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { AxiosInstance } from 'axios'

import { IActionAttachmentSerializer } from '@/serializers/jsonapi/ActionAttachmentSerializer'
import { GenericDeviceActionAttachmentSerializer, GenericPlatformActionAttachmentSerializer, GenericConfigurationActionAttachmentSerializer } from '@/serializers/jsonapi/GenericActionAttachmentSerializer'
import { AbstractActionAttachmentApi } from '@/services/sms/ActionAttachmentApi'

export class GenericDeviceActionAttachmentApi extends AbstractActionAttachmentApi {
  private _serializer: IActionAttachmentSerializer

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance, basePath)
    this._serializer = new GenericDeviceActionAttachmentSerializer()
  }

  get serializer (): IActionAttachmentSerializer {
    return this._serializer
  }
}

export class GenericPlatformActionAttachmentApi extends AbstractActionAttachmentApi {
  private _serializer: IActionAttachmentSerializer

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance, basePath)
    this._serializer = new GenericPlatformActionAttachmentSerializer()
  }

  get serializer (): IActionAttachmentSerializer {
    return this._serializer
  }
}

export class GenericConfigurationActionAttachmentApi extends AbstractActionAttachmentApi {
  private _serializer: IActionAttachmentSerializer

  constructor (axiosInstance: AxiosInstance, basePath: string) {
    super(axiosInstance, basePath)
    this._serializer = new GenericConfigurationActionAttachmentSerializer()
  }

  get serializer (): IActionAttachmentSerializer {
    return this._serializer
  }
}
