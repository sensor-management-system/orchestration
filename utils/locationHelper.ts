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

import { DateTime } from 'luxon'

import { Configuration } from '@/models/Configuration'
import { DynamicLocationBeginAction } from '@/models/DynamicLocationBeginAction'
import { DynamicLocationEndAction } from '@/models/DynamicLocationEndAction'
import { StationaryLocation } from '@/models/Location'
import { StaticLocationBeginAction } from '@/models/StaticLocationBeginAction'
import { StaticLocationEndAction } from '@/models/StaticLocationEndAction'

export function setCoordinatesInStaticLocationBeginActionFromStationaryLocation (beginAction: StaticLocationBeginAction, location: StationaryLocation) {
  // TODO coordinate transformation in case it is not wgs84 & MSL
  beginAction.x = location.longitude
  beginAction.y = location.latitude
  if (location.elevation !== null) {
    beginAction.z = location.elevation
  }
}

export function extractStationaryLocationFromStaticLocationBeginAction (beginAction: StaticLocationBeginAction): StationaryLocation {
  // TODO coordinate transformation in case it is not wgs84 & MSL
  return StationaryLocation.createFromObject({
    latitude: beginAction.y,
    longitude: beginAction.x,
    elevation: beginAction.z
  })
}

export function getCurrentlyActiveLocationAction (configuration: Configuration, checkDate: DateTime): StaticLocationBeginAction | DynamicLocationBeginAction | null {
  let latestStaticLocationAction: StaticLocationBeginAction | null = null
  for (const staticLocationBeginAction of configuration.staticLocationBeginActions) {
    const actionDate = staticLocationBeginAction.beginDate
    if (actionDate && checkDate >= actionDate) {
      if (latestStaticLocationAction === null) {
        latestStaticLocationAction = staticLocationBeginAction
      } else {
        const latestDate = latestStaticLocationAction.beginDate
        if (!latestDate || latestDate < actionDate) {
          latestStaticLocationAction = staticLocationBeginAction
        }
      }
    }
  }
  for (const staticLocationEndAction of configuration.staticLocationEndActions) {
    const actionDate = staticLocationEndAction.endDate
    // we want to show the information also in case we selected the date for stop
    // so here we need to have a date seleted that is later then the endDate
    if (actionDate && checkDate > actionDate) {
      if (latestStaticLocationAction !== null && latestStaticLocationAction.beginDate && latestStaticLocationAction.beginDate < actionDate) {
        latestStaticLocationAction = null
      }
    }
  }

  let latestDynamicLocationAction: DynamicLocationBeginAction | null = null
  for (const dynamicLocationBeginAction of configuration.dynamicLocationBeginActions) {
    const actionDate = dynamicLocationBeginAction.beginDate
    if (actionDate && checkDate >= actionDate) {
      if (latestDynamicLocationAction === null) {
        latestDynamicLocationAction = dynamicLocationBeginAction
      } else {
        const latestDate = latestDynamicLocationAction.beginDate
        if (!latestDate || latestDate < actionDate) {
          latestDynamicLocationAction = dynamicLocationBeginAction
        }
      }
    }
  }
  for (const dynamicLocationEndAction of configuration.dynamicLocationEndActions) {
    const actionDate = dynamicLocationEndAction.endDate
    // as for the static dates we want to show the location actions
    // in case the selcted date is the endDate
    if (actionDate && checkDate > actionDate) {
      if (latestDynamicLocationAction !== null && latestDynamicLocationAction.beginDate && latestDynamicLocationAction.beginDate < actionDate) {
        latestDynamicLocationAction = null
      }
    }
  }
  // in case on of them is null, we return the other one
  // in case both are null, this is fine as well as
  // we just have no active location action
  if (latestDynamicLocationAction === null) {
    return latestStaticLocationAction
  }
  if (latestStaticLocationAction === null) {
    return latestDynamicLocationAction
  }
  // here we know that both are not null
  const latestDynamicLocationActionDate = latestDynamicLocationAction?.beginDate as DateTime
  const latestStaticLocationActionDate = latestStaticLocationAction?.beginDate as DateTime

  if (latestDynamicLocationActionDate > latestStaticLocationActionDate) {
    return latestDynamicLocationAction
  }
  return latestStaticLocationAction
}

