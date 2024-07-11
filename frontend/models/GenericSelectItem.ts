/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2022 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

/**
 * The interface defines a data structure for the following Vuetify components:
 * - VSelect
 * - VCombobox
 * - VAutocomplete
 */
export interface IGenericSelectItem<T> {
  text: string
  value: T
  disabled?: boolean
}
