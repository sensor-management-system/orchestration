/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2022
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

import { IMountAction, MountAction } from '@/models/MountAction'
import { Contact } from '@/models/Contact'
import { Configuration } from '@/models/Configuration'

export interface IConfigurationMountAction extends IMountAction {
  configuration: Configuration
}

/**
 * This class is just used for convenience. It basically wraps a Configuration
 * and provides an unified access to begin- and enddate of a configuration when
 * used as a root node in a `ConfigurationTree`.
 *
 * Note that there is no corresponding `ConfigurationMountAction` concept in the
 * backend. That's the reason why this class is located in the `viewmodels`
 * folder.
 *
 * @implements IConfigurationMountAction
 */
export class ConfigurationMountAction extends MountAction implements IConfigurationMountAction {
  private _configuration: Configuration

  constructor (
    configuration: Configuration
  ) {
    super(
      '',
      null,
      // as we're not allowed to return `null`, we return 1970-01-01
      configuration.startDate || DateTime.fromSeconds(0),
      configuration.endDate,
      0,
      0,
      0,
      // we need a contact, so we take the first one we can get or create an
      // empty one
      configuration.contacts.length ? Contact.createFromObject(configuration.contacts[0]) : new Contact(),
      null,
      '',
      null
    )
    this._configuration = configuration
  }

  get TYPE (): string {
    return 'CONFIGURATION_MOUNT_ACTION'
  }

  get configuration (): Configuration {
    return this._configuration
  }

  isConfigurationMountAction (): this is IConfigurationMountAction {
    return true
  }

  static createFromObject (otherAction: Omit<IConfigurationMountAction, 'TYPE'>): ConfigurationMountAction {
    return new ConfigurationMountAction(
      Configuration.createFromObject(otherAction.configuration)
    )
  }
}
