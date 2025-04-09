/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2025
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'
import { TsmLinking } from '@/models/TsmLinking'
import { Device } from '@/models/Device'
import { DeviceProperty } from '@/models/DeviceProperty'
import { TSMLinkingDateFilter, TSMLinkingDateFilterOperation } from '@/store/tsmLinking'
import {
  filterLinkings,
  matchesDateFilter,
  matchesDeviceSelection,
  matchesMeasuredQuantitiesSelection
} from '@/utils/dataLinkingHelper'

describe('matchesDeviceSelection', () => {
  it('returns true if linking device is null and no devices are selected', () => {
    const linking = new TsmLinking()
    linking.device = null
    const selectedDevices: Device[] = []

    expect(matchesDeviceSelection(linking, selectedDevices)).toBe(true)
  })

  it('returns false if linking device is null and devices are selected', () => {
    const linking = new TsmLinking()
    linking.device = null
    const device = new Device()
    device.shortName = 'Device 1'
    const selectedDevices: Device[] = [device]

    expect(matchesDeviceSelection(linking, selectedDevices)).toBe(false)
  })

  it('returns true if linking device matches selected device', () => {
    const linking = new TsmLinking()
    const linkingDevice = new Device()
    linkingDevice.shortName = 'Device 1'
    linkingDevice.serialNumber = '123'
    linking.device = linkingDevice

    const selectedDevice = new Device()
    selectedDevice.shortName = 'Device 1'
    selectedDevice.serialNumber = '123'
    const selectedDevices: Device[] = [selectedDevice]
    expect(matchesDeviceSelection(linking, selectedDevices)).toBe(true)
  })

  it('returns false if linking device does not match selected device', () => {
    const linking = new TsmLinking()
    const linkingDevice = new Device()
    linkingDevice.shortName = 'Device 1'
    linkingDevice.serialNumber = '123'
    linking.device = linkingDevice

    const selectedDevice = new Device()
    selectedDevice.shortName = 'Device 2'
    selectedDevice.serialNumber = '456'
    const selectedDevices: Device[] = [selectedDevice]

    expect(matchesDeviceSelection(linking, selectedDevices)).toBe(false)
  })
})

describe('matchesMeasuredQuantitiesSelection', () => {
  it('returns true if linking device property is null and no device properties are selected', () => {
    const linking = new TsmLinking()
    linking.deviceProperty = null
    const selectedMeasuredQuantities: DeviceProperty[] = []

    expect(matchesMeasuredQuantitiesSelection(linking, selectedMeasuredQuantities)).toBe(true)
  })

  it('returns false if linking device property is null and device properties are selected', () => {
    const linking = new TsmLinking()
    linking.deviceProperty = null
    const deviceProperty = new DeviceProperty()
    deviceProperty.propertyName = 'Property 1'
    const selectedMeasuredQuantities: DeviceProperty[] = [deviceProperty]

    expect(matchesMeasuredQuantitiesSelection(linking, selectedMeasuredQuantities)).toBe(false)
  })

  it('returns true if linking device property matches selected device property', () => {
    const linking = new TsmLinking()
    const linkingDeviceProperty = new DeviceProperty()
    linkingDeviceProperty.propertyName = 'Property 1'
    linking.deviceProperty = linkingDeviceProperty

    const selectedDeviceProperty = new DeviceProperty()
    selectedDeviceProperty.propertyName = 'Property 1'
    const selectedMeasuredQuantities: DeviceProperty[] = [selectedDeviceProperty]

    expect(matchesMeasuredQuantitiesSelection(linking, selectedMeasuredQuantities)).toBe(true)
  })

  it('returns false if linking device property does not match selected device property', () => {
    const linking = new TsmLinking()
    const linkingDeviceProperty = new DeviceProperty()
    linkingDeviceProperty.propertyName = 'Property 1'
    linking.deviceProperty = linkingDeviceProperty

    const selectedDeviceProperty = new DeviceProperty()
    selectedDeviceProperty.propertyName = 'Property 2'
    const selectedMeasuredQuantities: DeviceProperty[] = [selectedDeviceProperty]

    expect(matchesMeasuredQuantitiesSelection(linking, selectedMeasuredQuantities)).toBe(false)
  })
})

