export default class PlatformType {
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
    this._name = newName
  }

  static createWithIdAndName (id: number, name: string): PlatformType {
    const result = new PlatformType()
    result.id = id
    result.name = name
    return result
  }

  static createEmpty (): PlatformType {
    return new PlatformType()
  }
}
