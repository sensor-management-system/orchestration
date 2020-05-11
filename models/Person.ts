export interface IPerson {
  id: number | null
  name: string
}

export default class Person implements IPerson {
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

  static createWithIdAndName (id: number, name: string): Person {
    const result = new Person()
    result.id = id
    result.name = name
    return result
  }

  static createEmpty (): Person {
    return new Person()
  }

  /**
   * creates an instance from another object
   *
   * @static
   * @param {IPerson} someObject - the object from which the new instance is to be created
   * @return {Person} the newly created instance
   */
  static createFromObject (someObject: IPerson): Person {
    const newObject = new Person()
    newObject.id = someObject.id
    newObject.name = someObject.name
    return newObject
  }
}
