/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { Device } from '@/models/Device'
import { Manufacturer } from '@/models/Manufacturer'
import { Platform } from '@/models/Platform'
import { PlatformType } from '@/models/PlatformType'

export const PLATFORM_URN_SEPERATOR = '_'
export const PLATFORM_URN_TYPE_PLACEHOLDER = '[platformtype]'
export const PLATFORM_URN_SHORT_NAME_PLACEHOLDER = '[short_name]'

export const DEVICE_URN_SEPERATOR = '_'
export const DEVICE_URN_MANUFACTURER_PLACEHOLDER = '[manufacturer]'
export const DEVICE_URN_MODEL_PLACEHOLDER = '[model]'
export const DEVICE_URN_SERIAL_NUMBER_PLACEHOLDER = '[serial_number]'

export function createPlatformUrn (platform: Platform, platformTypes: PlatformType[]): string {
  let partType: string = PLATFORM_URN_TYPE_PLACEHOLDER
  if (platform.platformTypeUri !== '') {
    const typeIndex: number = platformTypes.findIndex(t => t.uri === platform.platformTypeUri)
    if (typeIndex > -1) {
      partType = platformTypes[typeIndex].name
    } else if (platform.platformTypeName !== '') {
      partType = platform.platformTypeName
    }
  } else if (platform.platformTypeName !== '') {
    partType = platform.platformTypeName
  }

  const partShortName: string = platform.shortName || PLATFORM_URN_SHORT_NAME_PLACEHOLDER

  return [partType, partShortName]
    .join(PLATFORM_URN_SEPERATOR)
    .replace(/\s/g, '_')
}

export function createDeviceUrn (device: Device, manufacturers: Manufacturer[]): string {
  let partManufacturer: string = DEVICE_URN_MANUFACTURER_PLACEHOLDER
  if (device.manufacturerUri !== '') {
    const manIndex: number = manufacturers.findIndex(m => m.uri === device.manufacturerUri)
    if (manIndex > -1) {
      partManufacturer = manufacturers[manIndex].name
    } else if (device.manufacturerName !== '') {
      partManufacturer = device.manufacturerName
    }
  } else if (device.manufacturerName !== '') {
    partManufacturer = device.manufacturerName
  }

  const partModel: string = device.model || DEVICE_URN_MODEL_PLACEHOLDER
  const partSerialNumber: string = device.serialNumber || DEVICE_URN_SERIAL_NUMBER_PLACEHOLDER

  return [partManufacturer, partModel, partSerialNumber]
    .join(DEVICE_URN_SEPERATOR)
    .replace(/\s/g, '_')
}
