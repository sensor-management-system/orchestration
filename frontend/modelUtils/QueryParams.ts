/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

/**
 * the Vue route query params are defined (but not exported) in
 * vue-router/types as:
 *
 *   Dictionary<string | (string | null)[]>
 *
 * where Dictionary is defined as:
 *
 *   type Dictionary<T> = { [key: string]: T }
 *
 */
export type QueryParams = {
  [param: string]: string | (string | null)[]
}
