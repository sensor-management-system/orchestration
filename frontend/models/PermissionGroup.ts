/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
export interface IPermissionGroup {
  id: string | null
  name: string
  description: string
  equals (group: IPermissionGroup): boolean
}

export interface IPermissionableSingleGroup {
  permissionGroup: IPermissionGroup | null
}

export interface IPermissionableMultipleGroups {
  permissionGroups: IPermissionGroup[]
}

export interface IPersistentlyIdentifiable {
  persistentIdentifier?: string
}

export interface IArchivable {
  archived: boolean
}

export type IPermissionable = IPermissionableSingleGroup | IPermissionableMultipleGroups

export class PermissionGroup implements IPermissionGroup {
  private _id: string | null = null
  private _name: string = ''
  private _description: string = ''

  get id (): string | null {
    return this._id
  }

  set id (id: string | null) {
    this._id = id
  }

  get name (): string {
    return this._name
  }

  set name (name: string) {
    this._name = name
  }

  get description (): string {
    return this._description
  }

  set description (description: string) {
    this._description = description
  }

  toString (): string {
    return this._name
  }

  equals (group: PermissionGroup): boolean {
    return this.id === group.id
    // &&
    //  this.name === group.name &&
    //  this.description === group.description
    //
    // Why do we just compare the id? Actually we have different detailed levels of groups:
    // - detailed groups with name and description as retrieved from the /permission-groups endpoint
    // - groups with just the id as retrieved from the /user-info endpoint
  }

  /**
   * creates an instance from another object
   *
   * @static
   * @param {Partial<IPermissionGroup>} someObject - the object from which the new instance is to be created
   * @return {PermissionGroup} the newly created instance
   */
  static createFromObject (someObject: Partial<IPermissionGroup>): PermissionGroup {
    const permissionGroup = new PermissionGroup()
    if (typeof someObject.id !== 'undefined') {
      permissionGroup.id = someObject.id
    }
    if (someObject.name) {
      permissionGroup.name = someObject.name
    }
    if (someObject.description) {
      permissionGroup.description = someObject.description
    }
    return permissionGroup
  }
}
