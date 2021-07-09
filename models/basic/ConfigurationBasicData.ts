/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2021
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

export interface IConfigurationBasicData {
  id: string
  startDate: DateTime | null
  endDate: DateTime | null
  projectUri: string
  projectName: string
  label: string
  status: string
}

export class ConfigurationBasicData implements IConfigurationBasicData {
  private _id: string = ''
  private _startDate: DateTime | null = null
  private _endDate: DateTime | null = null
  private _projectUri: string = ''
  private _projectName: string = ''
  private _label: string = ''
  private _status: string = ''

  get id (): string {
    return this._id
  }

  set id (id: string) {
    this._id = id
  }

  get startDate (): DateTime | null {
    return this._startDate
  }

  set startDate (date: DateTime | null) {
    this._startDate = date
  }

  get endDate (): DateTime | null {
    return this._endDate
  }

  set endDate (date: DateTime | null) {
    this._endDate = date
  }

  get projectName (): string {
    return this._projectName
  }

  set projectName (newProjectName: string) {
    this._projectName = newProjectName
  }

  get projectUri (): string {
    return this._projectUri
  }

  set projectUri (newProjectUri: string) {
    this._projectUri = newProjectUri
  }

  get label (): string {
    return this._label
  }

  set label (newLabel: string) {
    this._label = newLabel
  }

  get status (): string {
    return this._status
  }

  set status (newStatus: string) {
    this._status = newStatus
  }

  static createFromObject (someObject: IConfigurationBasicData): ConfigurationBasicData {
    const newObject = new ConfigurationBasicData()

    newObject.id = someObject.id
    newObject.startDate = someObject.startDate
    newObject.endDate = someObject.endDate

    newObject.projectName = someObject.projectName
    newObject.projectUri = someObject.projectUri

    newObject.label = someObject.label
    newObject.status = someObject.status

    return newObject
  }
}
