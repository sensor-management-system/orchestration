import Person from './Person'

export default class Platform {
  private _id: number | null = null
  private _platformTypeId: number | null = null
  private _shortName: string = ''
  private _longName: string = ''
  private _description: string = ''
  private _manufactureId: number | null = null
  private _website: string = ''
  private _responsiblePersons: Person[] = []

  get id (): number | null {
    return this._id
  }

  set id (newId: number | null) {
    this._id = newId
  }

  get platformTypeId (): number | null {
    return this._platformTypeId
  }

  set platformTypeId (newPlatformTypeId: number | null) {
    this._platformTypeId = newPlatformTypeId
  }

  get shortName (): string {
    return this._shortName
  }

  set shortName (newShortName: string) {
    this._shortName = newShortName
  }

  get longName (): string {
    return this._longName
  }

  set longName (newLongName: string) {
    this._longName = newLongName
  }

  get description (): string {
    return this._description
  }

  set description (newDescription: string) {
    this._description = newDescription
  }

  get manufactureId (): number | null {
    return this._manufactureId
  }

  set manufactureId (newManufactureId: number | null) {
    this._manufactureId = newManufactureId
  }

  get website (): string {
    return this._website
  }

  set website (newWebsite: string) {
    this._website = newWebsite
  }

  get responsiblePersons (): Person[] {
    return this._responsiblePersons
  }

  set responsiblePersons (responsiblePersons: Person[]) {
    this._responsiblePersons = responsiblePersons
  }

  static createEmpty (): Platform {
    return new Platform()
  }

  static createWithIdAndData (
    id: number | null,
    platformTypeId: number | null,
    shortName: string,
    longName: string,
    description: string,
    manufactureId: number | null,
    website: string,
    responsiblePersons: Person[]
  ): Platform {
    const result: Platform = new Platform()
    result.id = id
    result.platformTypeId = platformTypeId
    result.shortName = shortName
    result.longName = longName
    result.description = description
    result.manufactureId = manufactureId
    result.website = website
    result.responsiblePersons = responsiblePersons

    return result
  }
}
