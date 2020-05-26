import Contact from './Contact'

export default class Platform {
  private _id: number | null = null
  private _platformType: string = ''
  private _shortName: string = ''
  private _longName: string = ''
  private _description: string = ''
  private _manufacturer: string = ''
  private _type: string = ''
  private _inventoryNumber: number | null = null
  private _url: string = ''

  private _contacts: Contact[] = []

  get id (): number | null {
    return this._id
  }

  set id (newId: number | null) {
    this._id = newId
  }

  get platformType (): string {
    return this._platformType
  }

  set platformType (newPlatformType: string) {
    this._platformType = newPlatformType
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

  get manufacturer (): string {
    return this._manufacturer
  }

  set manufacturer (newManufacturer: string) {
    this._manufacturer = newManufacturer
  }

  get type (): string {
    return this._type
  }

  set type (newType: string) {
    this._type = newType
  }

  get inventoryNumber (): number | null {
    return this._inventoryNumber
  }

  set inventoryNumber (newInventoryNumber: number | null) {
    this._inventoryNumber = newInventoryNumber
  }

  get url (): string {
    return this._url
  }

  set url (newUrl: string) {
    this._url = newUrl
  }

  get contacts (): Contact[] {
    return this._contacts
  }

  set contacts (newContacts: Contact[]) {
    this._contacts = newContacts
  }

  static createEmpty (): Platform {
    return new Platform()
  }

  static createWithIdAndData (
    id: number | null,
    platformType: string,
    shortName: string,
    longName: string,
    description: string,
    manufacturer: string,
    type: string,
    inventoryNumber: number | null,
    url: string,
    contacts: Contact[]
  ): Platform {
    const result: Platform = new Platform()
    result.id = id
    result.platformType = platformType
    result.shortName = shortName
    result.longName = longName
    result.description = description
    result.manufacturer = manufacturer
    result.type = type
    result.inventoryNumber = inventoryNumber
    result.url = url
    result.contacts = contacts

    return result
  }
}
