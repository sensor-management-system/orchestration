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
import { Platform } from '@/models/Platform'

export interface IPlatformConfigurationAttributes {
  platform: Platform
  offsetX: number
  offsetY: number
  offsetZ: number
}

export class PlatformConfigurationAttributes implements IPlatformConfigurationAttributes {
  private _platform: Platform
  private _offsetX: number = 0
  private _offsetY: number = 0
  private _offsetZ: number = 0

  constructor (platform: Platform) {
    this._platform = platform
  }

  static createFromObject (someObject: IPlatformConfigurationAttributes): PlatformConfigurationAttributes {
    const newObject = new PlatformConfigurationAttributes(someObject.platform)

    newObject.offsetX = someObject.offsetX
    newObject.offsetY = someObject.offsetY
    newObject.offsetZ = someObject.offsetZ

    return newObject
  }

  get id (): string | null {
    return this._platform.id
  }

  get platform (): Platform {
    return this._platform
  }

  get offsetX (): number {
    return this._offsetX
  }

  set offsetX (offsetX: number) {
    this._offsetX = offsetX
  }

  get offsetY (): number {
    return this._offsetY
  }

  set offsetY (offsetY: number) {
    this._offsetY = offsetY
  }

  get offsetZ (): number {
    return this._offsetZ
  }

  set offsetZ (offsetZ: number) {
    this._offsetZ = offsetZ
  }
}
