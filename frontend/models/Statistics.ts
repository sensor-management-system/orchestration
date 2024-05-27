/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
export interface IStatisticsCount {
  configurations: number,
  devices: number,
  platforms: number,
  sites: number,
  users: number
}

export class StatisticsCount implements IStatisticsCount {
  private readonly _configurations: number = 0
  private readonly _devices: number = 0
  private readonly _platforms: number = 0
  private readonly _sites: number = 0
  private readonly _users: number = 0

  get configurations (): number {
    return this._configurations
  }

  get devices (): number {
    return this._devices
  }

  get platforms (): number {
    return this._platforms
  }

  get sites (): number {
    return this._sites
  }

  get users (): number {
    return this._users
  }
}
