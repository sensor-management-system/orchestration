export interface ICustomTextField {
  key: string,
  value: string
}

export class CustomTextField implements ICustomTextField {
  private _key: string = ''
  private _value: string = ''

  /**
   * creates an instance from another object
   *
   * @static
   * @param {ICustomTextField} someObject - the object from which the new instance is to be created
   * @return {CustomTextField} the newly created instance
   */
  static createFromObject (someObject: ICustomTextField) : CustomTextField {
    const newObject = new CustomTextField()

    newObject.key = someObject.key
    newObject.value = someObject.value

    return newObject
  }

  get key (): string {
    return this._key
  }

  set key (key: string) {
    this._key = key
  }

  get value (): string {
    return this._value
  }

  set value (value: string) {
    this._value = value
  }
}
