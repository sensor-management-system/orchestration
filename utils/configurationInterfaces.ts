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
