export interface IContact {
  id: number | null
  email: string
  userName: string
  firstName: string
  lastName: string
}

export default class Contact implements IContact {
  private _id: number | null = null
  private _email: string = ''
  private _userName: string = ''
  private _firstName: string = ''
  private _lastName: string = ''

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

  get userName (): string {
    return this._userName
  }

  set userName (newUserName: string) {
    this._userName = newUserName
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

  static createWithIdEMailAndNames (id: number, email: string, userName: string, firstName: string, lastName: string): Contact {
    const result = new Contact()
    result.id = id
    result.email = email
    result.userName = userName
    result.firstName = firstName
    result.lastName = lastName
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
    newObject.userName = someObject.userName
    newObject.firstName = someObject.firstName
    newObject.lastName = someObject.lastName
    return newObject
  }
}
