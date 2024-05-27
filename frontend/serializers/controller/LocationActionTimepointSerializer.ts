/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'
import { LocationTypes } from '@/store/configurations'
import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'

export interface IControllerTimepoint {
  timepoint: string,
  type: string,
  id: string,
  label: string | null
}
export interface ILocationTimepoint {
  timepoint: DateTime,
  type: string,
  id: string,
  text: string
}

export class LocationActionTimepointSerializer {
  convertJsonApiObjectListToModelList (jsonControllerObjectList: IControllerTimepoint[]): ILocationTimepoint[] {
    const result = []
    for (const entry of jsonControllerObjectList) {
      const locationAcionTimepoint = this.convertJsonApiDataToModel(entry)
      result.push(locationAcionTimepoint)
    }
    result.sort((a, b) => {
      if (a.timepoint && b.timepoint) {
        return b.timepoint.toUnixInteger() - a.timepoint.toUnixInteger()
      } else {
        return 0
      }
    })
    return result
  }

  convertJsonApiDataToModel (jsonControllerObject: IControllerTimepoint): ILocationTimepoint {
    const tmpTimepoint = DateTime.fromISO(jsonControllerObject.timepoint, { zone: 'UTC' })
    const text = this.generateText(jsonControllerObject, tmpTimepoint)

    return {
      timepoint: tmpTimepoint,
      type: jsonControllerObject.type,
      id: jsonControllerObject.id,
      text
    }
  }

  private generateText (jsonControllerObject: IControllerTimepoint, tmpTimepoint: DateTime) {
    let typeText = ''

    switch (jsonControllerObject.type) {
      case LocationTypes.staticStart:
        typeText = 'Static location begin'
        break
      case LocationTypes.staticEnd:
        typeText = 'Static location end'
        break
      case LocationTypes.dynamicStart:
        typeText = 'Dynamic location begin'
        break
      case LocationTypes.dynamicEnd:
        typeText = 'Dynamic location end'
        break
    }

    if (jsonControllerObject.label) {
      typeText = typeText + ' - ' + jsonControllerObject.label
    }

    return dateToDateTimeStringHHMM(tmpTimepoint) + ' - ' + typeText
  }
}
