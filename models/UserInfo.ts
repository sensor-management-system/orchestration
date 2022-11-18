/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2022
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
 */
import { PermissionGroup } from '@/models/PermissionGroup'

export type PermissionGroupId = string

export interface IUserInfo {
  id: string | null
  active: boolean
  isSuperUser: boolean
  contactId: string | null
  member: PermissionGroupId[]
  admin: PermissionGroupId[]
  isMemberOf(group: PermissionGroup): boolean
  isAdminOf(group: PermissionGroup): boolean
}

const isGroupIdMatching = (groupId: PermissionGroupId, group: PermissionGroup) => group.id === groupId

export class UserInfo implements IUserInfo {
  private _id: string | null = null
  private _active: boolean = false
  private _isSuperUser: boolean = false
  private _contactId: string | null = null
  private _member: PermissionGroupId[] = []
  private _admin: PermissionGroupId[] = []

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

  get contactId () : string | null {
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
    if (someObject.contactId) {
      userinfo.contactId = someObject.contactId
    }
    if (someObject.member?.length) {
      userinfo.member = someObject.member.map(i => i)
    }
    if (someObject.admin?.length) {
      userinfo.admin = someObject.admin.map(i => i)
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
