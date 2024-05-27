/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tobias Kuhnert <tobias.kuhnert@ufz.de>
 * - Erik Pongratz <erik.pongratz@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ (UFZ, https://www.ufz.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
