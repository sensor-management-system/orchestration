export interface IUnit {
  id: string
  name: string
  uri: string
}

export class Unit implements IUnit {
  private _id: string = ''
  private _name: string = ''
  private _uri: string = ''

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

  toString (): string {
    return this._name
  }

  static createWithData (id: string, name: string, uri: string): Unit {
    const result = new Unit()
    result.id = id
    result.name = name
    result.uri = uri
    return result
  }

  static createFromObject (someObject: IUnit): Unit {
    const newObject = new Unit()

    newObject.id = someObject.id
    newObject.name = someObject.name
    newObject.uri = someObject.uri

    return newObject
  }
}
