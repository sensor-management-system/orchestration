/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
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
} from '@/modelUtils/urnBuilders'

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
      uri: 'https://foo.bar',
      definition: '',
      note: '',
      category: '',
      provenance: '',
      provenanceUri: '',
      globalProvenanceId: null
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
      definition: '',
      note: '',
      category: '',
      provenance: '',
      provenanceUri: '',
      globalProvenanceId: null,
      uri: 'https://foo.bar'
    })
    platform.platformTypeUri = platformType.uri
    platform.platformTypeName = platformType.name

    const urn: string = createPlatformUrn(platform, [platformType])
    const expectedUrn = `Test_Platformtype${PLATFORM_URN_SEPERATOR}My_Platform`

    expect(urn).toBe(expectedUrn)
  })
})
