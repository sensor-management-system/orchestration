/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2022
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
export interface IActionType {
  id: string
  name: string
  uri: string
  definition: string
  provenance: string
  provenanceUri: string
  category: string
  note: string
  globalProvenanceId: string | null
  actionCategoryId: string | null
}

export class ActionType implements IActionType {
  private _id: string = ''
  private _name: string = ''
  private _uri: string = ''
  private _definition: string = ''
  private _provenance: string = ''
  private _provenanceUri: string = ''
  private _category: string = ''
  private _note: string = ''
  private _globalProvenanceId: string | null = null
  private _actionCategoryId: string | null = null

  get id (): string {
    return this._id
  }

  set id (newId: string) {
    this._id = newId
  }

  get name (): string {
    return this._name
  }

  set name (newName: string) {
    this._name = newName
  }

  get uri (): string {
    return this._uri
  }

  set uri (newUri: string) {
    this._uri = newUri
  }

  get definition (): string {
    return this._definition
  }

  set definition (newdefinition: string) {
    this._definition = newdefinition
  }

  get provenance (): string {
    return this._provenance
  }

  set provenance (newProvenance: string) {
    this._provenance = newProvenance
  }

  get provenanceUri (): string {
    return this._provenanceUri
  }

  set provenanceUri (newProvenanceUri: string) {
    this._provenanceUri = newProvenanceUri
  }

  get category (): string {
    return this._category
  }

  set category (newCategory: string) {
    this._category = newCategory
  }

  get note (): string {
    return this._note
  }

  set note (newNote: string) {
    this._note = newNote
  }

  get globalProvenanceId (): string | null {
    return this._globalProvenanceId
  }

  set globalProvenanceId (newId: string | null) {
    this._globalProvenanceId = newId
  }

  get actionCategoryId (): string | null {
    return this._actionCategoryId
  }

  set actionCategoryId (newActionCategoryId: string | null) {
    this._actionCategoryId = newActionCategoryId
  }

  toString (): string {
    return this._name
  }

  static createWithData (id: string, name: string, uri: string, definition: string): ActionType {
    const result = new ActionType()
    result.id = id
    result.name = name
    result.uri = uri
    result.definition = definition
    return result
  }

  static createFromObject (someObject: IActionType): ActionType {
    const newObject = new ActionType()

    newObject.id = someObject.id
    newObject.name = someObject.name
    newObject.uri = someObject.uri
    newObject.definition = someObject.definition
    newObject.provenance = someObject.provenance
    newObject.provenanceUri = someObject.provenanceUri
    newObject.category = someObject.category
    newObject.note = someObject.note
    newObject.uri = someObject.uri
    newObject.globalProvenanceId = someObject.globalProvenanceId
    newObject.actionCategoryId = someObject.actionCategoryId

    return newObject
  }
}