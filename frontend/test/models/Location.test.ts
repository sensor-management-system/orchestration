/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { StationaryLocation, DynamicLocation } from '@/models/Location'
import { DeviceProperty } from '@/models/DeviceProperty'

describe('StationaryLocation', () => {
  it('should create a StationaryLocation from an object', () => {
    const location = StationaryLocation.createFromObject({ latitude: 50.986451, longitude: 12.973538, elevation: 280 })
    expect(typeof location).toBe('object')
    expect(location).toHaveProperty('latitude', 50.986451)
    expect(location).toHaveProperty('longitude', 12.973538)
    expect(location).toHaveProperty('elevation', 280)
  })
})

describe('DynamicLocation', () => {
  it('should create a DynamicLocation from an object', () => {
    const latitude = new DeviceProperty()
    const longitude = new DeviceProperty()
    const elevation = new DeviceProperty()

    const location = DynamicLocation.createFromObject({ latitude, longitude, elevation })
    expect(typeof location).toBe('object')
    expect(location).toHaveProperty('latitude', latitude)
    expect(location).toHaveProperty('longitude', longitude)
    expect(location).toHaveProperty('elevation', elevation)
  })
})
