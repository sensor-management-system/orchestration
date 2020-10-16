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
import Contact, { IContact } from '@/models/Contact'
import { ConfigurationsTree } from '@/models/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/models/ConfigurationsTreeNode'
import { DeviceConfigurationAttributes } from '@/models/DeviceConfigurationAttributes'
import { IStationaryLocation, IDynamicLocation, StationaryLocation, DynamicLocation } from '@/models/Location'
import { PlatformConfigurationAttributes } from '@/models/PlatformConfigurationAttributes'

export interface IConfiguration {
  id: string | null
  startDate: Date | null
  endDate: Date | null
  location: IStationaryLocation | IDynamicLocation | null
  contacts: IContact[]
  children: ConfigurationsTreeNode[]
  platformAttributes: PlatformConfigurationAttributes[]
  deviceAttributes: DeviceConfigurationAttributes[]
}

export class Configuration implements IConfiguration {
  private _id: string | null = null
  private _startDate: Date | null = null
  private _endDate: Date | null = null
  private _location: IStationaryLocation | IDynamicLocation | null = null
  private _contacts: IContact[] = [] as IContact[]
  private _tree: ConfigurationsTree = new ConfigurationsTree()
  private _platformAttributes: PlatformConfigurationAttributes[] = [] as PlatformConfigurationAttributes[]
  private _deviceAttributes: DeviceConfigurationAttributes[] = [] as DeviceConfigurationAttributes[]

  get id (): string | null {
    return this._id
  }

  set id (id: string | null) {
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

  get location (): IStationaryLocation | IDynamicLocation | null {
    return this._location
  }

  set location (location: IStationaryLocation | IDynamicLocation | null) {
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

  static createFromObject (someObject: Configuration): Configuration {
    const newObject = new Configuration()

    newObject.id = someObject.id
    newObject.startDate = someObject.startDate instanceof Date ? new Date(someObject.startDate.getTime()) : null
    newObject.endDate = someObject.endDate instanceof Date ? new Date(someObject.endDate.getTime()) : null

    switch (true) {
      case someObject.location instanceof StationaryLocation:
        newObject.location = StationaryLocation.createFromObject(someObject.location as StationaryLocation)
        break
      case someObject.location instanceof DynamicLocation:
        newObject.location = DynamicLocation.createFromObject(someObject.location as DynamicLocation)
        break
    }
    newObject.contacts = someObject.contacts.map(Contact.createFromObject)
    newObject.tree = ConfigurationsTree.createFromObject(someObject.tree)
    newObject.platformAttributes = someObject.platformAttributes.map(PlatformConfigurationAttributes.createFromObject)
    newObject.deviceAttributes = someObject.deviceAttributes.map(DeviceConfigurationAttributes.createFromObject)

    return newObject
  }
}
