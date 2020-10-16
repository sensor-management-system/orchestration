/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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
