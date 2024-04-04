/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2024
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

import { ExportControl } from '@/models/ExportControl'

export interface IManufacturerModel {
  id: string
  manufacturerName: string
  model: string
  externalSystemName: string
  externalSystemUrl: string

  exportControl: ExportControl | null
}

export class ManufacturerModel implements IManufacturerModel {
  private _id: string = ''
  private _manufacturerName: string = ''
  private _model: string = ''
  private _externalSystemName: string = ''
  private _externalSystemUrl: string = ''

  private _exportControl: ExportControl | null = null

  get id (): string {
    return this._id
  }

  set id (newId: string) {
    this._id = newId
  }

  get manufacturerName (): string {
    return this._manufacturerName
  }

  set manufacturerName (newManufacturerName: string) {
    this._manufacturerName = newManufacturerName
  }

  get model (): string {
    return this._model
  }

  set model (newModel: string) {
    this._model = newModel
  }

  get externalSystemName (): string {
    return this._externalSystemName
  }

  set externalSystemName (newExternalSystemName: string) {
    this._externalSystemName = newExternalSystemName
  }

  get externalSystemUrl (): string {
    return this._externalSystemUrl
  }

  set externalSystemUrl (newExternalSystemUrl: string) {
    this._externalSystemUrl = newExternalSystemUrl
  }

  get exportControl (): ExportControl | null {
    return this._exportControl
  }

  set exportControl (newExportControl: ExportControl | null) {
    this._exportControl = newExportControl
  }

  static createFromObject (someObject: IManufacturerModel): ManufacturerModel {
    const newObject = new ManufacturerModel()

    newObject.id = someObject.id
    newObject.manufacturerName = someObject.manufacturerName
    newObject.model = someObject.model
    newObject.externalSystemName = someObject.externalSystemName
    newObject.externalSystemUrl = someObject.externalSystemUrl

    newObject.exportControl = someObject.exportControl === null ? null : ExportControl.createFromObject(someObject.exportControl)

    return newObject
  }
}
