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
import { MeasuringRange } from '@/models/MeasuringRange'
import { DeviceProperty } from '@/models/DeviceProperty'

describe('DeviceProperty Models', () => {
  it('should create a DeviceProperty from an object', () => {
    const prop = DeviceProperty.createFromObject({
      id: null,
      label: 'test',
      compartmentUri: 'http://foo/compartment/1',
      compartmentName: 'bar',
      unitUri: 'http://foo/unit/1',
      unitName: 'mm',
      samplingMediaUri: 'http://foo/samplingMedia/1',
      samplingMediaName: 'water',
      propertyUri: 'http://foo/property/1',
      propertyName: 'foo.bar',
      measuringRange: {
        min: 10,
        max: 1000
      },
      accuracy: 0.1,
      failureValue: 0.01
    })
    expect(typeof prop).toBe('object')
    expect(prop).toHaveProperty('id', null)
    expect(prop).toHaveProperty('label', 'test')
    expect(prop).toHaveProperty('compartmentUri', 'http://foo/compartment/1')
    expect(prop).toHaveProperty('compartmentName', 'bar')
    expect(prop).toHaveProperty('unitUri', 'http://foo/unit/1')
    expect(prop).toHaveProperty('unitName', 'mm')
    expect(prop).toHaveProperty('samplingMediaUri', 'http://foo/samplingMedia/1')
    expect(prop).toHaveProperty('samplingMediaName', 'water')
    expect(prop).toHaveProperty('propertyUri', 'http://foo/property/1')
    expect(prop).toHaveProperty('propertyName', 'foo.bar')
    expect(prop).toHaveProperty('accuracy', 0.1)
    expect(prop).toHaveProperty('failureValue', 0.01)
    expect(prop.measuringRange instanceof MeasuringRange).toBe(true)
  })
})
