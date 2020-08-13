export interface IContact {
  id: number | null
  email: string
  givenName: string
  familyName: string
  website: string
}

export default class Contact implements IContact {
  private _id: number | null = null
  private _email: string = ''
  private _givenName: string = ''
  private _familyName: string = ''
  private _website: string = ''

  get id (): number | null {
    return this._id
  }

  set id (newId: number | null) {
    this._id = newId
  }

  get email (): string {
    return this._email
  }

  set email (newEmail: string) {
    this._email = newEmail
  }

  get givenName (): string {
    return this._givenName
  }

  set givenName (newGivenName: string) {
    this._givenName = newGivenName
  }

  get familyName (): string {
    return this._familyName
  }

  set familyName (newFamilyName: string) {
    this._familyName = newFamilyName
  }

  get website (): string {
    return this._website
  }

  set website (newWebsite: string) {
    this._website = newWebsite
  }

  toString (): string {
    if (this._givenName && this._familyName) {
      return this._givenName + ' ' + this._familyName
    }
    if (this._email) {
      return this._email
    }
    return 'Contact ' + this._id
  }

  static createWithIdEMailAndNames (id: number, email: string, givenName: string, familyName: string, website: string): Contact {
    const result = new Contact()
    result.id = id
    result.email = email
    result.givenName = givenName
    result.familyName = familyName
    result.website = website
    return result
  }

  static createEmpty (): Contact {
    return new Contact()
  }

  /**
   * creates an instance from another object
   *
   * @static
   * @param {IContact} someObject - the object from which the new instance is to be created
   * @return {Contact} the newly created instance
   */
  static createFromObject (someObject: IContact): Contact {
    const newObject = new Contact()
    newObject.id = someObject.id
    newObject.email = someObject.email
    newObject.givenName = someObject.givenName
    newObject.familyName = someObject.familyName
    newObject.website = someObject.website
    return newObject
  }
}
