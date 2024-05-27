/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
export interface IMeasuringRange {
  min: number | null
  max: number | null
}

export class MeasuringRange implements IMeasuringRange {
  private _min: number | null = null
  private _max: number | null = null

  constructor (min: number | null = null, max: number | null = null) {
    this.min = min
    this.max = max
  }

  /**
   * creates an instance from another object
   *
   * @static
   * @param {IMeasuringRange} someObject - the object from which the new instance is to be created
   * @return {MeasuringRange} the newly created instance
   */
  static createFromObject (someObject: IMeasuringRange): MeasuringRange {
    return new MeasuringRange(someObject.min, someObject.max)
  }

  get min (): number | null {
    return this._min
  }

  set min (min: number | null) {
    this._min = min
  }

  get max (): number | null {
    return this._max
  }

  set max (max: number | null) {
    this._max = max
  }
}
