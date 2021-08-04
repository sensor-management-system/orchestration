/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2021
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

import { IActionCommonDetails } from '@/models/ActionCommonDetails'
import { Api } from '@/services/Api'

/**
 * returns a color depending on the action type
 *
 * the color returned can be a Material color name as defined here:
 * https://vuetifyjs.com/en/styles/colors/#material-colors or a hexadecimal
 * HTML color code
 *
 * @param {IActionCommonDetails} action - the action to get the color for
 * @returns {string} the color
 */
export function getActionColor (action: IActionCommonDetails): string {
  switch (true) {
    case 'isGenericAction' in action:
      return 'blue'
    case 'isSoftwareUpdateAction' in action:
      return 'yellow'
    case 'isDeviceCalibrationAction' in action:
      return 'teal'
    case 'isDeviceMountAction' in action:
    case 'isPlatformMountAction' in action:
      return 'green'
    case 'isDeviceUnmountAction' in action:
    case 'isPlatformUnmountAction' in action:
      return 'grey darken-3'
  }
  return 'grey'
}

/**
 * Type for a function that returns the API method to delete an action
 */
export type ActionApiDeleteMethod = (id: string) => Promise<void>

/**
 * Common interface for all ActionApiDispatcher classes
 *
 * currently just defines a method to return the API method to delete an action
 */
export interface IActionApiDispatcher {
  getDeleteMethod (action: IActionCommonDetails): ActionApiDeleteMethod | undefined
}

/**
 * abstract class for the actions dispatchers which holds just an Api reference
 */
abstract class AbstractApiDispatcher {
  private _api: Api

  constructor (api: Api) {
    this._api = api
  }

  get api (): Api {
    return this._api
  }
}

/**
 * Api dispatcher for device related actions
 * @extends AbstractApiDispatcher
 * @implements IActionApiDispatcher
 */
export class DeviceActionApiDispatcher extends AbstractApiDispatcher implements IActionApiDispatcher {
  getDeleteMethod (action: IActionCommonDetails): ActionApiDeleteMethod | undefined {
    switch (true) {
      case 'isGenericAction' in action:
        return this.api.genericDeviceActions.deleteById.bind(this.api.genericDeviceActions)
      case 'isSoftwareUpdateAction' in action:
        return this.api.deviceSoftwareUpdateActions.deleteById.bind(this.api.deviceSoftwareUpdateActions)
      case 'isDeviceCalibrationAction' in action:
        return this.api.deviceCalibrationActions.deleteById.bind(this.api.deviceCalibrationActions)
    }
  }
}

/**
 * Api dispatcher for platform related actions
 * @extends AbstractApiDispatcher
 * @implements IActionApiDispatcher
 */
export class PlatformActionApiDispatcher extends AbstractApiDispatcher implements IActionApiDispatcher {
  getDeleteMethod (action: IActionCommonDetails): ActionApiDeleteMethod | undefined {
    switch (true) {
      case 'isGenericAction' in action:
        return this.api.genericPlatformActions.deleteById.bind(this.api.genericPlatformActions)
      case 'isSoftwareUpdateAction' in action:
        return this.api.platformSoftwareUpdateActions.deleteById.bind(this.api.platformSoftwareUpdateActions)
    }
  }
}
