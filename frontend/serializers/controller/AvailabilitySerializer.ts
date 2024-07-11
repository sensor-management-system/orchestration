/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { Availability } from '@/models/Availability'

import {
  IJsonApiEntityListEnvelope,
  IJsonApiAttributes
} from '@/serializers/jsonapi/JsonApiTypes'
import { stringToDate } from '@/utils/dateHelper'

export class AvailabilitySerializer {
  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiEntityListEnvelope): Availability[] {
    return jsonApiObjectList.data.map(this.convertJsonApiDataToModel.bind(this))
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiAttributes): Availability {
    const newAvailability = new Availability()
    newAvailability.id = jsonApiData.id
    newAvailability.available = jsonApiData.available
    if (!jsonApiData.available) {
      newAvailability.beginDate = stringToDate(jsonApiData.begin_date)
      newAvailability.endDate = stringToDate(jsonApiData.end_date)
      newAvailability.configurationID = jsonApiData.configuration
      newAvailability.mountID = jsonApiData.mount
    }

    return Availability.createFromObject(newAvailability)
  }
}
