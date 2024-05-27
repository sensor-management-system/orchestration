/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'

export interface IAttachment {
  id: string | null
  url: string
  label: string
  description: string
  isUpload: boolean
  createdAt: DateTime | null
}

export class Attachment implements IAttachment {
  static readonly mimeTypes: Object = {
    'image/png': ['png'],
    'images/jpeg': ['jpg', 'jpeg'],
    'application/pdf': ['pdf'],
    'text/plain': ['txt'],
    'text/rtf': ['rtf'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['docx'],
    'application/msword': ['doc'],
    'application/vnd.oasis.opendocument.text': ['odt']
  }

  private _id: string | null = null
  private _url: string = ''
  private _label: string = ''
  private _description: string = ''
  private _isUpload: boolean = false
  private _createdAt: DateTime | null = null

  // @TODO: add an _uploadedAt field
  static createEmpty (): Attachment {
    return new Attachment()
  }

  /**
   * creates an instance from another object
   *
   * @static
   * @param {IAttachment} someObject - the object from which the new instance is to be created
   * @return {Attachment} the newly created instance
   */
  static createFromObject (someObject: IAttachment): Attachment {
    const attachment = new Attachment()
    attachment.id = someObject.id || null
    attachment.url = someObject.url || ''
    attachment.label = someObject.label || ''
    attachment.description = someObject.description || ''
    attachment.isUpload = someObject.isUpload
    attachment.createdAt = someObject.createdAt
    return attachment
  }

  get id (): string | null {
    return this._id
  }

  set id (id: string | null) {
    this._id = id
  }

  get url (): string {
    return this._url
  }

  set url (url: string) {
    this._url = url
  }

  get label (): string {
    return this._label
  }

  set label (label: string) {
    this._label = label
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

  set isUpload (isUpload: boolean) {
    this._isUpload = isUpload
  }

  get createdAt (): DateTime | null {
    return this._createdAt
  }

  set createdAt (newDate: DateTime | null) {
    this._createdAt = newDate
  }
}
