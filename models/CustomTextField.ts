import IPathSetter from './IPathSetter'

export interface ICustomTextField {
  key: string,
  value: string
}

export class CustomTextField implements ICustomTextField, IPathSetter {
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

  /**
   * sets the value at the given path
   *
   * @param {string} path - the path (property name) to the value
   * @param {any} value - the value to set
   */
  setPath (path: string, value: any): void {
    switch (path) {
      case 'key':
        this.key = String(value)
        break
      case 'value':
        this.value = String(value)
        break
      default:
        throw new TypeError('path ' + path + ' is not valid')
    }
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
