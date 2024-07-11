/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

export class ConfigurationStatusApi {
  newSearchBuilder (): ConfigurationStatusSearchBuilder {
    return new ConfigurationStatusSearchBuilder()
  }

  findAll (): Promise<string[]> {
    return this.newSearchBuilder().build().findMatchingAsList()
  }
}

export class ConfigurationStatusSearchBuilder {
  build (): ConfigurationStatusSeacher {
    return new ConfigurationStatusSeacher()
  }
}

export class ConfigurationStatusSeacher {
  findMatchingAsList (): Promise<string[]> {
    return new Promise<string[]>((resolve) => {
      resolve(['draft', 'active', 'deprecated'])
    })
  }
}
