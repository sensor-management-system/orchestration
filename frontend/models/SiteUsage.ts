/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
export interface ISiteUsage {
  id: string
  name: string
  uri: string
  definition: string
  provenance: string
  provenanceUri: string
  category: string
  note: string
  globalProvenanceId: string | null
}

export class SiteUsage implements ISiteUsage {
  private _id: string = ''
  private _name: string = ''
  private _uri: string = ''
  private _definition: string = ''
  private _provenance: string = ''
  private _provenanceUri: string = ''
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

  toString (): string {
    return this._name
  }

  static createWithData (id: string, name: string, uri: string, definition: string): SiteUsage {
    const result = new SiteUsage()
    result.id = id
    result.name = name
    result.uri = uri
    result.definition = definition
    return result
  }

  static createFromObject (someObject: ISiteUsage): SiteUsage {
    const newObject = new SiteUsage()

    newObject.id = someObject.id
    newObject.name = someObject.name
    newObject.definition = someObject.definition
    newObject.provenance = someObject.provenance
    newObject.provenanceUri = someObject.provenanceUri
    newObject.category = someObject.category
    newObject.note = someObject.note
    newObject.uri = someObject.uri
    newObject.globalProvenanceId = someObject.globalProvenanceId

    return newObject
  }
}
