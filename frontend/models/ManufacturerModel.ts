/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
