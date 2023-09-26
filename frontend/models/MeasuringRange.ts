/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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
