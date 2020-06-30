import Contact from './Contact'

export default class User {
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
    this._subject = this.subject
  }

  get contact (): Contact | null {
    return this._contact
  }

  set contact (newContact: Contact | null) {
    this._contact = newContact
  }
}
