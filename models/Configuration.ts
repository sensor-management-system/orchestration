import IPathSetter from '@/models/IPathSetter'
import Contact, { IContact } from '@/models/Contact'
import { ConfigurationsTree } from '@/models/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/models/ConfigurationsTreeNode'
import { DeviceConfigurationAttributes } from '@/models/DeviceConfigurationAttributes'
import { ITypedLocation, StationaryLocation, DynamicLocation } from '@/models/Location'
import { PlatformConfigurationAttributes } from '@/models/PlatformConfigurationAttributes'

export interface IConfiguration {
  id: number | null
  startDate: Date | null
  endDate: Date | null
  location: ITypedLocation
  contacts: IContact[]
  children: ConfigurationsTreeNode[]
  platformAttributes: PlatformConfigurationAttributes[]
  deviceAttributes: DeviceConfigurationAttributes[]
}

export class Configuration implements IConfiguration, IPathSetter {
  private _id: number | null = null
  private _startDate: Date | null = null
  private _endDate: Date | null = null
  private _location: ITypedLocation = new StationaryLocation()
  private _contacts: IContact[] = [] as IContact[]
  private _tree: ConfigurationsTree = new ConfigurationsTree()
  private _platformAttributes: PlatformConfigurationAttributes[] = [] as PlatformConfigurationAttributes[]
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

  get platformAttributes (): PlatformConfigurationAttributes[] {
    return this._platformAttributes
  }

  set platformAttributes (attributes: PlatformConfigurationAttributes[]) {
    this._platformAttributes = attributes
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
    newObject.platformAttributes = someObject.platformAttributes.map(PlatformConfigurationAttributes.createFromObject)
    newObject.deviceAttributes = someObject.deviceAttributes.map(DeviceConfigurationAttributes.createFromObject)

    return newObject
  }
}
