/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'
import storeConfig from '@/store/configurations'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Contact } from '@/models/Contact'
import { DeviceProperty } from '@/models/DeviceProperty'
import { Device } from '@/models/Device'

describe('Configurations', () => {
  describe('getters', () => {
    it('it should return empty array if no devices are mounted', () => {
      const mockState = storeConfig.state()
      const mockGetters = {}
      const mockRootState = {}
      const mockRootGetters = {}

      const beginDate = DateTime.fromISO('2023-06-20T11:25:00.000Z', { zone: 'UTC' })
      const endDate = DateTime.fromISO('2023-06-22T12:00:00.000Z', { zone: 'UTC' })

      const activeDevicesWithPropertiesForDate = storeConfig.getters.activeDevicesWithPropertiesForDate(mockState, mockGetters, mockRootState, mockRootGetters)

      // Test with only start date
      const result1 = activeDevicesWithPropertiesForDate(beginDate)
      expect(result1).toEqual(expect.any(Array))
      expect(result1.length).toEqual(0)

      // Test with start date and end date
      const result2 = activeDevicesWithPropertiesForDate(beginDate, endDate)
      expect(result2).toEqual(expect.any(Array))
      expect(result2.length).toEqual(0)
    })

    it('should return a result if begin and end date are provided an suitable device mount action has no end date', () => {
      const mockState = storeConfig.state()
      const mockGetters = {}
      const mockRootState = {}
      const mockRootGetters = {}

      const device1 = new Device()
      device1.id = '1'
      device1.shortName = 'GPS'
      const prop1 = new DeviceProperty()
      prop1.id = '1'
      prop1.propertyName = 'GPS position, latitude'
      device1.properties = [prop1]

      const contact = new Contact()
      const action = DeviceMountAction.createFromObject({
        id: '1',
        device: device1,
        parentPlatform: null,
        parentDevice: null,
        beginDate: DateTime.fromISO('2023-06-19T11:25:00.000Z', { zone: 'UTC' }),
        endDate: null,
        offsetX: 0,
        offsetY: 0,
        offsetZ: 0,
        epsgCode: '',
        x: null,
        y: null,
        z: null,
        elevationDatumName: '',
        elevationDatumUri: '',
        beginContact: contact,
        endContact: null,
        beginDescription: '',
        endDescription: null,
        label: ''
      })

      mockState.deviceMountActionsIncludingDeviceInformation = [action]
      const beginDate = DateTime.fromISO('2023-06-20T11:25:00.000Z', { zone: 'UTC' })
      const endDate = DateTime.fromISO('2023-06-22T12:00:00.000Z', { zone: 'UTC' })

      const activeDevicesWithPropertiesForDate = storeConfig.getters.activeDevicesWithPropertiesForDate(mockState, mockGetters, mockRootState, mockRootGetters)
      const result = activeDevicesWithPropertiesForDate(beginDate, endDate)

      expect(result).toEqual(expect.any(Array))
      expect(result.length).toEqual(1)
    })
  })
})
