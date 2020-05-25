export default class CustomTextField {
  private _key: string = ''
  private _value: string = ''

  get key (): string {
    return this._key
  }

  set key (key: string) {
    this._key = key
  }
}
