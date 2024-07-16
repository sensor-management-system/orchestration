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
      '',
      null,
      null,
      null,
      '',
      '',
      // we need a contact, so we take the first one we can get or create an
      // empty one
      configuration.contacts.length ? Contact.createFromObject(configuration.contacts[0]) : new Contact(),
      null,
      '',
      null,
      configuration.label
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
