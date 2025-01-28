/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { StaApiEntity } from '@/models/sta/StaEntity'
import { StaApiThing } from '@/models/sta/StaThing'
import { StaApiDatastream } from '@/models/sta/StaDatastream'
import { removeTrailingSlash } from '@/utils/urlHelpers'

/**
 * Type including all (nested) keys of a given StaApiEntity
 */
export type StaApiEntityPropertyNames<T> = T extends object
  ? { [K in keyof T & string]:
        K | (T[K] extends object ? `${K}/${StaApiEntityPropertyNames<T[K]>}` : never)
    }[keyof T & string]
  : never;

/**
 * Valid query parameters for STA
 */
export type StaQueryParams<T extends StaApiEntity> = {
  filter?: string;
  top?: number|string;
  skip?: number|string;
  select?: StaApiEntityPropertyNames<T>[];
  orderby?: string;
  expand?: string[];
  count?: boolean;
}

// alias types for STA entities
export type StaThingQueryParams = StaQueryParams<StaApiThing>
export type StaDatastreamQueryParams = StaQueryParams<StaApiDatastream>

/**
 * Transforms a query parameter object into a properly formatted STA query string.
 * @param {StaQueryParams<StaApiEntity>} paramsObj - The query parameters object to be converted.
 * @returns {string} A correctly formatted query string.
 */
export function getStaQueryStringByQueryParams (paramsObj: StaQueryParams<StaApiEntity>): string {
  const params: { [key: string]: string } = {}

  if (paramsObj.filter) {
    params.$filter = paramsObj.filter
  }
  if (paramsObj.top) {
    params.$top = paramsObj.top.toString()
  }
  if (paramsObj.skip) {
    params.$skip = paramsObj.skip.toString()
  }
  if (paramsObj.select) {
    params.$select = paramsObj.select.join(',')
  }
  if (paramsObj.orderby) {
    params.$orderby = paramsObj.orderby
  }
  if (paramsObj.expand) {
    params.$expand = paramsObj.expand.join(',')
  }
  if (paramsObj.count !== undefined) {
    params.$count = paramsObj.count.toString()
  }

  const queryString = Object.entries(params)
    .map(([key, value]) => `${key}=${value}`)
    .join('&')

  return queryString ? `?${queryString}` : ''
}

type StaQueryParamsCollection = {
  findThingStaLinkByConfigurationId: (configurationId: string) => StaThingQueryParams;
  findDatastreamStaLinkByTsmLinkingId: (linkingId: string) => StaDatastreamQueryParams;
};

export const STA_QUERY_PARAMS_COLLECTION: StaQueryParamsCollection = {
  findThingStaLinkByConfigurationId (configurationId: string): StaThingQueryParams {
    const smsEndpoint = removeTrailingSlash(process.env.smsFrontendUrl ?? '')
    return {
      filter: `properties/jsonld.id eq '${smsEndpoint}/configurations/${configurationId}'`,
      select: ['@iot.selfLink']
    }
  },

  findDatastreamStaLinkByTsmLinkingId (linkingId: string): StaDatastreamQueryParams {
    const smsEndpoint = removeTrailingSlash(process.env.smsFrontendUrl ?? '')
    return {
      filter: `properties/jsonld.id eq '${smsEndpoint}/datastream-links/${linkingId}'`,
      select: ['@iot.selfLink']
    }
  }
}
