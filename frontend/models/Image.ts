/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
