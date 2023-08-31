/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Tobias Kuhnert (UFZ, tobias.kuhnert@ufz.de)
 * - Erik Pongratz (UFZ, erik.pongratz@ufz.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences
 *   (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 *   (UFZ, https://www.ufz.de)
 *
 * Parts of this program were developed within the context of the
 * following publicly funded projects or measures:
 * - Helmholtz Earth and Environment DataHub
 *   (https://www.helmholtz.de/en/research/earth_and_environment/initiatives/#h51095)
 *
 * Licensed under the HEESIL, Version 1.0 or - as soon they will be
 * approved by the "Community" - subsequent versions of the HEESIL
 * (the "Licence").
 *
 * You may not use this work except in compliance with the Licence.
 *
 * You may obtain a copy of the Licence at:
 * https://gitext.gfz-potsdam.de/software/heesil
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the Licence is distributed on an "AS IS" basis,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the Licence for the specific language governing
 * permissions and limitations under the Licence.
 */

import { StationaryLocation } from '@/models/Location'
import { StaticLocationAction } from '@/models/StaticLocationAction'
import { ILocationTimepoint } from '@/serializers/controller/LocationActionTimepointSerializer'
import { LocationTypes } from '@/store/configurations'

export function setCoordinatesInStaticLocationBeginActionFromStationaryLocation (beginAction: StaticLocationAction, location: StationaryLocation) {
  // TODO coordinate transformation in case it is not wgs84 & MSL
  beginAction.x = location.longitude
  beginAction.y = location.latitude
  if (location.elevation !== null) {
    beginAction.z = location.elevation
  }
}

export function extractStationaryLocationFromStaticLocationBeginAction (beginAction: StaticLocationAction): StationaryLocation {
  // TODO coordinate transformation in case it is not wgs84 & MSL
  return StationaryLocation.createFromObject({
    latitude: beginAction.y,
    longitude: beginAction.x,
    elevation: beginAction.z
  })
}

export function isTimePointForStaticAction (locationTimepoint: ILocationTimepoint) {
  return locationTimepoint.type === LocationTypes.staticStart || locationTimepoint.type === LocationTypes.staticEnd
}
export function isTimePointForDynamicAction (locationTimepoint: ILocationTimepoint) {
  return locationTimepoint.type === LocationTypes.dynamicStart || locationTimepoint.type === LocationTypes.dynamicEnd
}

export function getEndLocationTimepointForBeginning (beginLocationTimepoint: ILocationTimepoint, locationTimepoints: ILocationTimepoint []): ILocationTimepoint | null {
  let correspondingEndAction = null

  if (beginLocationTimepoint.type === LocationTypes.staticStart) {
    correspondingEndAction = locationTimepoints.find((element: ILocationTimepoint) => {
      return element.id === beginLocationTimepoint.id && element.type === LocationTypes.staticEnd
    })
  }
  if (beginLocationTimepoint.type === LocationTypes.dynamicStart) {
    correspondingEndAction = locationTimepoints.find((element: ILocationTimepoint) => {
      return element.id === beginLocationTimepoint.id && element.type === LocationTypes.dynamicEnd
    })
  }
  return correspondingEndAction ?? null
}

export function getActiveActionOrNull (locationTimepoints: ILocationTimepoint[]) {
  return locationTimepoints.find((element: ILocationTimepoint) => {
    if (element.type === LocationTypes.staticEnd || element.type === LocationTypes.dynamicEnd) {
      return false
    }
    const correspondingEndAction = getEndLocationTimepointForBeginning(element, locationTimepoints)
    const hasNoEndAction = correspondingEndAction == null

    return (element.type === LocationTypes.staticStart || element.type === LocationTypes.dynamicStart) && hasNoEndAction
  }) ?? null
}