describe('matchesDateFilter', () => {
  it('returns true if date to check is null and no date filter is applied', () => {
    const dateToCheck: DateTime | null = null
    const dateFilter: TSMLinkingDateFilter | null = null

    expect(matchesDateFilter(dateToCheck, dateFilter)).toBe(true)
  })

  it('returns false if date to check is null and date filter is applied', () => {
    const dateToCheck: DateTime | null = null
    const dateFilter = {
      date: DateTime.utc().set({ second: 0, millisecond: 0 }),
      operation: {
        id: TSMLinkingDateFilterOperation.LTE,
        text: 'earlier than or equals'
      }
    }

    expect(matchesDateFilter(dateToCheck, dateFilter)).toBe(false)
  })

  it('returns true if date to check is before date filter (LTE)', () => {
    const dateToCheck = DateTime.utc(2022, 1, 1)
    const dateFilter = {
      date: DateTime.utc(2022, 1, 1),
      operation: {
        id: TSMLinkingDateFilterOperation.LTE,
        text: 'earlier than or equals'
      }
    }
    expect(matchesDateFilter(dateToCheck, dateFilter)).toBe(true)
  })

  it('returns false if date to check is after date filter (LTE)', () => {
    const dateToCheck = DateTime.utc(2022, 1, 3)
    const dateFilter = {
      date: DateTime.utc(2022, 1, 1),
      operation: {
        id: TSMLinkingDateFilterOperation.LTE,
        text: 'earlier than or equals'
      }
    }

    expect(matchesDateFilter(dateToCheck, dateFilter)).toBe(false)
  })

  it('returns true if date to check is after date filter (GTE)', () => {
    const dateToCheck = DateTime.utc(2022, 1, 3)
    const dateFilter = {
      date: DateTime.utc(2022, 1, 2),
      operation: {
        id: TSMLinkingDateFilterOperation.GTE,
        text: 'later than or equals'
      }
    }

    expect(matchesDateFilter(dateToCheck, dateFilter)).toBe(true)
  })

  it('returns false if date to check is before date filter (GTE)', () => {
    const dateToCheck = DateTime.utc(2022, 1, 1)
    const dateFilter = {
      date: DateTime.utc(2022, 1, 2),
      operation: {
        id: TSMLinkingDateFilterOperation.GTE,
        text: 'later than or equals'
      }
    }

    expect(matchesDateFilter(dateToCheck, dateFilter)).toBe(false)
  })
})

describe('filterLinkings', () => {
  it('returns an empty array if no linkings match the filters', () => {
    const linking1 = new TsmLinking()
    linking1.device = new Device()
    linking1.device.shortName = 'Device 1'
    linking1.deviceProperty = new DeviceProperty()
    linking1.deviceProperty.propertyName = 'Property 1'
    linking1.startDate = DateTime.utc(2022, 1, 1)

    const linking2 = new TsmLinking()
    linking2.device = new Device()
    linking2.device.shortName = 'Device 2'
    linking2.deviceProperty = new DeviceProperty()
    linking2.deviceProperty.propertyName = 'Property 2'
    linking2.startDate = DateTime.utc(2022, 1, 2)

    const linkings: TsmLinking[] = [linking1, linking2]
    const selectedDevices: Device[] = []
    const selectedMeasuredQuantities: DeviceProperty[] = []
    const startDateFilter: TSMLinkingDateFilter | null = null
    const endDateFilter: TSMLinkingDateFilter | null = null

    const filteredLinkings = filterLinkings(linkings, selectedDevices, selectedMeasuredQuantities, startDateFilter, endDateFilter)
    expect(filteredLinkings.length).toEqual(2)
  })

  it('returns the linkings that match the filters', () => {
    const linking1 = new TsmLinking()
    linking1.device = new Device()
    linking1.device.shortName = 'Device 1'
    linking1.deviceProperty = new DeviceProperty()
    linking1.deviceProperty.propertyName = 'Property 1'
    linking1.startDate = DateTime.utc(2022, 1, 1)

    const linking2 = new TsmLinking()
    linking2.device = new Device()
    linking2.device.shortName = 'Device 2'
    linking2.deviceProperty = new DeviceProperty()
    linking2.deviceProperty.propertyName = 'Property 2'
    linking2.startDate = DateTime.utc(2022, 1, 2)

    const linkings: TsmLinking[] = [linking1, linking2]
    const selectedDevice = new Device()
    selectedDevice.shortName = 'Device 1'
    const selectedDevices: Device[] = [selectedDevice]

    const selectedDeviceProperty = new DeviceProperty()
    selectedDeviceProperty.propertyName = 'Property 1'
    const selectedMeasuredQuantities: DeviceProperty[] = [selectedDeviceProperty]

    const startDateFilter: TSMLinkingDateFilter | null = null
    const endDateFilter: TSMLinkingDateFilter | null = null

    const filteredLinkings = filterLinkings(linkings, selectedDevices, selectedMeasuredQuantities, startDateFilter, endDateFilter)
    expect(filteredLinkings).toEqual([linking1])
  })
})
