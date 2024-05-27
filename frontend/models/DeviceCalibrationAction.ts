/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'
import { Attachment } from '@/models/Attachment'
import { Contact } from '@/models/Contact'
import { DeviceProperty } from '@/models/DeviceProperty'
import { IActionCommonDetails, ActionCommonDetails } from '@/models/ActionCommonDetails'
import { IDateCompareable } from '@/modelUtils/Compareables'
import { IActionKind, KIND_OF_ACTION_TYPE_DEVICE_CALIBRATION } from '@/models/ActionKind'

export interface IDeviceCalibrationAction extends IActionCommonDetails {
  currentCalibrationDate: DateTime | null
  nextCalibrationDate: DateTime | null
  formula: string
  value: number | null
  measuredQuantities: DeviceProperty[]
}

export class DeviceCalibrationAction extends ActionCommonDetails implements IDeviceCalibrationAction, IDateCompareable, IActionKind {
  private _currentCalibrationDate: DateTime | null = null
  private _nextCalibrationDate: DateTime | null = null
  private _formula: string = ''
  private _value: number | null = null
  private _measuredQuantities: DeviceProperty[] = []

  static createEmpty () {
    return new DeviceCalibrationAction()
  }

  static createFromObject (someObject: IDeviceCalibrationAction): DeviceCalibrationAction {
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

  get currentCalibrationDate (): DateTime | null {
    return this._currentCalibrationDate
  }

  set currentCalibrationDate (newDate: DateTime | null) {
    this._currentCalibrationDate = newDate
  }

  get nextCalibrationDate (): DateTime | null {
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

  get value (): number | null {
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

  get icon (): string {
    return 'mdi-compass'
  }

  get color (): string {
    return 'teal'
  }

  get kind (): string {
    return KIND_OF_ACTION_TYPE_DEVICE_CALIBRATION
  }
}
