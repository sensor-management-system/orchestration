/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { StaEntitySerializer } from '@/serializers/sta/StaEntitySerializer'
import { StaApiDatastream, StaDatastream } from '@/models/sta/StaDatastream'

export class StaDatastreamSerializer extends StaEntitySerializer {
  convertStaApiObjectListToModelList (staObjectList: StaApiDatastream[]): StaDatastream[] {
    return super.convertStaApiObjectListToModelList(staObjectList)
  }

  convertStaApiObjectToModel (staApiData: StaApiDatastream): StaDatastream {
    return super.convertStaApiObjectToModel(staApiData)
  }
}
