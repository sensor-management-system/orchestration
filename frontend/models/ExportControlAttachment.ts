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
import { IAttachment } from '@/models/Attachment'

export interface IExportControlAttachment extends IAttachment {
  isExportControlOnly: boolean
}

export class ExportControlAttachment implements IExportControlAttachment {
  private _id: string = ''
  private _url: string = ''
  private _label: string = ''
  private _description: string = ''
  private _isUpload: boolean = false
  private _createdAt: DateTime | null = null

  private _isExportControlOnly: boolean = true

  get id (): string {
    return this._id
  }

  set id (newId: string) {
    this._id = newId
  }

  get url (): string {
    return this._url
  }

  set url (newUrl: string) {
    this._url = newUrl
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

  get isUpload (): boolean {
    return this._isUpload
  }

  set isUpload (newIsUpload: boolean) {
    this._isUpload = newIsUpload
  }

  get createdAt (): DateTime | null {
    return this._createdAt
  }

  set createdAt (newCreatedAt: DateTime | null) {
    this._createdAt = newCreatedAt
  }

  get isExportControlOnly (): boolean {
    return this._isExportControlOnly
  }

  set isExportControlOnly (newIsExportControlOnly: boolean) {
    this._isExportControlOnly = newIsExportControlOnly
  }

  static createFromObject (someObject: IExportControlAttachment): ExportControlAttachment {
    const newObject = new ExportControlAttachment()

    newObject.id = someObject.id || ''
    newObject.url = someObject.url
    newObject.label = someObject.label
    newObject.description = someObject.description
    newObject.isUpload = someObject.isUpload
    newObject.createdAt = someObject.createdAt
    newObject.isExportControlOnly = someObject.isExportControlOnly

    return newObject
  }
}
