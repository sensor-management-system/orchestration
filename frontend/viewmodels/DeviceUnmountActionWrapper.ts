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
import { DeviceMountAction } from '@/models/views/devices/actions/DeviceMountAction'
import { Contact } from '@/models/Contact'
import { Attachment } from '@/models/Attachment'
import { IActionCommonDetails } from '@/models/ActionCommonDetails'
import { IDateCompareable } from '@/modelUtils/Compareables'
import { IActionKind, KIND_OF_ACTION_TYPE_DEVICE_UNMOUNT } from '@/models/ActionKind'

export class DeviceUnmountActionWrapper implements IActionCommonDetails, IDateCompareable, IActionKind {
  inner: DeviceMountAction

  constructor (inner: DeviceMountAction) {
    this.inner = inner
  }

  get id (): string {
    return this.inner.basicData.id
  }

  get description (): string {
    return this.inner.basicData.endDescription
  }

  get contact (): Contact {
    // Fallback to use the begin contact if we don't have the end Contact
    if (this.inner.endContact) {
      return Contact.createFromObject(this.inner.endContact)
    }
    return Contact.createFromObject(this.inner.beginContact)
  }

  get attachments (): Attachment[] {
    return []
  }

  get isDeviceUnmountAction (): boolean {
    return true
  }

  get date (): DateTime | null {
    return this.inner.basicData.endDate
  }

  get icon (): string {
    return 'mdi-network'
  }

  get color (): string {
    return 'red'
  }

  get kind (): string {
    return KIND_OF_ACTION_TYPE_DEVICE_UNMOUNT
  }

  get logicOrder (): number {
    return 300
  }
}
