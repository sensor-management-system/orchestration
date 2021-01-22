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
import { DateTime } from 'luxon'
import { Device } from '@/models/Device'
import { DeviceConfigurationAttributes } from '@/models/DeviceConfigurationAttributes'

describe('DeviceConfigurationAttributes', () => {
  it('should create a DeviceConfigurationAttributes object', () => {
    const device = new Device()
    device.id = '1'

    const attributes = new DeviceConfigurationAttributes(device)
    expect(attributes).toHaveProperty('device', device)
    expect(attributes).toHaveProperty('id', '1')
  })

  it('should create a DeviceConfigurationAttributes from an object', () => {
    const device = new Device()
    device.id = '1'

    const now = DateTime.utc()
    const attributes = DeviceConfigurationAttributes.createFromObject({ device, offsetX: 1, offsetY: 1, offsetZ: 1, calibrationDate: now })
    expect(typeof attributes).toBe('object')
    expect(attributes.device).toBe(device)
    expect(attributes).toHaveProperty('id', '1')
    expect(attributes).toHaveProperty('offsetX', 1)
    expect(attributes).toHaveProperty('offsetY', 1)
    expect(attributes).toHaveProperty('offsetZ', 1)
    expect(attributes).toHaveProperty('calibrationDate', now)
  })
})
