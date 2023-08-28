/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
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

export interface IAttachment {
  id: string | null
  url: string
  label: string
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
