/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2023
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
  label: string
  description: string
  project: string
  status: string
  archived: boolean
}

export class ConfigurationBasicData implements IConfigurationBasicData {
  private _id: string = ''
  private _startDate: DateTime | null = null
  private _endDate: DateTime | null = null
  private _label: string = ''
  private _description: string = ''
  private _project: string = ''
  private _status: string = ''
  private _archived: boolean = false

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

  get label (): string {
    return this._label
  }

  set label (newLabel: string) {
    this._label = newLabel
  }

  get description (): string {
    return this._description
  }

  set description (newDescription: string) {
    this._description = newDescription
  }

  get project (): string {
    return this._project
  }

  set project (newProject: string) {
    this._project = newProject
  }

  get status (): string {
    return this._status
  }

  set status (newStatus: string) {
    this._status = newStatus
  }

  get archived (): boolean {
    return this._archived
  }

  set archived (newValue: boolean) {
    this._archived = newValue
  }

  static createFromObject (someObject: IConfigurationBasicData): ConfigurationBasicData {
    const newObject = new ConfigurationBasicData()

    newObject.id = someObject.id
    newObject.startDate = someObject.startDate
    newObject.endDate = someObject.endDate

    newObject.label = someObject.label
    newObject.description = someObject.description
    newObject.project = someObject.project
    newObject.status = someObject.status
    newObject.archived = someObject.archived

    return newObject
  }
}
