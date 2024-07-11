/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { PlatformMountActionBasicData } from '@/models/basic/PlatformMountActionBasicData'
import { ConfigurationBasicData } from '@/models/basic/ConfigurationBasicData'
import { ContactBasicData } from '@/models/basic/ContactBasicData'
import { PlatformBasicData } from '@/models/basic/PlatformBasicData'

export interface IPlatformMountAction {
  basicData: PlatformMountActionBasicData
  configuration: ConfigurationBasicData
  beginContact: ContactBasicData
  endContact: ContactBasicData | null
  parentPlatform: PlatformBasicData | null
}

export class PlatformMountAction implements IPlatformMountAction {
  private _basicData: PlatformMountActionBasicData
  private _configuration: ConfigurationBasicData
  private _beginContact: ContactBasicData
  private _endContact: ContactBasicData | null
  private _parentPlatform: PlatformBasicData | null

  constructor (basicData: PlatformMountActionBasicData,
    configuration: ConfigurationBasicData,
    beginContact: ContactBasicData,
    endContact: ContactBasicData | null,
    parentPlatform: PlatformBasicData | null
  ) {
    this._basicData = basicData
    this._configuration = configuration
    this._beginContact = beginContact
    this._endContact = endContact
    this._parentPlatform = parentPlatform
  }

  get basicData (): PlatformMountActionBasicData {
    return this._basicData
  }

  get configuration (): ConfigurationBasicData {
    return this._configuration
  }

  get beginContact (): ContactBasicData {
    return this._beginContact
  }

  get endContact (): ContactBasicData | null {
    return this._endContact
  }

  get parentPlatform (): PlatformBasicData | null {
    return this._parentPlatform
  }

  static createFromObject (otherAction: IPlatformMountAction): PlatformMountAction {
    return new PlatformMountAction(
      PlatformMountActionBasicData.createFromObject(otherAction.basicData),
      ConfigurationBasicData.createFromObject(otherAction.configuration),
      ContactBasicData.createFromObject(otherAction.beginContact),
      otherAction.endContact == null ? null : ContactBasicData.createFromObject(otherAction.endContact),
      otherAction.parentPlatform === null ? null : PlatformBasicData.createFromObject(otherAction.parentPlatform)
    )
  }
}
