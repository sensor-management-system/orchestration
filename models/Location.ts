import IPathSetter from '@/models/IPathSetter'
import { DeviceProperty } from '@/models/DeviceProperty'

export interface IStationaryLocation {
  type: string
  latitude: number | null
  longitude: number | null
  elevation: number | null
}

export class StationaryLocation implements IStationaryLocation, IPathSetter {
  private _latitude: number | null = null
  private _longitude: number | null = null
  private _elevation: number | null = null

  get type (): string {
    return 'stationary'
  }

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

  setPath (path: string, value: any): void {
    switch (path) {
      case 'type':
        throw new TypeError('path type is readonly')
      case 'latitude':
        this.latitude = isNaN(parseFloat(value)) ? 0 : parseFloat(value)
        break
      case 'longitude':
        this.longitude = isNaN(parseFloat(value)) ? 0 : parseFloat(value)
        break
      case 'elevation':
        this.elevation = isNaN(parseFloat(value)) ? 0 : parseFloat(value)
        break
      default:
        throw new TypeError('path ' + path + ' is not defined')
    }
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
  type: string
  latitude: DeviceProperty | null
  longitude: DeviceProperty | null
  elevation: DeviceProperty | null
}

export class DynamicLocation implements IDynamicLocation {
  private _latitude: DeviceProperty | null = null
  private _longitude: DeviceProperty | null = null
  private _elevation: DeviceProperty | null = null

  get type (): string {
    return 'dynamic'
  }

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
