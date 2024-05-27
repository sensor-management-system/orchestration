/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { TsmdlEntitySerializer } from './TsmdlEntitySerializer'
import { TsmdlDatastream } from '@/models/TsmdlDatastream'

interface TsdmlApiResponse {
  '@iot.id': string,
  name: string,
  description: string,
  properties: Object
}

export class TsmdlDatastreamSerializer extends TsmdlEntitySerializer {
  convertJsonApiObjectListToModelList (jsonApiObjectList: TsdmlApiResponse[]): TsmdlDatastream[] {
    return super.convertJsonApiObjectListToModelList(jsonApiObjectList)
  }

  convertJsonApiEntityToModel (jsonApiData: TsdmlApiResponse): TsmdlDatastream {
    return super.convertJsonApiEntityToModel(jsonApiData)
  }
}
