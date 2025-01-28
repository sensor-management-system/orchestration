/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2024
 * - Maximilian Schaldach <maximilian.schaldach@ufz.de>
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { StaApiEntity, StaEntity } from '@/models/sta/StaEntity'

export class StaEntitySerializer {
  convertStaApiObjectListToModelList (staObjectList: StaApiEntity[]): StaEntity[] {
    return staObjectList.map((jsonApiEntity) => {
      return this.convertStaApiObjectToModel(jsonApiEntity)
    })
  }

  convertStaApiObjectToModel (staApiData: StaApiEntity): StaEntity {
    const staEntity = new StaEntity()

    staEntity.id = staApiData['@iot.id']?.toString() || ''
    staEntity.name = staApiData.name || ''
    staEntity.properties = staApiData.properties || {}
    staEntity.selfLink = staApiData['@iot.selfLink'] || ''

    return staEntity
  }
}
