/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

// We really want to do a recursive function definition here
// eslint-disable-next-line no-use-before-define
export type PaginationLoaderFunction<E> = () => Promise<IPaginationLoader<E>>
// eslint-disable-next-line no-use-before-define
export type PaginationPageLoaderFunction<E> = (page: number) => Promise<IPaginationLoader<E>>

export interface IPaginationLoader<E> {
  elements: E[]
  totalCount: number,
  page: number,
  funToLoadNext: null | PaginationLoaderFunction<E>,
  funToLoadPage: null | PaginationPageLoaderFunction<E>
}
