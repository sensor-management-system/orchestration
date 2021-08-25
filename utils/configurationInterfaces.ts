/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Erik Pongratz (UFZ, erik.pongratz@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
 *   (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *   (UFZ, https://www.ufz.de)
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
import { Platform } from '@/models/Platform'
import { Contact } from '@/models/Contact'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { PlatformUnmountAction } from '@/models/PlatformUnmountAction'
import { DeviceUnmountAction } from '@/models/DeviceUnmountAction'

export interface IActionDateWithText {
  date: DateTime
  text: string
}

export interface IMountInfo {
  parentPlatform: Platform | null
  offsetX: number
  offsetY: number
  offsetZ: number
}

export interface ITimelineAction {
  key: string
  color: string
  icon: string
  date: DateTime
  title: string
  contact: Contact
  mountInfo: IMountInfo | null
  description: string
}

export class PlatformMountTimelineAction implements ITimelineAction {
  private mountAction: PlatformMountAction

  constructor (mountAction: PlatformMountAction) {
    this.mountAction = mountAction
  }

  get key (): string {
    return 'Platform-mount-action-' + this.mountAction.id
  }

  get color (): string {
    return 'blue'
  }

  get icon (): string {
    return 'mdi-rocket'
  }

  get date (): DateTime {
    return this.mountAction.date
  }

  get title (): string {
    return this.mountAction.platform.shortName + ' mounted'
  }

  get contact (): Contact {
    return this.mountAction.contact
  }

  get mountInfo (): IMountInfo {
    return {
      parentPlatform: this.mountAction.parentPlatform,
      offsetX: this.mountAction.offsetX,
      offsetY: this.mountAction.offsetY,
      offsetZ: this.mountAction.offsetZ
    }
  }

  get description (): string {
    return this.mountAction.description
  }
}

export class DeviceMountTimelineAction implements ITimelineAction {
  private mountAction: DeviceMountAction

  constructor (mountAction: DeviceMountAction) {
    this.mountAction = mountAction
  }

  get key (): string {
    return 'Device-mount-action-' + this.mountAction.id
  }

  get color (): string {
    return 'blue'
  }

  get icon (): string {
    return 'mdi-network'
  }

  get date (): DateTime {
    return this.mountAction.date
  }

  get title (): string {
    return this.mountAction.device.shortName + ' mounted'
  }

  get contact (): Contact {
    return this.mountAction.contact
  }

  get mountInfo (): IMountInfo {
    return {
      parentPlatform: this.mountAction.parentPlatform,
      offsetX: this.mountAction.offsetX,
      offsetY: this.mountAction.offsetY,
      offsetZ: this.mountAction.offsetZ
    }
  }

  get description (): string {
    return this.mountAction.description
  }
}

export class PlatformUnmountTimelineAction implements ITimelineAction {
  private unmountAction: PlatformUnmountAction

  constructor (unmountAction: PlatformUnmountAction) {
    this.unmountAction = unmountAction
  }

  get key (): string {
    return 'Platform-unmount-action-' + this.unmountAction.id
  }

  get color (): string {
    return 'red'
  }

  get icon (): string {
    return 'mdi-rocket'
  }

  get date (): DateTime {
    return this.unmountAction.date
  }

  get title (): string {
    return this.unmountAction.platform.shortName + ' unmounted'
  }

  get contact (): Contact {
    return this.unmountAction.contact
  }

  get mountInfo (): null {
    return null
  }

  get description (): string {
    return this.unmountAction.description
  }
}

export class DeviceUnmountTimelineAction implements ITimelineAction {
  private unmountAction: DeviceUnmountAction

  constructor (unmountAction: DeviceUnmountAction) {
    this.unmountAction = unmountAction
  }

  get key (): string {
    return 'Device-unmount-action-' + this.unmountAction.device.id + this.unmountAction.date.toString()
  }

  get color (): string {
    return 'red'
  }

  get icon (): string {
    return 'mdi-network'
  }

  get date (): DateTime {
    return this.unmountAction.date
  }

  get title (): string {
    return this.unmountAction.device.shortName + ' unmounted'
  }

  get contact (): Contact {
    return this.unmountAction.contact
  }

  get mountInfo (): null {
    return null
  }

  get description (): string {
    return this.unmountAction.description
  }
}
