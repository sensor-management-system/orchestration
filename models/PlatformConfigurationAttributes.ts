import Platform from '@/models/Platform'
import IPathSetter from '@/models/IPathSetter'

export interface IPlatformConfigurationAttributes {
  platform: Platform
  offsetX: number
  offsetY: number
  offsetZ: number
}

export class PlatformConfigurationAttributes implements IPlatformConfigurationAttributes, IPathSetter {
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

  setPath (path: string, value: any): void {
    switch (path) {
      case 'offsetX':
        this.offsetX = isNaN(value) ? 0 : parseInt(value)
        break
      case 'offsetY':
        this.offsetY = isNaN(value) ? 0 : parseInt(value)
        break
      case 'offsetZ':
        this.offsetZ = isNaN(value) ? 0 : parseInt(value)
        break
      default:
        throw new TypeError('path ' + path + ' is not defined')
    }
  }

  get id (): number | null {
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
