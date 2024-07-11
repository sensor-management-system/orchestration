/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2021
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

export interface IEpsgCode {
  code: string
  text: string
}

export class EpsgCode implements IEpsgCode {
  private _code: string
  private _text: string

  constructor (code: string, text: string) {
    this._code = code
    this._text = text
  }

  get code (): string {
    return this._code
  }

  get text (): string {
    return this._text
  }

  static createFromObject (someObject: IEpsgCode) {
    return new EpsgCode(
      someObject.code,
      someObject.text
    )
  }
}
