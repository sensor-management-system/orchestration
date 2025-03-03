/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { TsmdlEntitySerializer } from './TsmdlEntitySerializer'
import { TsmdlDatasource } from '@/models/TsmdlDatasource'

interface TsdmlApiResponse {
  '@iot.id': string,
  name: string,
  description: string,
  properties: Object,
  sta_endpoint?: string
}

export class TsmdlDatasourceSerializer extends TsmdlEntitySerializer {
  convertJsonApiObjectListToModelList (jsonApiObjectList: TsdmlApiResponse[]): TsmdlDatasource[] {
    return super.convertJsonApiObjectListToModelList(jsonApiObjectList)
  }

  convertJsonApiEntityToModel (jsonApiData: TsdmlApiResponse): TsmdlDatasource {
    const tsmdlDatasource = new TsmdlDatasource()

    tsmdlDatasource.id = jsonApiData['@iot.id'].toString()
    tsmdlDatasource.name = jsonApiData.name || ''
    tsmdlDatasource.description = jsonApiData.description || ''
    tsmdlDatasource.properties = jsonApiData.properties || {}
    tsmdlDatasource.staLink = jsonApiData.sta_endpoint?.replace(/\/$/, '') ?? ''

    return tsmdlDatasource
  }
}
