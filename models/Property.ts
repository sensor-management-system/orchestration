export interface IProperty {
  id: string
  name: string
  uri: string
}

export class Property implements IProperty {
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

  static createWithData (id: string, name: string, uri: string): Property {
    const result = new Property()
    result.id = id
    result.name = name
    result.uri = uri
    return result
  }

  static createFromObject (someObject: IProperty): Property {
    const newObject = new Property()

    newObject.id = someObject.id
    newObject.name = someObject.name
    newObject.uri = someObject.uri

    return newObject
  }
}
