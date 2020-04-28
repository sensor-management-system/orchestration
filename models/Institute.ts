export default class Institute {
  private _id: number | null = null
  private _name: string = ''

  get id (): number | null {
    return this._id
  }

  set id (newId: number | null) {
    this._id = newId
  }

  get name (): string {
    return this._name
  }

  set name (newName: string) {
    this._name = name
  }

  static createWithIdAndName (id: number, name: string): Institute {
    const result = new Institute()
    result.id = id
    result.name = name
    return result
  }

  static createEmpty (): Institute {
    return new Institute()
  }
}
