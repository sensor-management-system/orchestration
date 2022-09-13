/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2022
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

import { DeviceMountActionBasicData } from '@/models/basic/DeviceMountActionBasicData'
import { ConfigurationBasicData } from '@/models/basic/ConfigurationBasicData'
import { ContactBasicData } from '@/models/basic/ContactBasicData'
import { PlatformBasicData } from '@/models/basic/PlatformBasicData'
import { IDateCompareable } from '@/modelUtils/Compareables'

export interface IDeviceMountAction {
  basicData: DeviceMountActionBasicData
  configuration: ConfigurationBasicData
  beginContact: ContactBasicData
  endContact: ContactBasicData | null
  parentPlatform: PlatformBasicData | null
}

export class DeviceMountAction implements IDeviceMountAction, IDateCompareable {
  private _basicData: DeviceMountActionBasicData
  private _configuration: ConfigurationBasicData
  private _beginContact: ContactBasicData
  private _endContact: ContactBasicData | null
  private _parentPlatform: PlatformBasicData | null

  constructor (basicData: DeviceMountActionBasicData,
    configuration: ConfigurationBasicData,
    beginContact: ContactBasicData,
    endContact: ContactBasicData | null,
    parentPlatform: PlatformBasicData | null
  ) {
    this._basicData = basicData
    this._configuration = configuration
    this._beginContact = beginContact
    this._endContact = endContact
    this._parentPlatform = parentPlatform
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

  get date () {
    return this._basicData.beginDate
  }

  static createFromObject (otherAction: IDeviceMountAction): DeviceMountAction {
    return new DeviceMountAction(
      DeviceMountActionBasicData.createFromObject(otherAction.basicData),
      ConfigurationBasicData.createFromObject(otherAction.configuration),
      ContactBasicData.createFromObject(otherAction.beginContact),
      otherAction.endContact == null ? null : ContactBasicData.createFromObject(otherAction.endContact),
      otherAction.parentPlatform === null ? null : PlatformBasicData.createFromObject(otherAction.parentPlatform)
    )
  }
}
