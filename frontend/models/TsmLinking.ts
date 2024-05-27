/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'
import { TsmdlDatasource } from '@/models/TsmdlDatasource'
import { TsmdlThing } from '@/models/TsmdlThing'
import { TsmdlDatastream } from '@/models/TsmdlDatastream'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Device } from '@/models/Device'
import { DeviceProperty } from '@/models/DeviceProperty'
import { TsmEndpoint } from '@/models/TsmEndpoint'

export interface ITsmLinking {
  id: string
  configurationId: string
  deviceMountAction: DeviceMountAction|null
  device: Device|null
  deviceProperty: DeviceProperty|null
  startDate: DateTime | null
  endDate: DateTime | null
  datasource: TsmdlDatasource | null
  thing: TsmdlThing | null
  datastream: TsmdlDatastream | null
  tsmEndpoint: TsmEndpoint | null
  licenseUri: string
  licenseName: string
  aggregationPeriod: number | null
}
export class TsmLinking implements ITsmLinking {
  private _id: string = ''
  private _configurationId: string = ''
  private _deviceMountAction: DeviceMountAction|null = null
  private _device: Device|null = null
  private _deviceProperty: DeviceProperty|null = null
  private _startDate: DateTime | null = null
  private _endDate: DateTime | null = null
  private _datasource: TsmdlDatasource | null = null
  private _thing: TsmdlThing | null = null
  private _datastream: TsmdlDatastream | null = null
  private _tsmEndpoint: TsmEndpoint | null = null
  private _licenseUri: string = ''
  private _licenseName: string = ''
  private _aggregationPeriod: number | null = null

  get id (): string {
    return this._id
  }

  set id (value: string) {
    this._id = value
  }

  get configurationId (): string {
    return this._configurationId
  }

  set configurationId (value: string) {
    this._configurationId = value
  }

  get deviceMountAction (): DeviceMountAction | null {
    return this._deviceMountAction
  }

  set deviceMountAction (value: DeviceMountAction | null) {
    this._deviceMountAction = value
  }

  get device (): Device | null {
    return this._device
  }

  set device (value: Device | null) {
    this._device = value
  }

  get deviceProperty (): DeviceProperty | null {
    return this._deviceProperty
  }

  set deviceProperty (value: DeviceProperty | null) {
    this._deviceProperty = value
  }

  get startDate (): DateTime | null {
    return this._startDate
  }

  set startDate (value: DateTime | null) {
    this._startDate = value
  }

  get endDate (): DateTime | null {
    return this._endDate
  }

  set endDate (value: DateTime | null) {
    this._endDate = value
  }

  get datasource (): TsmdlDatasource | null {
    return this._datasource
  }

  set datasource (value: TsmdlDatasource | null) {
    this._datasource = value
  }

  get thing (): TsmdlThing | null {
    return this._thing
  }

  set thing (value: TsmdlThing | null) {
    this._thing = value
  }

  get datastream (): TsmdlDatastream | null {
    return this._datastream
  }

  set datastream (value: TsmdlDatastream | null) {
    this._datastream = value
  }

  get tsmEndpoint (): TsmEndpoint | null {
    return this._tsmEndpoint
  }

  set tsmEndpoint (value: TsmEndpoint | null) {
    this._tsmEndpoint = value
  }

  get licenseName (): string {
    return this._licenseName
  }

  set licenseName (newLicenseName: string) {
    this._licenseName = newLicenseName
  }

  get licenseUri (): string {
    return this._licenseUri
  }

  set licenseUri (newLicenseUri: string) {
    this._licenseUri = newLicenseUri
  }

  get aggregationPeriod (): number | null {
    return this._aggregationPeriod
  }

  set aggregationPeriod (newAggregationPeriod: number | null) {
    this._aggregationPeriod = newAggregationPeriod
  }

  get aggregationText (): string {
    if (!this.aggregationPeriod) {
      return ''
    }
    const partPeriod = `${this.aggregationPeriod} s`
    if (this.deviceProperty?.aggregationTypeName) {
      const partType = this.deviceProperty?.aggregationTypeName
      return `${partPeriod} ${partType}`
    }
    return partPeriod
  }

  static createFromObject (someObject: ITsmLinking): TsmLinking {
    const result = new TsmLinking()
    result.id = someObject.id
    result.configurationId = someObject.configurationId
    result.datasource = someObject.datasource
    result.datastream = someObject.datastream
    result.device = someObject.device
    result.deviceMountAction = someObject.deviceMountAction
    result.deviceProperty = someObject.deviceProperty
    result.endDate = someObject.endDate
    result.startDate = someObject.startDate
    result.thing = someObject.thing
    result.tsmEndpoint = someObject.tsmEndpoint
    result.licenseName = someObject.licenseName
    result.licenseUri = someObject.licenseUri
    result.aggregationPeriod = someObject.aggregationPeriod
    return result
  }
}
