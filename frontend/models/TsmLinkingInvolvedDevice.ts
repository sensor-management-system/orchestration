/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

export interface ITsmLinkingInvolvedDevice {
  id: string | null
  deviceId: string | null
  orderIndex: number | null
}

export class TsmLinkingInvolvedDevice implements ITsmLinkingInvolvedDevice {
  private _id: string | null = null
  private _deviceId: string | null = null
  private _orderIndex: number | null = null

  get id (): string | null {
    return this._id
  }

  set id (newId: string | null) {
    this._id = newId
  }

  get deviceId (): string | null {
    return this._deviceId
  }

  set deviceId (newDeviceId: string | null) {
    this._deviceId = newDeviceId
  }

  get orderIndex (): number | null {
    return this._orderIndex
  }

  set orderIndex (newOrderIndex: number | null) {
    this._orderIndex = newOrderIndex
  }

  static createFromObject (someObject: ITsmLinkingInvolvedDevice) {
    const result = new TsmLinkingInvolvedDevice()
    result.id = someObject.id
    result.deviceId = someObject.deviceId
    result.orderIndex = someObject.orderIndex
    return result
  }
}
