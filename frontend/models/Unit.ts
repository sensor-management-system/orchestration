/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
export interface IUnit {
  id: string
  name: string
  uri: string
  definition: string
  provenance: string
  provenanceTerm: string
  provenanceUri: string
  ucumCaseSensitiveSymbol: string
  category: string
  note: string
  globalProvenanceId: string | null
}

export class Unit implements IUnit {
  private _id: string = ''
  private _name: string = ''
  private _uri: string = ''
  private _definition: string = ''
  private _provenance: string = ''
  private _provenanceTerm: string = ''
  private _provenanceUri: string = ''
  private _ucumCaseSenstiveSymbol: string = ''
  private _category: string = ''
  private _note: string = ''
  private _globalProvenanceId: string | null = null

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

  set definition (newDefinition: string) {
    this._definition = newDefinition
  }

  get provenance (): string {
    return this._provenance
  }

  set provenance (newProvenance: string) {
    this._provenance = newProvenance
  }

  get provenanceTerm (): string {
    return this._provenanceTerm
  }

  set provenanceTerm (newProvenanceTerm: string) {
    this._provenanceTerm = newProvenanceTerm
  }

  get provenanceUri (): string {
    return this._provenanceUri
  }

  set provenanceUri (newProvenanceUri: string) {
    this._provenanceUri = newProvenanceUri
  }

  get ucumCaseSensitiveSymbol (): string {
    return this._ucumCaseSenstiveSymbol
  }

  set ucumCaseSensitiveSymbol (newUcumCaseSensitiveSymbol: string) {
    this._ucumCaseSenstiveSymbol = newUcumCaseSensitiveSymbol
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

  toString (): string {
    return this._name
  }

  static createWithData (id: string, name: string, uri: string, definition: string): Unit {
    const result = new Unit()
    result.id = id
    result.name = name
    result.uri = uri
    result.definition = definition
    return result
  }

  static createFromObject (someObject: IUnit): Unit {
    const newObject = new Unit()

    newObject.id = someObject.id
    newObject.name = someObject.name
    newObject.definition = someObject.definition
    newObject.provenance = someObject.provenance
    newObject.provenanceTerm = someObject.provenanceTerm
    newObject.provenanceUri = someObject.provenanceUri
    newObject.ucumCaseSensitiveSymbol = someObject.ucumCaseSensitiveSymbol
    newObject.category = someObject.category
    newObject.note = someObject.note
    newObject.uri = someObject.uri
    newObject.globalProvenanceId = someObject.globalProvenanceId

    return newObject
  }
}
