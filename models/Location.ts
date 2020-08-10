import IPathSetter from '@/models/IPathSetter'

export interface ILocation {
  latitude: number | null
  longitude: number | null
  elevation: number | null
}

export interface ITypedLocation extends ILocation, IPathSetter {
  type: string
}

export class StationaryLocation implements ITypedLocation, IPathSetter {
  private _latitude: number = 0
  private _longitude: number = 0
  private _elevation: number = 0

  get type (): string {
    return 'stationary'
  }

  get latitude (): number {
    return this._latitude
  }

  set latitude (latitude: number) {
    this._latitude = latitude
  }

  get longitude (): number {
    return this._longitude
  }

  set longitude (longitude: number) {
    this._longitude = longitude
  }

  get elevation (): number {
    return this._elevation
  }

  set elevation (elevation: number) {
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

  static createFromObject (someObject: ITypedLocation): StationaryLocation {
    const newObject: StationaryLocation = new StationaryLocation()
    newObject.latitude = someObject.latitude || 0
    newObject.longitude = someObject.longitude || 0
    newObject.elevation = someObject.elevation || 0
    return newObject
  }
}

export class DynamicLocation implements ITypedLocation, IPathSetter {
  private _latitude: number | null = null
  private _longitude: number | null = null
  private _elevation: number | null = null

  get type (): string {
    return 'dynamic'
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
        this.latitude = isNaN(parseFloat(value)) ? null : parseFloat(value)
        break
      case 'longitude':
        this.longitude = isNaN(parseFloat(value)) ? null : parseFloat(value)
        break
      case 'elevation':
        this.elevation = isNaN(parseFloat(value)) ? null : parseFloat(value)
        break
      default:
        throw new TypeError('path ' + path + ' is not defined')
    }
  }

  static createFromObject (someObject: ITypedLocation): DynamicLocation {
    const newObject: DynamicLocation = new DynamicLocation()
    newObject.latitude = someObject.latitude
    newObject.longitude = someObject.longitude
    newObject.elevation = someObject.elevation
    return newObject
  }
}
