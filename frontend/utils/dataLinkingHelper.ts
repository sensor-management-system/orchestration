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

export function matchesDeviceSelection (linking: TsmLinking, selectedDevices: Device[]) {
  const isMatchingDevice = (device: Device) => {
    if (device.serialNumber && linking.device!.serialNumber) {
      return device.shortName === linking.device!.shortName && device.serialNumber === linking.device!.serialNumber
    }
    return device.shortName === linking.device!.shortName
  }

  if (linking.device === null) {
    // the linking has no device, so we should exclude the linking if there are selected devices
    return selectedDevices.length === 0
  } else {
    return selectedDevices.length === 0 || selectedDevices.some(isMatchingDevice)
  }
}

export function matchesMeasuredQuantitiesSelection (linking: TsmLinking, selectedMeasuredQuantities: DeviceProperty[]) {
  const isMatchingMeasuredQuantitiesSelection = (deviceProperty: DeviceProperty) => {
    return deviceProperty.propertyName === linking.deviceProperty!.propertyName
  }

  if (linking.deviceProperty === null) {
    // the linking has no deviceProperty, so we should exclude the linking if there are selected device properties
    return selectedMeasuredQuantities.length === 0
  } else {
    return selectedMeasuredQuantities.length === 0 || selectedMeasuredQuantities.some(isMatchingMeasuredQuantitiesSelection)
  }
}

export function matchesDateFilter (dateToCheck: DateTime | null, dateFilter: TSMLinkingDateFilter | null): boolean {
  if (dateToCheck === null) {
    return dateFilter === null
  }

  if (dateFilter === null) {
    return true
  }

  switch (dateFilter.operation.id) {
    case TSMLinkingDateFilterOperation.LTE:
      return dateToCheck <= dateFilter.date
    case TSMLinkingDateFilterOperation.GTE:
      return dateToCheck >= dateFilter.date
    default:
      // This should never happen, as the operation id is an enum value
      throw new Error(`Invalid operation id: ${dateFilter.operation.id}`)
  }
}

export function filterLinkings (linkings: TsmLinking[], selectedDevices: Device[], selectedMeasuredQuantities: DeviceProperty[], startDateFilter: TSMLinkingDateFilter | null, endDateFilter: TSMLinkingDateFilter | null): TsmLinking[] {
  const filteredLinkings = linkings.filter((linking: TsmLinking) => {
    return matchesDeviceSelection(linking, selectedDevices) &&
      matchesMeasuredQuantitiesSelection(linking, selectedMeasuredQuantities) &&
      matchesDateFilter(linking.startDate, startDateFilter) &&
      matchesDateFilter(linking.startDate, endDateFilter)
  })

  return filteredLinkings
}
