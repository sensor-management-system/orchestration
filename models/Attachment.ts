export interface IAttachment {
  id: number | null
  url: string
  label: string
}

export class Attachment implements IAttachment {
  static readonly mimeTypes: Object = {
    'image/png': ['png'],
    'images/jpeg': ['jpg', 'jpeg'],
    'application/pdf': ['pdf'],
    'text/plain': ['txt'],
    'text/rtf': ['rtf'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['docx'],
    'application/msword': ['doc'],
    'application/vnd.oasis.opendocument.text': ['odt']
  }

  private _id: number | null = null
  private _url: string = ''
  private _label: string = ''
  // @TODO: add an _uploadedAt field

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
