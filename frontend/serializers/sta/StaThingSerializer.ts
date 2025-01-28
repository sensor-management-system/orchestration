/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { StaApiThing, StaThing } from '@/models/sta/StaThing'
import { StaEntitySerializer } from '@/serializers/sta/StaEntitySerializer'

export class StaThingSerializer extends StaEntitySerializer {
  convertStaApiObjectListToModelList (staObjectList: StaApiThing[]): StaThing[] {
    return super.convertStaApiObjectListToModelList(staObjectList)
  }

  convertStaApiObjectToModel (staApiData: StaApiThing): StaThing {
    return super.convertStaApiObjectToModel(staApiData)
  }
}
