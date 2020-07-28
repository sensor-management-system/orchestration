import IPathSetter from './IPathSetter'

export interface IVariable {
  id: string
  name: string
  uri: string
}

export default class Variable implements IVariable, IPathSetter {
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

  setPath (path: string, value: any): void {
    const pathArray = path.split('.')
    const topLevelElement = pathArray.splice(0, 1)[0]

    switch (topLevelElement) {
      case 'id':
        this.id = String(value)
        break
      case 'name':
        this.name = String(value)
        break
      case 'uri':
        this.uri = String(value)
        break
      default:
        throw new TypeError('path ' + path + ' is not value')
    }
  }

  static createWithData (id: string, name: string, uri: string): Variable {
    const result = new Variable()
    result.id = id
    result.name = name
    result.uri = uri
    return result
  }

  static createFromObject (someObject: IVariable): Variable {
    const newObject = new Variable()

    newObject.id = someObject.id
    newObject.name = someObject.name
    newObject.uri = someObject.uri

    return newObject
  }
}
