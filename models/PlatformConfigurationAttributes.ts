import Platform from '@/models/Platform'

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
