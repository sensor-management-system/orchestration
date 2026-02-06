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
import { TsmdlThing } from '@/models/TsmdlThing'

interface TsmdlApiResponse {
  '@iot.id': string,
  name: string,
  description: string,
  properties: Object
}

export class TsmdlThingSerializer extends TsmdlEntitySerializer {
  convertJsonApiObjectListToModelList (jsonApiObjectList: TsmdlApiResponse[]): TsmdlThing[] {
    return super.convertJsonApiObjectListToModelList(jsonApiObjectList) as TsmdlThing[]
  }

  convertJsonApiEntityToModel (jsonApiData: TsmdlApiResponse): TsmdlThing {
    const thing = super.convertJsonApiEntityToModel(jsonApiData) as TsmdlThing
    return thing
  }
}
