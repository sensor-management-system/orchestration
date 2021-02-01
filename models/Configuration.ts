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
import { DateTime } from 'luxon'

import { IContact, Contact } from '@/models/Contact'
import { ConfigurationsTree } from '@/models/ConfigurationsTree'
import { ConfigurationsTreeNode } from '@/models/ConfigurationsTreeNode'
import { DeviceConfigurationAttributes } from '@/models/DeviceConfigurationAttributes'
import { IStationaryLocation, IDynamicLocation, StationaryLocation, DynamicLocation } from '@/models/Location'
import { PlatformConfigurationAttributes } from '@/models/PlatformConfigurationAttributes'

export interface IConfiguration {
  id: string
  startDate: DateTime | null
  endDate: DateTime | null
  projectUri: string
  projectName: string
  label: string
  status: string
  location: IStationaryLocation | IDynamicLocation | null
  contacts: IContact[]
  children: ConfigurationsTreeNode[]
  platformAttributes: PlatformConfigurationAttributes[]
  deviceAttributes: DeviceConfigurationAttributes[]
}

export class Configuration implements IConfiguration {
  private _id: string = ''
  private _startDate: DateTime | null = null
  private _endDate: DateTime | null = null
  private _projectUri: string = ''
  private _projectName: string = ''
  private _label: string = ''
  private _status: string = ''
  private _location: IStationaryLocation | IDynamicLocation | null = null
  private _contacts: IContact[] = [] as IContact[]
  private _tree: ConfigurationsTree = new ConfigurationsTree()
  private _platformAttributes: PlatformConfigurationAttributes[] = [] as PlatformConfigurationAttributes[]
  private _deviceAttributes: DeviceConfigurationAttributes[] = [] as DeviceConfigurationAttributes[]

  get id (): string {
    return this._id
  }

  set id (id: string) {
    this._id = id
  }

  get startDate (): DateTime | null {
    return this._startDate
  }

  set startDate (date: DateTime | null) {
    this._startDate = date
  }

  get endDate (): DateTime | null {
    return this._endDate
  }

  set endDate (date: DateTime | null) {
    this._endDate = date
  }

  get projectName (): string {
    return this._projectName
  }

  set projectName (newProjectName: string) {
    this._projectName = newProjectName
  }

  get projectUri (): string {
    return this._projectUri
  }

  set projectUri (newProjectUri: string) {
    this._projectUri = newProjectUri
  }

  get label (): string {
    return this._label
  }

  set label (newLabel: string) {
    this._label = newLabel
  }

  get status (): string {
    return this._status
  }

  set status (newStatus: string) {
    this._status = newStatus
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
    // luxon DateTime objects are immutable
    newObject.startDate = someObject.startDate
    newObject.endDate = someObject.endDate

    newObject.projectName = someObject.projectName
    newObject.projectUri = someObject.projectUri

    newObject.label = someObject.label
    newObject.status = someObject.status

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
