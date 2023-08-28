/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *   (UFZ, https://www.ufz.de)
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
