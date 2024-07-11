/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'
import { PermissionGroup } from '@/models/PermissionGroup'

export type PermissionGroupId = string

export interface IUserInfo {
  id: string | null
  active: boolean
  isSuperUser: boolean
  isExportControl: boolean
  contactId: string | null
  member: PermissionGroupId[]
  admin: PermissionGroupId[]
  apikey: string | null
  termsOfUseAgreementDate: DateTime | null
  isMemberOf(group: PermissionGroup): boolean
  isAdminOf(group: PermissionGroup): boolean
}

const isGroupIdMatching = (groupId: PermissionGroupId, group: PermissionGroup) => group.id === groupId

export class UserInfo implements IUserInfo {
  private _id: string | null = null
  private _active: boolean = false
  private _isSuperUser: boolean = false
  private _isExportControl: boolean = false
  private _contactId: string | null = null
  private _member: PermissionGroupId[] = []
  private _admin: PermissionGroupId[] = []
  private _apikey: string | null = null
  private _termsOfUseAgreementDate: DateTime | null = null

  get id (): string | null {
    return this._id
  }

  set id (id: string | null) {
    this._id = id
  }

  get active (): boolean {
    return this._active
  }

  set active (active: boolean) {
    this._active = active
  }

  get isSuperUser (): boolean {
    return this._isSuperUser
  }

  set isSuperUser (isSuperUser: boolean) {
    this._isSuperUser = isSuperUser
  }

  get isExportControl (): boolean {
    return this._isExportControl
  }

  set isExportControl (newIsExportControl: boolean) {
    this._isExportControl = newIsExportControl
  }

  get contactId (): string | null {
    return this._contactId
  }

  set contactId (newContactId: string | null) {
    this._contactId = newContactId
  }

  get member (): PermissionGroupId[] {
    return this._member
  }

  set member (member: PermissionGroupId[]) {
    this._member = member
  }

  isMemberOf (group: PermissionGroup): boolean {
    return this.member.find(someGroup => isGroupIdMatching(someGroup, group)) !== undefined
  }

  get admin (): PermissionGroupId[] {
    return this._admin
  }

  set admin (admin: PermissionGroupId[]) {
    this._admin = admin
  }

  isAdminOf (group: PermissionGroup): boolean {
    return this.admin.find(someGroup => isGroupIdMatching(someGroup, group)) !== undefined
  }

  get apikey (): string | null {
    return this._apikey
  }

  set apikey (newApikey: string | null) {
    this._apikey = newApikey
  }

  get termsOfUseAgreementDate (): DateTime | null {
    return this._termsOfUseAgreementDate
  }

  set termsOfUseAgreementDate (newDate: DateTime | null) {
    this._termsOfUseAgreementDate = newDate
  }

  /**
   * creates an instance from another object
   *
   * @static
   * @param {Partial<IUserInfo>} someObject - the object from which the new instance is to be created
   * @return {UserInfo} the newly created instance
   */
  static createFromObject (someObject: Partial<IUserInfo>): UserInfo {
    const userinfo = new UserInfo()
    if (typeof someObject.id !== 'undefined') {
      userinfo.id = someObject.id
    }
    if (someObject.active) {
      userinfo.active = someObject.active
    }
    if (someObject.isSuperUser) {
      userinfo.isSuperUser = someObject.isSuperUser
    }
    if (someObject.isExportControl) {
      userinfo.isExportControl = someObject.isExportControl
    }
    if (someObject.contactId) {
      userinfo.contactId = someObject.contactId
    }
    if (someObject.member?.length) {
      userinfo.member = someObject.member.map(i => i)
    }
    if (someObject.admin?.length) {
      userinfo.admin = someObject.admin.map(i => i)
    }
    if (someObject.apikey) {
      userinfo.apikey = someObject.apikey
    }
    if (someObject.termsOfUseAgreementDate === null || someObject.termsOfUseAgreementDate) {
      userinfo.termsOfUseAgreementDate = someObject.termsOfUseAgreementDate
    }
    return userinfo
  }
}

/**
 * A class that wraps the `UserInfo` class by forbidding setting properties and
 * enriching member and admin groups with full PermissionGroup instances
 */
export class DetailedUserInfo {
  private _userInfo: UserInfo
  private _member: PermissionGroup[] = []
  private _admin: PermissionGroup[] = []

  constructor (userInfo: UserInfo = new UserInfo(), permissionGroups: PermissionGroup[] = []) {
    this._userInfo = userInfo
    this._member = permissionGroups.filter(group => this._userInfo.isMemberOf(group))
    this._admin = permissionGroups.filter(group => this._userInfo.isAdminOf(group))
  }

  get id (): string | null {
    return this._userInfo.id
  }

  get active (): boolean {
    return this._userInfo.active
  }

  get isSuperUser (): boolean {
    return this._userInfo.isSuperUser
  }

  get member (): PermissionGroup[] {
    return this._member
  }

  isMemberOf (group: PermissionGroup): boolean {
    return this._userInfo.isMemberOf(group)
  }

  get admin (): PermissionGroup[] {
    return this._admin
  }

  isAdminOf (group: PermissionGroup): boolean {
    return this._userInfo.isAdminOf(group)
  }

  get groups (): PermissionGroup[] {
    return [
      ...this.member,
      ...this.admin.filter(adminGroup => !this.member.find(memberGroup => memberGroup.equals(adminGroup)))
    ]
  }
}
