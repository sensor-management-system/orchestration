export default class PlatformStatus {
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

  static createWithData (id: number | null, name: string, uri: string): PlatformStatus {
    const result = new PlatformStatus()
    result.id = id
    result.name = name
    result.uri = uri
    return result
  }
}
