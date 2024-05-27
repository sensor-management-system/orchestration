/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
export interface ITsmEndpoint {
  id: string
  name: string
  url: string
}

export class TsmEndpoint implements ITsmEndpoint {
  private _id: string = ''
  private _name: string = ''
  private _url: string = ''

  get id (): string {
    return this._id
  }

  set id (value: string) {
    this._id = value
  }

  get name (): string {
    return this._name
  }

  set name (value: string) {
    this._name = value
  }

  get url (): string {
    return this._url
  }

  set url (value: string) {
    this._url = value
  }

  static createFromObject (someObject: ITsmEndpoint): TsmEndpoint {
    const result = new TsmEndpoint()
    result.id = someObject.id ?? ''
    result.name = someObject.name ?? ''
    result.url = someObject.url ?? ''
    return result
  }
}
