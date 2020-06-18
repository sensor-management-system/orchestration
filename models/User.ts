import Contact, { IContact } from './Contact'
import IPathSetter from './IPathSetter'

export interface IUser {
  id: number | null
  subject: string
  contact: IContact | null
}

export default class User implements IUser, IPathSetter {
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

  setPath (path: string, value: any) : void {
    const pathArray = path.split('.')
    const topLevelElement = pathArray.splice(0, 1)[0]

    switch (topLevelElement) {
      case 'id':
        if (value !== null) {
          this.id = Number(value)
        } else {
          this.id = null
        }
        break
      case 'subject':
        this.subject = String(value)
        break
      case 'contact':
        if (value !== null) {
          this.contact = Contact.createFromObject(value)
        } else {
          this.contact = null
        }
        break
      default:
        throw new TypeError('path ' + path + ' is not value')
    }
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
