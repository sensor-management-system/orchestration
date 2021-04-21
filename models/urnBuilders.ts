/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
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

import { Device } from '@/models/Device'
import { Manufacturer } from '@/models/Manufacturer'
import { Platform } from '@/models/Platform'
import { PlatformType } from '@/models/PlatformType'

export function createPlatformUrn (platform: Platform, platformTypes: PlatformType[]): string {
  let partType: string = '[platformtype]'
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

  const partShortName: string = platform.shortName || '[short_name]'

  return [partType, partShortName]
    .join('_')
    .replace(/\s/g, '_')
}

export function createDeviceUrn (device: Device, manufacturers: Manufacturer[]): string {
  let partManufacturer: string = '[manufacturer]'
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

  const partModel: string = device.model || '[model]'
  const partSerialNumber: string = device.serialNumber || '[serial_number]'

  return [partManufacturer, partModel, partSerialNumber]
    .join('_')
    .replace(/\s/g, '_')
}
