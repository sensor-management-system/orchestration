import IPathSetter from './IPathSetter'

export interface IAttachment {
  id: number | null
  url: string
  label: string
}

export default class Attachment implements IAttachment, IPathSetter {
  private _id: number | null = null
  private _url: string = ''
  private _label: string = ''

  /**
   * creates an instance from another object
   *
   * @static
   * @param {IAttachment} someObject - the object from which the new instance is to be created
   * @return {Attachment} the newly created instance
   */
  static createFromObject (someObject: IAttachment) : Attachment {
    const attachment = new Attachment()
    attachment.id = someObject.id || null
    attachment.url = someObject.url || ''
    attachment.label = someObject.label || ''
    return attachment
  }

  /**
   * sets the path of the instance to value
   *
   * @param {string} path - the path to the property to be changed
   * @param {any} value - the value to set the property to
   */
  setPath (path: string, value: any): void {
    const properties = path.split('.')
    const property = properties.splice(0, 1)[0]
    switch (property) {
      case 'id':
        this.id = parseInt(value)
        break
      case 'url':
        this.url = String(value)
        break
      case 'label':
        this.label = String(value)
        break
      default:
        throw new TypeError('path ' + path + ' is not valid')
    }
  }

  get id (): number | null {
    return this._id
  }

  set id (id: number | null) {
    this._id = id
  }

  get url (): string {
    return this._url
  }

  set url (url: string) {
    this._url = url
  }

  get label (): string {
    return this._label
  }

  set label (label: string) {
    this._label = label
  }
}
