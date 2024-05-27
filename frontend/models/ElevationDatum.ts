/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2021
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

export interface IElevationDatum {
  name: string
  uri: string
}

export class ElevationDatum implements IElevationDatum {
  private _name: string
  private _uri: string

  constructor (name: string, uri: string) {
    this._name = name
    this._uri = uri
  }

  get name (): string {
    return this._name
  }

  get uri (): string {
    return this._uri
  }

  static createFromObject (someObject: IElevationDatum) {
    return new ElevationDatum(
      someObject.name,
      someObject.uri
    )
  }
}
