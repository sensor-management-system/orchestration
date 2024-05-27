/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'

export interface IExportControl {
  id: string
  dualUse: boolean | null
  exportControlClassificationNumber: string
  customsTariffNumber: string
  additionalInformation: string
  internalNote: string
  createdAt: DateTime | null
  updatedAt: DateTime | null
  createdByUserId: string | null
  updatedByUserId: string | null
  manufacturerModelId: string | null
}

export class ExportControl implements IExportControl {
  private _id: string = ''
  private _dualUse: boolean | null = null
  private _exportControlClassificationNumber: string = ''
  private _customsTariffNumber: string = ''
  private _additionalInformation: string = ''
  private _internalNote: string = ''

  private _createdAt: DateTime | null = null
  private _updatedAt: DateTime | null = null

  private _createdByUserId: string | null = null
  private _updatedByUserId: string | null = null
  private _manufacturerModelId: string | null = null

  get id (): string {
    return this._id
  }

  set id (newId: string) {
    this._id = newId
  }

  get dualUse (): boolean | null {
    return this._dualUse
  }

  set dualUse (newDualUse: boolean | null) {
    this._dualUse = newDualUse
  }

  get exportControlClassificationNumber (): string {
    return this._exportControlClassificationNumber
  }

  set exportControlClassificationNumber (newExportControlClassificationNumber: string) {
    this._exportControlClassificationNumber = newExportControlClassificationNumber
  }

  get customsTariffNumber (): string {
    return this._customsTariffNumber
  }

  set customsTariffNumber (newCustomsTariffNumber: string) {
    this._customsTariffNumber = newCustomsTariffNumber
  }

  get additionalInformation (): string {
    return this._additionalInformation
  }

  set additionalInformation (newAdditionalInformation: string) {
    this._additionalInformation = newAdditionalInformation
  }

  get internalNote (): string {
    return this._internalNote
  }

  set internalNote (newInternalNote: string) {
    this._internalNote = newInternalNote
  }

  get createdAt (): DateTime | null {
    return this._createdAt
  }

  set createdAt (newCreatedAt: DateTime | null) {
    this._createdAt = newCreatedAt
  }

  get updatedAt (): DateTime | null {
    return this._updatedAt
  }

  set updatedAt (newUpdatedAt: DateTime | null) {
    this._updatedAt = newUpdatedAt
  }

  get createdByUserId (): string | null {
    return this._createdByUserId
  }

  set createdByUserId (newId: string | null) {
    this._createdByUserId = newId
  }

  get updatedByUserId (): string | null {
    return this._updatedByUserId
  }

  set updatedByUserId (newId: string | null) {
    this._updatedByUserId = newId
  }

  get manufacturerModelId (): string | null {
    return this._manufacturerModelId
  }

  set manufacturerModelId (newManufacturerModelId: string | null) {
    this._manufacturerModelId = newManufacturerModelId
  }

  static createFromObject (someObject: IExportControl): ExportControl {
    const newObject = new ExportControl()

    newObject.id = someObject.id
    newObject.dualUse = someObject.dualUse
    newObject.exportControlClassificationNumber = someObject.exportControlClassificationNumber
    newObject.customsTariffNumber = someObject.customsTariffNumber
    newObject.additionalInformation = someObject.additionalInformation
    newObject.internalNote = someObject.internalNote

    newObject.createdAt = someObject.createdAt
    newObject.updatedAt = someObject.updatedAt
    newObject.createdByUserId = someObject.createdByUserId
    newObject.updatedByUserId = someObject.updatedByUserId

    newObject.manufacturerModelId = someObject.manufacturerModelId

    return newObject
  }
}
