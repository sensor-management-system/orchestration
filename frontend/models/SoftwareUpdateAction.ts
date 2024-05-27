/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'
import { Attachment } from '@/models/Attachment'
import { Contact } from '@/models/Contact'
import { IActionCommonDetails, ActionCommonDetails } from '@/models/ActionCommonDetails'
import { IDateCompareable } from '@/modelUtils/Compareables'
import { IActionKind, KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE } from '@/models/ActionKind'

export interface ISoftwareUpdateAction extends IActionCommonDetails {
  softwareTypeName: string
  softwareTypeUrl: string
  updateDate: DateTime | null
  version: string
  repositoryUrl: string
}

export class SoftwareUpdateAction extends ActionCommonDetails implements ISoftwareUpdateAction, IDateCompareable, IActionKind {
  private _softwareTypeName: string = ''
  private _softwareTypeUrl: string = ''
  private _updateDate: DateTime | null = null
  private _version: string = ''
  private _repositoryUrl: string = ''

  /**
   * returns an empty instance
   *
   * @static
   * @return {SoftwareUpdateAction} an empty instance
   */
  static createEmpty (): SoftwareUpdateAction {
    return new SoftwareUpdateAction()
  }

  /**
   * creates an instance from an existing ISoftwareUpdateAction-like object
   *
   * @static
   * @param {ISoftwareUpdateAction} someObject - an ISoftwareUpdateAction like object
   * @return {SoftwareUpdateAction} a cloned instance of the original object
   */
  static createFromObject (someObject: ISoftwareUpdateAction): SoftwareUpdateAction {
    const action = new SoftwareUpdateAction()
    action.id = someObject.id
    action.softwareTypeName = someObject.softwareTypeName
    action.softwareTypeUrl = someObject.softwareTypeUrl
    action.updateDate = someObject.updateDate
    action.version = someObject.version
    action.repositoryUrl = someObject.repositoryUrl
    action.description = someObject.description
    action.contact = someObject.contact ? Contact.createFromObject(someObject.contact) : null
    action.attachments = someObject.attachments.map(i => Attachment.createFromObject(i))
    return action
  }

  get softwareTypeUrl (): string {
    return this._softwareTypeUrl
  }

  set softwareTypeUrl (softwareTypeUrl: string) {
    this._softwareTypeUrl = softwareTypeUrl
  }

  get softwareTypeName (): string {
    return this._softwareTypeName
  }

  set softwareTypeName (softwareTypeName: string) {
    this._softwareTypeName = softwareTypeName
  }

  get updateDate (): DateTime | null {
    return this._updateDate
  }

  set updateDate (date: DateTime | null) {
    this._updateDate = date
  }

  get version (): string {
    return this._version
  }

  set version (version: string) {
    this._version = version
  }

  get repositoryUrl (): string {
    return this._repositoryUrl
  }

  set repositoryUrl (repositoryUrl: string) {
    this._repositoryUrl = repositoryUrl
  }

  get isSoftwareUpdateAction (): boolean {
    return true
  }

  get date (): DateTime | null {
    return this.updateDate
  }

  get icon (): string {
    return 'mdi-floppy'
  }

  get color (): string {
    return 'orange'
  }

  get kind (): string {
    return KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE
  }
}
