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
import { IActionKind, KIND_OF_ACTION_TYPE_DEVICE_MOUNT } from '@/models/ActionKind'

export class DeviceMountActionWrapper implements IActionCommonDetails, IDateCompareable, IActionKind {
  inner: DeviceMountAction

  constructor (inner: DeviceMountAction) {
    this.inner = inner
  }

  get id (): string {
    return this.inner.basicData.id
  }

  get description (): string {
    return this.inner.basicData.beginDescription
  }

  get contact (): Contact {
    return Contact.createFromObject(this.inner.beginContact)
  }

  get attachments (): Attachment[] {
    return []
  }

  get isDeviceMountAction (): boolean {
    return true
  }

  get date (): DateTime | null {
    return this.inner.basicData.beginDate
  }

  get icon (): string {
    return 'mdi-network'
  }

  get color (): string {
    return 'blue'
  }

  get kind (): string {
    return KIND_OF_ACTION_TYPE_DEVICE_MOUNT
  }

  get logicOrder (): number {
    return 200
  }
}
