import { DateTime } from 'luxon'
import { Configuration } from '@/models/Configuration'

/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2022
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tim Eder (UFZ, tim.eder@ufz.de)
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
export interface IAvailability {
  id: string
  available: boolean
  beginDate?: DateTime
  endDate?: DateTime
  configurationID?: string
  configuration?: Configuration
  mountID?: string
}

export class Availability implements IAvailability {
  private _id: string = ''
  private _available: boolean = false
  private _beginDate?: DateTime
  private _endDate?: DateTime
  private _configurationID?: string = ''
  private _configuration?: Configuration
  private _mountID?: string = ''

  get id (): string {
    return this._id
  }

  set id (newId: string) {
    this._id = newId
  }

  get available (): boolean {
    return this._available
  }

  set available (newAvailability: boolean) {
    this._available = newAvailability
  }

  get beginDate (): DateTime | undefined {
    return this._beginDate
  }

  set beginDate (newDate: DateTime | undefined) {
    this._beginDate = newDate
  }

  get endDate (): DateTime | undefined {
    return this._endDate
  }

  set endDate (newEndDate: DateTime | undefined) {
    this._endDate = newEndDate
  }

  get configurationID (): string | undefined {
    return this._configurationID
  }

  set configurationID (newConfiguration: string | undefined) {
    this._configurationID = newConfiguration
  }

  get configuration (): Configuration | undefined {
    return this._configuration
  }

  set configuration (newConfiguration: Configuration | undefined) {
    this._configuration = newConfiguration
  }

  get mountID (): string | undefined {
    return this._mountID
  }

  set mountID (newmount: string | undefined) {
    this._mountID = newmount
  }

  static createFromObject (someObject: IAvailability): Availability {
    const newObject = new Availability()

    newObject.id = someObject.id
    newObject.available = someObject.available
    if (!newObject.available) {
      newObject.beginDate = someObject.beginDate
      newObject.endDate = someObject.endDate
      newObject.configurationID = someObject.configurationID
      newObject.configuration = someObject.configuration
      newObject.mountID = someObject.mountID
    }

    return newObject
  }
}
