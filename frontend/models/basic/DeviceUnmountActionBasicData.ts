/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2021
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'

/** Basically those classes and interfaces here
 *  define the "basic" view of the device unmount action data.
 *  This means this are the data explicitly for the entity
 *  without the need to make another joins or to include more
 *  data.
 */
export interface IDeviceUnmountActionBasicData {
  id: string
  date: DateTime
  description: string
}

export class DeviceUnmountActionBasicData implements IDeviceUnmountActionBasicData {
  private _id: string = ''
  private _date: DateTime
  private _description: string

  constructor (
    id: string,
    date: DateTime,
    description: string
  ) {
    this._id = id
    this._date = date
    this._description = description
  }

  get id (): string {
    return this._id
  }

  set id (newId: string) {
    this._id = newId
  }

  get date (): DateTime {
    return this._date
  }

  set date (newDate: DateTime) {
    this._date = newDate
  }

  get description (): string {
    return this._description
  }

  set description (newDescription: string) {
    this._description = newDescription
  }

  static createFromObject (otherAction: IDeviceUnmountActionBasicData): DeviceUnmountActionBasicData {
    return new DeviceUnmountActionBasicData(
      otherAction.id,
      otherAction.date,
      otherAction.description
    )
  }
}
