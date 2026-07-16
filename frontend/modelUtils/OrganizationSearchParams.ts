/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2026
 * - Nils Brinckmann <nils.brinckmann@gfz.de>
 * - GFZ Helmholtz for Geosciences (GFZ, https://www.gfz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */

import { QueryParams } from '@/modelUtils/QueryParams'

export interface IOrganizationSearchParams {
  searchText: string | null
}

export class OrganizationSearchParamsSerializer {
  toQueryParams (params: IOrganizationSearchParams): QueryParams {
    const result: QueryParams = {}
    if (params.searchText) {
      result.searchText = params.searchText
    }
    return result
  }

  toSearchParams (params: QueryParams): IOrganizationSearchParams {
    return {
      searchText: typeof params.searchText === 'string' ? params.searchText : ''
    }
  }
}
