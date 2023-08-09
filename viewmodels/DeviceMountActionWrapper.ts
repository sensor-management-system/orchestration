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
