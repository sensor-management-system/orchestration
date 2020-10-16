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
import { DeviceProperty } from '@/models/DeviceProperty'

export interface IStationaryLocation {
  latitude: number | null
  longitude: number | null
  elevation: number | null
}

export class StationaryLocation implements IStationaryLocation {
  private _latitude: number | null = null
  private _longitude: number | null = null
  private _elevation: number | null = null

  get latitude (): number | null {
    return this._latitude
  }

  set latitude (latitude: number | null) {
    this._latitude = latitude
  }

  get longitude (): number | null {
    return this._longitude
  }

  set longitude (longitude: number | null) {
    this._longitude = longitude
  }

  get elevation (): number | null {
    return this._elevation
  }

  set elevation (elevation: number | null) {
    this._elevation = elevation
  }

  static createFromObject (someObject: IStationaryLocation): StationaryLocation {
    const newObject: StationaryLocation = new StationaryLocation()
    newObject.latitude = someObject.latitude
    newObject.longitude = someObject.longitude
    newObject.elevation = someObject.elevation
    return newObject
  }
}

export interface IDynamicLocation {
  latitude: DeviceProperty | null
  longitude: DeviceProperty | null
  elevation: DeviceProperty | null
}

export class DynamicLocation implements IDynamicLocation {
  private _latitude: DeviceProperty | null = null
  private _longitude: DeviceProperty | null = null
  private _elevation: DeviceProperty | null = null

  get latitude (): DeviceProperty | null {
    return this._latitude
  }

  set latitude (latitude: DeviceProperty | null) {
    this._latitude = latitude
  }

  get longitude (): DeviceProperty | null {
    return this._longitude
  }

  set longitude (longitude: DeviceProperty | null) {
    this._longitude = longitude
  }

  get elevation (): DeviceProperty | null {
    return this._elevation
  }

  set elevation (elevation: DeviceProperty | null) {
    this._elevation = elevation
  }

  static createFromObject (someObject: IDynamicLocation): DynamicLocation {
    const newObject: DynamicLocation = new DynamicLocation()

    newObject.latitude = someObject.latitude
    newObject.longitude = someObject.longitude
    newObject.elevation = someObject.elevation

    return newObject
  }
}
