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

import {
  createDeviceUrn,
  createPlatformUrn,
  DEVICE_URN_SEPERATOR,
  DEVICE_URN_MODEL_PLACEHOLDER,
  DEVICE_URN_MANUFACTURER_PLACEHOLDER,
  DEVICE_URN_SERIAL_NUMBER_PLACEHOLDER,
  PLATFORM_URN_SEPERATOR,
  PLATFORM_URN_TYPE_PLACEHOLDER,
  PLATFORM_URN_SHORT_NAME_PLACEHOLDER
} from '@/models/urnBuilders'

describe('createDeviceUrn', () => {
  it('should return placeholders when no infos are available', () => {
    const device = new Device()

    const urn: string = createDeviceUrn(device, [])
    const expectedUrn = DEVICE_URN_MANUFACTURER_PLACEHOLDER + DEVICE_URN_SEPERATOR +
      DEVICE_URN_MODEL_PLACEHOLDER + DEVICE_URN_SEPERATOR +
      DEVICE_URN_SERIAL_NUMBER_PLACEHOLDER

    expect(urn).toBe(expectedUrn)
  })
  it('should return a meaningful string without whitespace', () => {
    const device = new Device()
    device.model = 'Some Model'
    device.serialNumber = '12345'

    const manufacturer = Manufacturer.createFromObject({
      id: '1',
      name: 'Test Manufacturer',
      uri: 'https://foo.bar'
    })
    device.manufacturerUri = manufacturer.uri
    device.manufacturerName = manufacturer.name

    const urn: string = createDeviceUrn(device, [manufacturer])
    const expectedUrn = `Test_Manufacturer${DEVICE_URN_SEPERATOR}Some_Model${DEVICE_URN_SEPERATOR}12345`

    expect(urn).toBe(expectedUrn)
  })
})

describe('createPlatformUrn', () => {
  it('should return placeholders when no infos are available', () => {
    const platform = new Platform()

    const urn: string = createPlatformUrn(platform, [])
    const expectedUrn = PLATFORM_URN_TYPE_PLACEHOLDER + PLATFORM_URN_SEPERATOR + PLATFORM_URN_SHORT_NAME_PLACEHOLDER

    expect(urn).toBe(expectedUrn)
  })
  it('should return a meaningful string without whitespace', () => {
    const platform = new Platform()
    platform.shortName = 'My Platform'

    const platformType = PlatformType.createFromObject({
      id: '1',
      name: 'Test Platformtype',
      uri: 'https://foo.bar'
    })
    platform.platformTypeUri = platformType.uri
    platform.platformTypeName = platformType.name

    const urn: string = createPlatformUrn(platform, [platformType])
    const expectedUrn = `Test_Platformtype${PLATFORM_URN_SEPERATOR}My_Platform`

    expect(urn).toBe(expectedUrn)
  })
})
