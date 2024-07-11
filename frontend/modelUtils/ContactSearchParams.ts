/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { QueryParams } from '@/modelUtils/QueryParams'

export interface IContactSearchParams {
  searchText: string | null
}

/**
 * defines methods to convert from ISearchParameters to QueryParams and vice
 * versa
 */
export class ContactSearchParamsSerializer {
  /**
   * converts search parameters to Vue route query params
   *
   * @param {IContactSearchParams} params - the params used in the search
   * @returns {QueryParams} Vue route query params
   */
  toQueryParams (params: IContactSearchParams): QueryParams {
    const result: QueryParams = {}
    if (params.searchText) {
      result.searchText = params.searchText
    }
    return result
  }

  /**
   * converts Vue route query params to search parameters
   *
   * @param {QueryParams} params - the Vue route query params
   * @returns {IContactSearchParams} the params used in the search
   */
  toSearchParams (params: QueryParams): IContactSearchParams {
    return {
      searchText: typeof params.searchText === 'string' ? params.searchText : ''
    }
  }
}
