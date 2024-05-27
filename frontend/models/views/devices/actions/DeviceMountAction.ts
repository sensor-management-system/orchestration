/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DeviceMountActionBasicData } from '@/models/basic/DeviceMountActionBasicData'
import { ConfigurationBasicData } from '@/models/basic/ConfigurationBasicData'
import { ContactBasicData } from '@/models/basic/ContactBasicData'
import { PlatformBasicData } from '@/models/basic/PlatformBasicData'
import { IDateCompareable } from '@/modelUtils/Compareables'
import { DeviceBasicData } from '@/models/basic/DeviceBasicData'

export interface IDeviceMountAction {
  basicData: DeviceMountActionBasicData
  configuration: ConfigurationBasicData
  beginContact: ContactBasicData
  endContact: ContactBasicData | null
  parentPlatform: PlatformBasicData | null
  parentDevice: DeviceBasicData | null
}

export class DeviceMountAction implements IDeviceMountAction, IDateCompareable {
  private _basicData: DeviceMountActionBasicData
  private _configuration: ConfigurationBasicData
  private _beginContact: ContactBasicData
  private _endContact: ContactBasicData | null
  private _parentPlatform: PlatformBasicData | null
  private _parentDevice: DeviceBasicData | null

  constructor (basicData: DeviceMountActionBasicData,
    configuration: ConfigurationBasicData,
    beginContact: ContactBasicData,
    endContact: ContactBasicData | null,
    parentPlatform: PlatformBasicData | null,
    parentDevice: DeviceBasicData | null
  ) {
    this._basicData = basicData
    this._configuration = configuration
    this._beginContact = beginContact
    this._endContact = endContact
    this._parentPlatform = parentPlatform
    this._parentDevice = parentDevice
  }

  get basicData (): DeviceMountActionBasicData {
    return this._basicData
  }

  get configuration (): ConfigurationBasicData {
    return this._configuration
  }

  get beginContact (): ContactBasicData {
    return this._beginContact
  }

  get endContact (): ContactBasicData | null {
    return this._endContact
  }

  get parentPlatform (): PlatformBasicData | null {
    return this._parentPlatform
  }

  get parentDevice (): DeviceBasicData | null {
    return this._parentDevice
  }

  get date () {
    return this._basicData.beginDate
  }

  static createFromObject (otherAction: IDeviceMountAction): DeviceMountAction {
    return new DeviceMountAction(
      DeviceMountActionBasicData.createFromObject(otherAction.basicData),
      ConfigurationBasicData.createFromObject(otherAction.configuration),
      ContactBasicData.createFromObject(otherAction.beginContact),
      otherAction.endContact == null ? null : ContactBasicData.createFromObject(otherAction.endContact),
      otherAction.parentPlatform === null ? null : PlatformBasicData.createFromObject(otherAction.parentPlatform),
      otherAction.parentDevice === null ? null : DeviceBasicData.createFromObject(otherAction.parentDevice)
    )
  }
}
