/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { IOptionsForActionType as DeviceActionOptionType } from '@/store/devices'
import { IOptionsForActionType as PlatformActionOptionType } from '@/store/platforms'
import { IOptionsForActionType as ConfigurationActionOptionType } from '@/store/configurations'

export interface IActionKind {
  kind: string
}

export const KIND_OF_ACTION_TYPE_GENERIC_ACTION = 'generic_action'
export const KIND_OF_ACTION_TYPE_UNKNOWN = 'unknown'
export const KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE = 'software_update'
export const KIND_OF_ACTION_TYPE_PARAMETER_CHANGE_ACTION = 'parameter_change_action'

export const KIND_OF_ACTION_TYPE_DEVICE_CALIBRATION = 'device_calibration'
export const KIND_OF_ACTION_TYPE_DEVICE_MOUNT = 'device_mount'
export const KIND_OF_ACTION_TYPE_DEVICE_UNMOUNT = 'device_unmount'

export const KIND_OF_ACTION_TYPE_PLATFORM_MOUNT = 'platform_mount'
export const KIND_OF_ACTION_TYPE_PLATFORM_UNMOUNT = 'platform_unmount'

export const KIND_OF_ACTION_TYPE_STATIC_LOCATION_BEGIN = 'static_location_begin'
export const KIND_OF_ACTION_TYPE_STATIC_LOCATION_END = 'static_location_end'
export const KIND_OF_ACTION_TYPE_DYNAMIC_LOCATION_BEGIN = 'dynamic_location_begin'
export const KIND_OF_ACTION_TYPE_DYNAMIC_LOCATION_END = 'dynamic_location_end'

export type KindOfDeviceActionType =
  typeof KIND_OF_ACTION_TYPE_DEVICE_CALIBRATION
  | typeof KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE
  | typeof KIND_OF_ACTION_TYPE_GENERIC_ACTION
  | typeof KIND_OF_ACTION_TYPE_UNKNOWN
  | typeof KIND_OF_ACTION_TYPE_DEVICE_MOUNT
  | typeof KIND_OF_ACTION_TYPE_DEVICE_UNMOUNT
  | typeof KIND_OF_ACTION_TYPE_PARAMETER_CHANGE_ACTION

export type KindOfPlatformAction =
  typeof KIND_OF_ACTION_TYPE_SOFTWARE_UPDATE
  | typeof KIND_OF_ACTION_TYPE_GENERIC_ACTION
  | typeof KIND_OF_ACTION_TYPE_UNKNOWN
  | typeof KIND_OF_ACTION_TYPE_PLATFORM_MOUNT
  | typeof KIND_OF_ACTION_TYPE_PLATFORM_UNMOUNT
  | typeof KIND_OF_ACTION_TYPE_PARAMETER_CHANGE_ACTION

export type KindOfConfigurationAction =
  typeof KIND_OF_ACTION_TYPE_GENERIC_ACTION | typeof KIND_OF_ACTION_TYPE_PARAMETER_CHANGE_ACTION

export const deviceParameterChangeActionOption: DeviceActionOptionType = {
  id: 'parameter_change_action',
  name: 'Parameter Value Change',
  uri: '',
  kind: KIND_OF_ACTION_TYPE_PARAMETER_CHANGE_ACTION
}

export const platformParameterChangeActionOption: PlatformActionOptionType = {
  id: 'parameter_change_action',
  name: 'Parameter Value Change',
  uri: '',
  kind: KIND_OF_ACTION_TYPE_PARAMETER_CHANGE_ACTION
}

export const configurationParameterChangeActionOption: ConfigurationActionOptionType = {
  id: 'parameter_change_action',
  name: 'Parameter Value Change',
  uri: '',
  kind: KIND_OF_ACTION_TYPE_PARAMETER_CHANGE_ACTION
}
