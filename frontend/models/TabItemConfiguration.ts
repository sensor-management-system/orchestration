/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
export interface ITabItem {
  name: string
  disabled?: boolean
}

export interface ITabItemRoute extends ITabItem {
  to: string
}

export interface ITabItemLink extends ITabItem {
  href: string
}

export type TabItemConfiguration = string | ITabItem | ITabItemRoute | ITabItemLink