export function getEndActionForActiveLocation (configuration: Configuration, activeLocation: StaticLocationBeginAction | DynamicLocationBeginAction | null): StaticLocationEndAction | DynamicLocationEndAction | null {
  if (activeLocation instanceof StaticLocationBeginAction) {
    let endAction = null
    if (activeLocation.beginDate) {
      for (const action of configuration.staticLocationEndActions) {
        if (action.endDate && action.endDate > activeLocation.beginDate) {
          if (endAction === null || endAction.endDate === null || endAction.endDate > action.endDate) {
            endAction = action
          }
        }
      }
    }
    // if we have one we need to make sure that it is not related to a later begin action
    // (could happen if someone deleted the end action)
    if (endAction) {
      for (const action of configuration.staticLocationBeginActions) {
        if (action.beginDate && activeLocation.beginDate && endAction.endDate && action.beginDate > activeLocation.beginDate && action.beginDate < endAction.endDate) {
          endAction = null
          break
        }
      }
    }
    return endAction
  } else if (activeLocation instanceof DynamicLocationBeginAction) {
    let endAction = null
    if (activeLocation.beginDate) {
      for (const action of configuration.dynamicLocationEndActions) {
        if (action.endDate && action.endDate > activeLocation.beginDate) {
          if (endAction === null || endAction.endDate === null || endAction.endDate > action.endDate) {
            endAction = action
          }
        }
      }
    }
    // also for the dynamic location it could happen that someone deleted the
    // according stop action (and the one we found so far is for the later begin action)
    if (endAction) {
      for (const action of configuration.dynamicLocationBeginActions) {
        if (action.beginDate && activeLocation.beginDate && endAction.endDate && action.beginDate > activeLocation.beginDate && action.beginDate < endAction.endDate) {
          endAction = null
          break
        }
      }
    }
    return endAction
  }
  return null
}

export function getBeginActionForLocationEndAction (configuration: Configuration, locationEndAction: StaticLocationEndAction | DynamicLocationEndAction | null): StaticLocationBeginAction | DynamicLocationBeginAction | null {
  if (locationEndAction === null) {
    return null
  }
  if (locationEndAction instanceof StaticLocationEndAction) {
    let beginAction = null
    if (locationEndAction.endDate) {
      for (const action of configuration.staticLocationBeginActions) {
        if (action.beginDate && action.beginDate < locationEndAction.endDate) {
          if (beginAction === null || (beginAction.beginDate && beginAction.beginDate < action.beginDate)) {
            beginAction = action
          }
        }
      }
    }
    return beginAction
  } else if (locationEndAction instanceof DynamicLocationEndAction) {
    let beginAction = null
    if (locationEndAction.endDate) {
      for (const action of configuration.dynamicLocationBeginActions) {
        if (action.beginDate && action.beginDate < locationEndAction.endDate) {
          if (beginAction === null || (beginAction.beginDate && beginAction.beginDate < action.beginDate)) {
            beginAction = action
          }
        }
      }
    }
    return beginAction
  }
  return null
}

export function getNextActiveLocationBeginDate (configuration: Configuration, checkDate: DateTime): DateTime | null {
  // The nearest begin date AFTER the current one
  let nextBeginDate = null
  for (const action of configuration.staticLocationBeginActions) {
    if (action.beginDate && action.beginDate > checkDate) {
      if (nextBeginDate === null || nextBeginDate > action.beginDate) {
        nextBeginDate = action.beginDate
      }
    }
  }
  for (const action of configuration.dynamicLocationBeginActions) {
    if (action.beginDate && action.beginDate > checkDate) {
      if (nextBeginDate === null || nextBeginDate > action.beginDate) {
        nextBeginDate = action.beginDate
      }
    }
  }
  return nextBeginDate
}

export function getLatestActiveActionEndDate (configuration: Configuration, checkDate: DateTime): DateTime | null {
  // The end date of the latest (freshed) end action BEFORE
  // the current selected date (currently active action can be null
  // if we are going to insert a location action)
  let latestEndDate = null
  for (const action of configuration.staticLocationEndActions) {
    if (action.endDate && action.endDate < checkDate) {
      if (latestEndDate === null || latestEndDate < action.endDate) {
        latestEndDate = action.endDate
      }
    }
  }
  for (const action of configuration.dynamicLocationEndActions) {
    if (action.endDate && action.endDate < checkDate) {
      if (latestEndDate === null || latestEndDate < action.endDate) {
        latestEndDate = action.endDate
      }
    }
  }
  return latestEndDate
}
