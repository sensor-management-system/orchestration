/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2024
 * - Maximilian Schaldach (UFZ, maximilian.schaldach@ufz.de)
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
import { Attachment, IAttachment } from '@/models/Attachment'

export interface IAttachmentWithUrl {
  attachment: IAttachment
  url: string
}
export interface IImage {
  id: string
  orderIndex: number
  attachment: IAttachment | null
}

export class Image implements IImage {
  private _id: string = ''
  private _orderIndex: number = 0
  private _attachment: Attachment | null = null

  get orderIndex (): number {
    return this._orderIndex
  }

  set orderIndex (value: number) {
    this._orderIndex = value
  }

  get id (): string {
    return this._id
  }

  set id (value: string) {
    this._id = value
  }

  get attachment (): Attachment | null {
    return this._attachment
  }

  set attachment (value: Attachment | null) {
    this._attachment = value
  }

  static createFromObject (someObject: IImage): Image {
    const result = new Image()
    result.id = someObject.id
    result.orderIndex = someObject.orderIndex ?? 0
    result.attachment = someObject.attachment ? Attachment.createFromObject(someObject.attachment) : null
    return result
  }
}
