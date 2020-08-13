import Contact, { IContact } from './Contact'

export interface IUser {
  id: number | null
  subject: string
  contact: IContact | null
}

export default class User implements IUser {
  private _id: number | null = null
  private _subject: string = ''
  private _contact: Contact | null = null

  get id (): number | null {
    return this._id
  }

  set id (newId: number | null) {
    this._id = newId
  }

  get subject (): string {
    return this._subject
  }

  set subject (newSubject: string) {
    this._subject = newSubject
  }

  get contact (): Contact | null {
    return this._contact
  }

  set contact (newContact: Contact | null) {
    this._contact = newContact
  }

  static createFromObjet (someObject: IUser): User {
    const newObject = new User()

    newObject.id = someObject.id
    newObject.subject = someObject.subject
    if (someObject.contact !== null) {
      newObject.contact = Contact.createFromObject(someObject.contact)
    }

    return newObject
  }
}
