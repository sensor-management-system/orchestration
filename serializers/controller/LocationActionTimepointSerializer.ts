/**
 * @license
 * Web client of the Sensor Management System software developed within the
 * Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 *   - Helmholtz Earth and Environment DataHub
 * (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 *   You may obtain a copy of the Licence at:
 *   https://gitext.gfz-potsdam.de/software/heesil
 *
 *     Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 *   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
 */
import { DateTime } from 'luxon'
import { LocationTypes } from '@/store/configurations'
import { dateToDateTimeStringHHMM } from '@/utils/dateHelper'

export interface IControllerTimepoint{
  timepoint: string,
  type: string,
  id: string
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

    return dateToDateTimeStringHHMM(tmpTimepoint) + ' - ' + typeText
  }
}
