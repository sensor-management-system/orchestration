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
export interface IPermissionGroup {
  id: string | null
  name: string
  description: string
  equals (group: IPermissionGroup): boolean
}

export interface IPermissionable {
  permissionGroups: IPermissionGroup[]
}

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
