import IPathSetter from '@/models/IPathSetter'
import Contact, { IContact } from '@/models/Contact'
import { ConfigurationsTree } from '@/models/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/models/ConfigurationsTreeNode'
import { DeviceConfigurationAttributes } from '@/models/DeviceConfigurationAttributes'

export interface ILocation {
  latitude: number | null
  longitude: number | null
  elevation: number | null
}

export const isILocation = (location: any): location is ILocation => {
  return location &&
    location.latitude !== undefined && (location.latitude === null || typeof location.latitude === 'number') &&
    location.longitude !== undefined && (location.longitude === null || typeof location.longitude === 'number') &&
    location.elevation !== undefined && (location.elevation === null || typeof location.elevation === 'number')
}

export interface ITypedLocation extends ILocation, IPathSetter {
  type: string
}

export const isITypedLocation = (location: any): location is ITypedLocation => {
  return isILocation(location) &&
    // @ts-ignore
    location.type !== undefined && (typeof location.type === 'string')
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

export interface IConfiguration {
  id: number | null
  startDate: Date | null
  endDate: Date | null
  location: ITypedLocation
  contacts: IContact[]
  children: ConfigurationsTreeNode[]
}

export class Configuration implements IConfiguration, IPathSetter {
  private _id: number | null = null
  private _startDate: Date | null = null
  private _endDate: Date | null = null
  private _location: ITypedLocation = new StationaryLocation()
  private _contacts: IContact[] = [] as IContact[]
  private _tree: ConfigurationsTree = new ConfigurationsTree()
  private _deviceAttributes: DeviceConfigurationAttributes[] = [] as DeviceConfigurationAttributes[]

  get id (): number | null {
    return this._id
  }

  set id (id: number | null) {
    this._id = id
  }

  get startDate (): Date | null {
    return this._startDate
  }

  set startDate (date: Date | null) {
    this._startDate = date
  }

  get endDate (): Date | null {
    return this._endDate
  }

  set endDate (date: Date | null) {
    this._endDate = date
  }

  get location (): ITypedLocation {
    return this._location
  }

  set location (location: ITypedLocation) {
    this._location = location
  }

  get contacts (): IContact[] {
    return this._contacts
  }

  set contacts (contacts: IContact[]) {
    this._contacts = contacts
  }

  get tree (): ConfigurationsTree {
    return this._tree
  }

  set tree (tree: ConfigurationsTree) {
    this._tree = tree
  }

  get children (): ConfigurationsTreeNode[] {
    return this._tree.toArray()
  }

  set children (children: ConfigurationsTreeNode[]) {
    this._tree = ConfigurationsTree.fromArray(children)
  }

  get deviceAttributes (): DeviceConfigurationAttributes[] {
    return this._deviceAttributes
  }

  set deviceAttributes (attributes: DeviceConfigurationAttributes[]) {
    this._deviceAttributes = attributes
  }

  setPath (path: string, value: any): void {
    const paths = path.split('.')
    const topLevelElement = paths.splice(0, 1)[0]
    const tail = paths.join('.')
    switch (topLevelElement) {
      case 'id':
        this.id = isNaN(parseInt(value)) ? null : parseInt(value)
        break
      case 'startDate':
        this.startDate = value instanceof Date ? value : null
        break
      case 'endDate':
        this.endDate = value instanceof Date ? value : null
        break
      case 'location':
        this.location.setPath(tail, value)
        break
      default:
        throw new TypeError('path ' + path + ' is not defined')
    }
  }

  static createFromObject (someObject: Configuration): Configuration {
    const newObject = new Configuration()

    newObject.id = someObject.id
    newObject.startDate = someObject.startDate instanceof Date ? new Date(someObject.startDate.getTime()) : null
    newObject.endDate = someObject.endDate instanceof Date ? new Date(someObject.endDate.getTime()) : null

    switch (someObject.location.type) {
      case 'stationary':
        newObject.location = StationaryLocation.createFromObject(someObject.location)
        break
      case 'dynamic':
        newObject.location = DynamicLocation.createFromObject(someObject.location)
        break
    }
    newObject.contacts = someObject.contacts.map(Contact.createFromObject)
    newObject.tree = ConfigurationsTree.createFromObject(someObject.tree)
    newObject.deviceAttributes = someObject.deviceAttributes.map(DeviceConfigurationAttributes.createFromObject)

    return newObject
  }
}
