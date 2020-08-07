import { DeviceProperty } from '@/models/DeviceProperty'
import Device from '@/models/Device'
import IPathSetter from './IPathSetter'

export interface IDeviceConfigurationAttributes {
  id: number | null
  offsetX: number
  offsetY: number
  offsetZ: number
  calibrationDate: Date | null
  deviceProperties: DeviceProperty[]
}

export class DeviceConfigurationAttributes implements IDeviceConfigurationAttributes, IPathSetter {
  private _device: Device
  private _offsetX: number = 0
  private _offsetY: number = 0
  private _offsetZ: number = 0
  private _calibrationDate: Date | null = null
  private _deviceProperties: DeviceProperty[] = []

  constructor (device: Device) {
    this._device = device
  }

  static createFromObject (someObject: DeviceConfigurationAttributes): DeviceConfigurationAttributes {
    const newObject = new DeviceConfigurationAttributes(someObject.device)

    newObject.offsetX = someObject.offsetX
    newObject.offsetY = someObject.offsetY
    newObject.offsetZ = someObject.offsetZ
    newObject.calibrationDate = someObject.calibrationDate instanceof Date ? new Date(someObject.calibrationDate.getTime()) : null
    someObject.deviceProperties.forEach(e => newObject.addDeviceProperty(e))

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
      case 'calibrationDate':
        this.calibrationDate = value instanceof Date ? value : null
        break
      default:
        throw new TypeError('path ' + path + ' is not defined')
    }
  }

  get id (): number | null {
    return this._device.id
  }

  get device (): Device {
    return this._device
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

  get calibrationDate (): Date | null {
    return this._calibrationDate
  }

  set calibrationDate (date: Date | null) {
    this._calibrationDate = date
  }

  get deviceProperties (): DeviceProperty[] {
    return this._deviceProperties
  }

  addDeviceProperty (property: DeviceProperty): number {
    if (!this.device.properties.find(e => e === property)) {
      throw new Error('unknown property')
    }
    return this._deviceProperties.push(property)
  }

  addDevicePropertyById (id: number): number {
    const property = this.device.properties.find(e => e.id === id)
    if (!property) {
      throw new Error('unknown property id')
    }
    return this._deviceProperties.push(property)
  }

  removeDeviceProperty (property: DeviceProperty): number {
    const index = this.device.properties.findIndex(e => e === property)
    if (index === -1) {
      throw new Error('unknown property')
    }
    this._deviceProperties.splice(index, 1)
    return index
  }

  removeDevicePropertyById (id: number): number {
    const index = this.device.properties.findIndex(e => e.id === id)
    if (index === -1) {
      throw new Error('unknown property id')
    }
    this._deviceProperties.splice(index, 1)
    return index
  }
}
