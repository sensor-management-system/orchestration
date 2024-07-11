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

export interface IConfigurationBasicData {
  id: string
  startDate: DateTime | null
  endDate: DateTime | null
  label: string
  description: string
  project: string
  campaign: string
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
  private _campaign: string = ''
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

  get campaign (): string {
    return this._campaign
  }

  set campaign (newCampaign: string) {
    this._campaign = newCampaign
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
    newObject.campaign = someObject.campaign
    newObject.status = someObject.status
    newObject.archived = someObject.archived

    return newObject
  }
}
