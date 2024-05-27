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
import { TsmdlEntity } from '@/models/TsmdlEntity'

interface TsdmlApiResponse {
  '@iot.id': string,
  name: string,
  description: string,
  properties: Object
}

export class TsmdlEntitySerializer {
  convertJsonApiObjectListToModelList (jsonApiObjectList: TsdmlApiResponse[]): TsmdlEntity[] {
    return jsonApiObjectList.map((jsonApiEntity) => {
      return this.convertJsonApiEntityToModel(jsonApiEntity)
    })
  }

  convertJsonApiEntityToModel (jsonApiData: TsdmlApiResponse): TsmdlEntity {
    const tsmdlEntity = new TsmdlEntity()

    tsmdlEntity.id = jsonApiData['@iot.id'].toString()
    tsmdlEntity.name = jsonApiData.name || ''
    tsmdlEntity.description = jsonApiData.description || ''
    tsmdlEntity.properties = jsonApiData.properties || {}

    return tsmdlEntity
  }
}
