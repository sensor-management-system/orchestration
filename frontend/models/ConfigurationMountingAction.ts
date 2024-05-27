/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'
import { Device } from '@/models/Device'
import { Platform } from '@/models/Platform'

export interface IConfigurationMountingAction {
  attributes: Device | Platform,
  timepoint: DateTime,
  type: string
}

export class ConfigurationMountingAction implements IConfigurationMountingAction {
  private _attributes: Device | Platform
  private _timepoint: DateTime
  private _type: string

  constructor (
    attributes: Device | Platform,
    timepoint: DateTime,
    type: string
  ) {
    this._attributes = attributes
    this._timepoint = timepoint
    this._type = type
  }

  get attributes (): Device | Platform {
    return this._attributes
  }

  set attributes (newAttribute: Device | Platform) {
    this._attributes = newAttribute
  }

  get timepoint (): DateTime {
    return this._timepoint
  }

  set timepoint (newTimepoint: DateTime) {
    this._timepoint = newTimepoint
  }

  get type (): string {
    return this._type
  }

  set type (newType: string) {
    this._type = newType
  }
}
