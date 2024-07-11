/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'

import { IMountAction, MountAction } from '@/models/MountAction'
import { Platform } from '@/models/Platform'
import { Contact } from '@/models/Contact'

export interface IPlatformMountAction extends IMountAction {
  platform: Platform
}

export class PlatformMountAction extends MountAction implements IPlatformMountAction {
  private _platform: Platform

  constructor (
    id: string,
    platform: Platform,
    parentPlatform: Platform | null,
    beginDate: DateTime,
    endDate: DateTime | null,
    offsetX: number,
    offsetY: number,
    offsetZ: number,
    epsgCode: string,
    x: number | null,
    y: number | null,
    z: number | null,
    elevationDatumName: string,
    elevationDatumUri: string,
    beginContact: Contact,
    endContact: Contact | null,
    beginDescription: string,
    endDescription: string | null
  ) {
    super(
      id,
      parentPlatform,
      beginDate,
      endDate,
      offsetX,
      offsetY,
      offsetZ,
      epsgCode,
      x,
      y,
      z,
      elevationDatumName,
      elevationDatumUri,
      beginContact,
      endContact,
      beginDescription,
      endDescription
    )
    this._platform = platform
  }

  get TYPE (): string {
    return 'PLATFORM_MOUNT_ACTION'
  }

  get platform (): Platform {
    return this._platform
  }

  isPlatformMountAction (): this is IPlatformMountAction {
    return true
  }

  static createFromObject (otherAction: Omit<IPlatformMountAction, 'TYPE'>): PlatformMountAction {
    return new PlatformMountAction(
      otherAction.id,
      Platform.createFromObject(otherAction.platform),
      otherAction.parentPlatform === null ? null : Platform.createFromObject(otherAction.parentPlatform),
      otherAction.beginDate,
      otherAction.endDate === null ? null : otherAction.endDate,
      otherAction.offsetX,
      otherAction.offsetY,
      otherAction.offsetZ,
      otherAction.epsgCode,
      otherAction.x,
      otherAction.y,
      otherAction.z,
      otherAction.elevationDatumName,
      otherAction.elevationDatumUri,
      Contact.createFromObject(otherAction.beginContact),
      otherAction.endContact === null ? null : Contact.createFromObject(otherAction.endContact),
      otherAction.beginDescription,
      otherAction.endDescription === null ? null : otherAction.endDescription
    )
  }
}
