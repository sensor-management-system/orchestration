/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
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
import { DateTime } from 'luxon'
import { Attachment } from '@/models/Attachment'
import { Contact } from '@/models/Contact'
import { DeviceProperty } from '@/models/DeviceProperty'
import { IActionCommonDetails, ActionCommonDetails } from '@/models/ActionCommonDetails'
import { IDateCompareable } from '@/modelUtils/Compareables'

export interface IDeviceCalibrationAction extends IActionCommonDetails {
  currentCalibrationDate: DateTime | null
  nextCalibrationDate: DateTime | null
  formula: string
  value: number | null
  measuredQuantities: DeviceProperty[]
}

export class DeviceCalibrationAction extends ActionCommonDetails implements IDeviceCalibrationAction, IDateCompareable {
  private _currentCalibrationDate: DateTime | null = null
  private _nextCalibrationDate: DateTime | null = null
  private _formula: string = ''
  private _value: number | null = null
  private _measuredQuantities: DeviceProperty[] = []

  static createEmpty () {
    return new DeviceCalibrationAction()
  }

  static createFromObject (someObject: IDeviceCalibrationAction) : DeviceCalibrationAction {
    const action = new DeviceCalibrationAction()
    action.id = someObject.id
    action.currentCalibrationDate = someObject.currentCalibrationDate
    action.nextCalibrationDate = someObject.nextCalibrationDate
    action.formula = someObject.formula
    action.value = someObject.value
    action.measuredQuantities = someObject.measuredQuantities.map((m: DeviceProperty) => DeviceProperty.createFromObject(m))
    action.description = someObject.description
    action.contact = someObject.contact ? Contact.createFromObject(someObject.contact) : null
    action.attachments = someObject.attachments.map((a: Attachment) => Attachment.createFromObject(a))
    return action
  }

  get currentCalibrationDate () : DateTime | null {
    return this._currentCalibrationDate
  }

  set currentCalibrationDate (newDate: DateTime | null) {
    this._currentCalibrationDate = newDate
  }

  get nextCalibrationDate () : DateTime | null {
    return this._nextCalibrationDate
  }

  set nextCalibrationDate (newDate: DateTime | null) {
    this._nextCalibrationDate = newDate
  }

  get formula (): string {
    return this._formula
  }

  set formula (newFormula: string) {
    this._formula = newFormula
  }

  get value () : number | null {
    return this._value
  }

  set value (newValue: number | null) {
    this._value = newValue
  }

  get measuredQuantities (): DeviceProperty[] {
    return this._measuredQuantities
  }

  set measuredQuantities (newMeasuredQuantities: DeviceProperty[]) {
    this._measuredQuantities = newMeasuredQuantities
  }

  get isDeviceCalibrationAction (): boolean {
    return true
  }

  get date (): DateTime | null {
    return this.currentCalibrationDate
  }
}
