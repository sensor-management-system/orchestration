export interface IContact {
  id: number | null
  email: string
  firstName: string
  lastName: string
  profileLink: string
}

export default class Contact implements IContact {
  private _id: number | null = null
  private _email: string = ''
  private _firstName: string = ''
  private _lastName: string = ''
  private _profileLink: string = ''

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

  get firstName (): string {
    return this._firstName
  }

  set firstName (newFirstName: string) {
    this._firstName = newFirstName
  }

  get lastName (): string {
    return this._lastName
  }

  set lastName (newLastName: string) {
    this._lastName = newLastName
  }

  get profileLink (): string {
    return this._profileLink
  }

  set profileLink (newProfileLink: string) {
    this._profileLink = newProfileLink
  }

  toString (): string {
    if (this._firstName && this._lastName) {
      return this._firstName + ' ' + this._lastName
    }
    if (this._email) {
      return this._email
    }
    return 'Contact ' + this._id
  }

  static createWithIdEMailAndNames (id: number, email: string, firstName: string, lastName: string, profileLink: string): Contact {
    const result = new Contact()
    result.id = id
    result.email = email
    result.firstName = firstName
    result.lastName = lastName
    result.profileLink = profileLink
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
    newObject.firstName = someObject.firstName
    newObject.lastName = someObject.lastName
    newObject.profileLink = someObject.profileLink
    return newObject
  }
}
