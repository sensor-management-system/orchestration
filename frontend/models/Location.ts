/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DeviceProperty } from '@/models/DeviceProperty'

export enum LocationType {
  Stationary = 'Stationary',
  Dynamic = 'Dynamic'
}

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

    newObject.latitude = someObject.latitude === null ? null : DeviceProperty.createFromObject(someObject.latitude)
    newObject.longitude = someObject.longitude === null ? null : DeviceProperty.createFromObject(someObject.longitude)
    newObject.elevation = someObject.elevation === null ? null : DeviceProperty.createFromObject(someObject.elevation)

    return newObject
  }
}
