/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2022
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
