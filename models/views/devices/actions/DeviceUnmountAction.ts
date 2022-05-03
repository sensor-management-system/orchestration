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

import { DeviceUnmountActionBasicData } from '@/models/basic/DeviceUnmountActionBasicData'
import { ConfigurationBasicData } from '@/models/basic/ConfigurationBasicData'
import { ContactBasicData } from '@/models/basic/ContactBasicData'
import { IDateCompareable } from '@/modelUtils/Compareables'

export interface IDeviceUnmountAction {
  basicData: DeviceUnmountActionBasicData
  configuration: ConfigurationBasicData
  contact: ContactBasicData
}

export class DeviceUnmountAction implements IDeviceUnmountAction, IDateCompareable {
  private _basicData: DeviceUnmountActionBasicData
  private _configuration: ConfigurationBasicData
  private _contact: ContactBasicData

  constructor (basicData: DeviceUnmountActionBasicData,
    configuration: ConfigurationBasicData,
    contact: ContactBasicData
  ) {
    this._basicData = basicData
    this._configuration = configuration
    this._contact = contact
  }

  get basicData (): DeviceUnmountActionBasicData {
    return this._basicData
  }

  get configuration (): ConfigurationBasicData {
    return this._configuration
  }

  get contact (): ContactBasicData {
    return this._contact
  }

  get date () {
    return this._basicData.date
  }

  static createFromObject (otherAction: IDeviceUnmountAction): DeviceUnmountAction {
    return new DeviceUnmountAction(
      DeviceUnmountActionBasicData.createFromObject(otherAction.basicData),
      ConfigurationBasicData.createFromObject(otherAction.configuration),
      ContactBasicData.createFromObject(otherAction.contact)
    )
  }
}
