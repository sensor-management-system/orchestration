import IPathSetter from './IPathSetter'

export interface IManufacturer {
  id: number | null
  name: string
  uri: string
}

export default class Manufacturer implements IManufacturer, IPathSetter {
  private _id: number | null = null
  private _name: string = ''
  private _uri: string = ''

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
        if (value !== null) {
          this.id = Number(value)
        } else {
          this.id = null
        }
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

  static createWithData (id: number | null, name: string, uri: string): Manufacturer {
    const result = new Manufacturer()
    result.id = id
    result.name = name
    result.uri = uri
    return result
  }

  static createFromObject (someObject: IManufacturer): Manufacturer {
    const newObject = new Manufacturer()

    newObject.id = someObject.id
    newObject.name = someObject.name
    newObject.uri = someObject.uri

    return newObject
  }
}
