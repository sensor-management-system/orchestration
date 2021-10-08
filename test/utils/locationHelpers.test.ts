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

import {
  extractStationaryLocationFromStaticLocationBeginAction,
  getCurrentlyActiveLocationAction,
  getEndActionForActiveLocation,
  getLatestActiveActionEndDate,
  getNextActiveLocationBeginDate,
  setCoordinatesInStaticLocationBeginActionFromStationaryLocation
} from '@/utils/locationHelper'

describe('setCoordinatesInStaticLocationBeginActionFromStationaryLocation', () => {
  it('should just set the x, y and z coordinates for wgs 84 and MSL', () => {
    const stationayLocation = StationaryLocation.createFromObject({
      latitude: 52,
      longitude: 12,
      elevation: 100
    })
    const staticLocationBeginAction = new StaticLocationBeginAction()

    expect(staticLocationBeginAction.x).toBeNull()
    expect(staticLocationBeginAction.y).toBeNull()
    expect(staticLocationBeginAction.z).toBeNull()

    expect(staticLocationBeginAction.epsgCode).toEqual('4326')
    expect(staticLocationBeginAction.elevationDatumName).toEqual('MSL')

    setCoordinatesInStaticLocationBeginActionFromStationaryLocation(staticLocationBeginAction, stationayLocation)

    expect(staticLocationBeginAction.x).toEqual(12)
    expect(staticLocationBeginAction.y).toEqual(52)
    expect(staticLocationBeginAction.z).toEqual(100)

    expect(staticLocationBeginAction.epsgCode).toEqual('4326')
    expect(staticLocationBeginAction.elevationDatumName).toEqual('MSL')
  })
  it('should just set the x, y coordinates for wgs 84 and MSL if elevation is null', () => {
    const stationayLocation = StationaryLocation.createFromObject({
      latitude: 52,
      longitude: 12,
      elevation: null
    })
    const staticLocationBeginAction = new StaticLocationBeginAction()
    staticLocationBeginAction.z = 200

    expect(staticLocationBeginAction.x).toBeNull()
    expect(staticLocationBeginAction.y).toBeNull()

    expect(staticLocationBeginAction.epsgCode).toEqual('4326')
    expect(staticLocationBeginAction.elevationDatumName).toEqual('MSL')

    setCoordinatesInStaticLocationBeginActionFromStationaryLocation(staticLocationBeginAction, stationayLocation)

    expect(staticLocationBeginAction.x).toEqual(12)
    expect(staticLocationBeginAction.y).toEqual(52)
    expect(staticLocationBeginAction.z).toEqual(200)

    expect(staticLocationBeginAction.epsgCode).toEqual('4326')
    expect(staticLocationBeginAction.elevationDatumName).toEqual('MSL')
  })
})
describe('extractStationaryLocationFromStaticLocationBeginAction', () => {
  it('should extract the coordinates for wgs 84 and MSL', () => {
    const staticLocationBeginAction = new StaticLocationBeginAction()

    staticLocationBeginAction.x = 15
    staticLocationBeginAction.y = 53
    staticLocationBeginAction.z = 75

    expect(staticLocationBeginAction.epsgCode).toEqual('4326')
    expect(staticLocationBeginAction.elevationDatumName).toEqual('MSL')

    const stationayLocation = extractStationaryLocationFromStaticLocationBeginAction(staticLocationBeginAction)

    expect(stationayLocation.longitude).toEqual(15)
    expect(stationayLocation.latitude).toEqual(53)
    expect(stationayLocation.elevation).toEqual(75)
  })
  it('should should also work with null values for xyz for wgs 84 and MSL', () => {
    const staticLocationBeginAction = new StaticLocationBeginAction()

    expect(staticLocationBeginAction.x).toBeNull()
    expect(staticLocationBeginAction.y).toBeNull()
    expect(staticLocationBeginAction.z).toBeNull()
    expect(staticLocationBeginAction.epsgCode).toEqual('4326')
    expect(staticLocationBeginAction.elevationDatumName).toEqual('MSL')

    const stationayLocation = extractStationaryLocationFromStaticLocationBeginAction(staticLocationBeginAction)

    expect(stationayLocation.longitude).toBeNull()
    expect(stationayLocation.latitude).toBeNull()
    expect(stationayLocation.elevation).toBeNull()
  })
})
describe('getCurrentlyActiveLocationAction', () => {
  it('should return null if there are no actions', () => {
    const configuration = new Configuration()

    expect(configuration.staticLocationBeginActions).toEqual([])
    expect(configuration.staticLocationEndActions).toEqual([])
    expect(configuration.dynamicLocationBeginActions).toEqual([])
    expect(configuration.dynamicLocationEndActions).toEqual([])

    const checkDate = DateTime.utc(2020, 1, 1, 12, 0, 0)

    const activeAction = getCurrentlyActiveLocationAction(configuration, checkDate)

    expect(activeAction).toBeNull()
  })
  it('should return null if the checkdate is before the start action', () => {
    const configuration = new Configuration()

    const staticLocationBeginAction = new StaticLocationBeginAction()
    staticLocationBeginAction.beginDate = DateTime.utc(2021, 1, 1, 12, 0, 0)

    configuration.staticLocationBeginActions = [staticLocationBeginAction]

    const checkDate = DateTime.utc(2020, 1, 1, 12, 0, 0)

    const activeAction = getCurrentlyActiveLocationAction(configuration, checkDate)

    expect(activeAction).toBeNull()
  })
  it('should return the start action if the checkdate is after the start action', () => {
    const configuration = new Configuration()

    const staticLocationBeginAction = new StaticLocationBeginAction()
    staticLocationBeginAction.beginDate = DateTime.utc(2021, 1, 1, 12, 0, 0)

    configuration.staticLocationBeginActions = [staticLocationBeginAction]

    const checkDate = DateTime.utc(2022, 1, 1, 12, 0, 0)

    const activeAction = getCurrentlyActiveLocationAction(configuration, checkDate)

    expect(activeAction).toEqual(staticLocationBeginAction)
  })
  it('should return the start action if the checkdate is after the start action and before an end action', () => {
    const configuration = new Configuration()

    const staticLocationBeginAction = new StaticLocationBeginAction()
    staticLocationBeginAction.beginDate = DateTime.utc(2021, 1, 1, 12, 0, 0)

    const staticLocationEndAction = new StaticLocationEndAction()
    staticLocationEndAction.endDate = DateTime.utc(2023, 1, 1, 12, 0, 0)

    configuration.staticLocationBeginActions = [staticLocationBeginAction]
    configuration.staticLocationEndActions = [staticLocationEndAction]

    const checkDate = DateTime.utc(2022, 1, 1, 12, 0, 0)

    const activeAction = getCurrentlyActiveLocationAction(configuration, checkDate)

    expect(activeAction).toEqual(staticLocationBeginAction)
  })
  it('should return null if the checkdate is after the end action', () => {
    const configuration = new Configuration()

    const staticLocationBeginAction = new StaticLocationBeginAction()
    staticLocationBeginAction.beginDate = DateTime.utc(2021, 1, 1, 12, 0, 0)

    const staticLocationEndAction = new StaticLocationEndAction()
    staticLocationEndAction.endDate = DateTime.utc(2023, 1, 1, 12, 0, 0)

    configuration.staticLocationBeginActions = [staticLocationBeginAction]
    configuration.staticLocationEndActions = [staticLocationEndAction]

    const checkDate = DateTime.utc(2024, 1, 1, 12, 0, 0)

    const activeAction = getCurrentlyActiveLocationAction(configuration, checkDate)

    expect(activeAction).toBeNull()
  })
  it('should return null if the checkdate is before the start action - also for dynamic actions', () => {
    const configuration = new Configuration()

    const dynamicLocationBeginAction = new DynamicLocationBeginAction()
    dynamicLocationBeginAction.beginDate = DateTime.utc(2021, 1, 1, 12, 0, 0)

    configuration.dynamicLocationBeginActions = [dynamicLocationBeginAction]

    const checkDate = DateTime.utc(2020, 1, 1, 12, 0, 0)

    const activeAction = getCurrentlyActiveLocationAction(configuration, checkDate)

    expect(activeAction).toBeNull()
  })
  it('should return the start action if the checkdate is after the start action - also for dynamic actions', () => {
    const configuration = new Configuration()

    const dynamicLocationBeginAction = new DynamicLocationBeginAction()
    dynamicLocationBeginAction.beginDate = DateTime.utc(2021, 1, 1, 12, 0, 0)

    configuration.dynamicLocationBeginActions = [dynamicLocationBeginAction]

    const checkDate = DateTime.utc(2022, 1, 1, 12, 0, 0)

    const activeAction = getCurrentlyActiveLocationAction(configuration, checkDate)

    expect(activeAction).toEqual(dynamicLocationBeginAction)
  })
  it('should return the start action if the checkdate is after the start action and before an end action - also for dynamic actions', () => {
    const configuration = new Configuration()

    const dynamicLocationBeginAction = new DynamicLocationBeginAction()
    dynamicLocationBeginAction.beginDate = DateTime.utc(2021, 1, 1, 12, 0, 0)

    const dynamicLocationEndAction = new DynamicLocationEndAction()
    dynamicLocationEndAction.endDate = DateTime.utc(2023, 1, 1, 12, 0, 0)

    configuration.dynamicLocationBeginActions = [dynamicLocationBeginAction]
    configuration.dynamicLocationEndActions = [dynamicLocationEndAction]

    const checkDate = DateTime.utc(2022, 1, 1, 12, 0, 0)

    const activeAction = getCurrentlyActiveLocationAction(configuration, checkDate)

    expect(activeAction).toEqual(dynamicLocationBeginAction)
  })
  it('should return null if the checkdate is after the end action - also for dynamic actions', () => {
    const configuration = new Configuration()

    const dynamicLocationBeginAction = new DynamicLocationBeginAction()
    dynamicLocationBeginAction.beginDate = DateTime.utc(2021, 1, 1, 12, 0, 0)

    const dynamicLocationEndAction = new DynamicLocationEndAction()
    dynamicLocationEndAction.endDate = DateTime.utc(2023, 1, 1, 12, 0, 0)

    configuration.dynamicLocationBeginActions = [dynamicLocationBeginAction]
    configuration.dynamicLocationEndActions = [dynamicLocationEndAction]

    const checkDate = DateTime.utc(2024, 1, 1, 12, 0, 0)

    const activeAction = getCurrentlyActiveLocationAction(configuration, checkDate)

    expect(activeAction).toBeNull()
  })
  it('also works for mixed cases', () => {
    const configuration = new Configuration()

    const dynamicLocationBeginAction1 = new DynamicLocationBeginAction()
    dynamicLocationBeginAction1.beginDate = DateTime.utc(2021, 2, 1, 12, 0, 0)

    const dynamicLocationEndAction1 = new DynamicLocationEndAction()
    dynamicLocationEndAction1.endDate = DateTime.utc(2021, 3, 1, 12, 0, 0)

    const staticLocationBeginAction1 = new StaticLocationBeginAction()
    staticLocationBeginAction1.beginDate = DateTime.utc(2021, 4, 1, 12, 0, 0)

    const staticLocationEndAction1 = new StaticLocationEndAction()
    staticLocationEndAction1.endDate = DateTime.utc(2021, 5, 1, 12, 0, 0)

    const dynamicLocationBeginAction2 = new DynamicLocationBeginAction()
    dynamicLocationBeginAction2.beginDate = DateTime.utc(2021, 6, 1, 12, 0, 0)

    const dynamicLocationEndAction2 = new DynamicLocationEndAction()
    dynamicLocationEndAction2.endDate = DateTime.utc(2021, 7, 1, 12, 0, 0)

    const staticLocationBeginAction2 = new StaticLocationBeginAction()
    staticLocationBeginAction2.beginDate = DateTime.utc(2021, 8, 1, 12, 0, 0)

    const staticLocationEndAction2 = new StaticLocationEndAction()
    staticLocationEndAction2.endDate = DateTime.utc(2021, 9, 1, 12, 0, 0)

    configuration.staticLocationBeginActions = [staticLocationBeginAction1, staticLocationBeginAction2]
    configuration.staticLocationEndActions = [staticLocationEndAction1, staticLocationEndAction2]
    configuration.dynamicLocationBeginActions = [dynamicLocationBeginAction1, dynamicLocationBeginAction2]
    configuration.dynamicLocationEndActions = [dynamicLocationEndAction1, dynamicLocationEndAction2]

    expect(getCurrentlyActiveLocationAction(configuration, DateTime.utc(2021, 1, 2, 12, 0, 0))).toBeNull()
    expect(getCurrentlyActiveLocationAction(configuration, DateTime.utc(2021, 2, 2, 12, 0, 0))).toEqual(dynamicLocationBeginAction1)
    expect(getCurrentlyActiveLocationAction(configuration, DateTime.utc(2021, 3, 2, 12, 0, 0))).toBeNull()
    expect(getCurrentlyActiveLocationAction(configuration, DateTime.utc(2021, 4, 2, 12, 0, 0))).toEqual(staticLocationBeginAction1)
    expect(getCurrentlyActiveLocationAction(configuration, DateTime.utc(2021, 5, 2, 12, 0, 0))).toBeNull()
    expect(getCurrentlyActiveLocationAction(configuration, DateTime.utc(2021, 6, 2, 12, 0, 0))).toEqual(dynamicLocationBeginAction2)
    expect(getCurrentlyActiveLocationAction(configuration, DateTime.utc(2021, 7, 2, 12, 0, 0))).toBeNull()
    expect(getCurrentlyActiveLocationAction(configuration, DateTime.utc(2021, 8, 2, 12, 0, 0))).toEqual(staticLocationBeginAction2)
    expect(getCurrentlyActiveLocationAction(configuration, DateTime.utc(2021, 9, 2, 12, 0, 0))).toBeNull()
  })
  it('returns the active location of the checkdate is exactly the one for the stop action', () => {
    const configuration = new Configuration()

    const staticLocationBeginAction = new StaticLocationBeginAction()
    staticLocationBeginAction.beginDate = DateTime.utc(2021, 1, 1, 12, 0, 0)

    const staticLocationEndAction = new StaticLocationEndAction()
    staticLocationEndAction.endDate = DateTime.utc(2023, 1, 1, 12, 0, 0)

    configuration.staticLocationBeginActions = [staticLocationBeginAction]
    configuration.staticLocationEndActions = [staticLocationEndAction]

    const checkDate = DateTime.utc(2023, 1, 1, 12, 0, 0)

    const activeAction = getCurrentlyActiveLocationAction(configuration, checkDate)
    expect(activeAction).toEqual(staticLocationBeginAction)
  })
  it('returns the active location of the checkdate is exactly the one for the stop action - also for dynamic actions', () => {
    const configuration = new Configuration()

    const dynamicLocationBeginAction = new DynamicLocationBeginAction()
    dynamicLocationBeginAction.beginDate = DateTime.utc(2021, 1, 1, 12, 0, 0)

    const dynamicLocationEndAction = new DynamicLocationEndAction()
    dynamicLocationEndAction.endDate = DateTime.utc(2023, 1, 1, 12, 0, 0)

    configuration.dynamicLocationBeginActions = [dynamicLocationBeginAction]
    configuration.dynamicLocationEndActions = [dynamicLocationEndAction]

    const checkDate = DateTime.utc(2023, 1, 1, 12, 0, 0)

    const activeAction = getCurrentlyActiveLocationAction(configuration, checkDate)
    expect(activeAction).toEqual(dynamicLocationBeginAction)
  })
  it('should not care about actions that don\'t have a date', () => {
    const configuration = new Configuration()

    const dynamicLocationBeginAction1 = new DynamicLocationBeginAction()
    expect(dynamicLocationBeginAction1.beginDate).toBeNull()
    const dynamicLocationEndAction1 = new DynamicLocationEndAction()
    expect(dynamicLocationEndAction1.endDate).toBeNull()

    const staticLocationBeginAction1 = new StaticLocationBeginAction()
    expect(staticLocationBeginAction1.beginDate).toBeNull()

    const staticLocationEndAction1 = new StaticLocationEndAction()
    expect(staticLocationEndAction1.endDate).toBeNull()

    const dynamicLocationBeginAction2 = new DynamicLocationBeginAction()
    expect(dynamicLocationBeginAction2.beginDate).toBeNull()

    const dynamicLocationEndAction2 = new DynamicLocationEndAction()
    expect(dynamicLocationEndAction2.endDate).toBeNull()

    const staticLocationBeginAction2 = new StaticLocationBeginAction()
    expect(staticLocationBeginAction2.beginDate).toBeNull()

    const staticLocationEndAction2 = new StaticLocationEndAction()
    expect(staticLocationEndAction2.endDate).toBeNull()

    configuration.staticLocationBeginActions = [staticLocationBeginAction1, staticLocationBeginAction2]
    configuration.staticLocationEndActions = [staticLocationEndAction1, staticLocationEndAction2]
    configuration.dynamicLocationBeginActions = [dynamicLocationBeginAction1, dynamicLocationBeginAction2]
    configuration.dynamicLocationEndActions = [dynamicLocationEndAction1, dynamicLocationEndAction2]

    expect(getCurrentlyActiveLocationAction(configuration, DateTime.utc(2021, 1, 2, 12, 0, 0))).toBeNull()
  })
  it('should also work if there are two actions that are not stopped (mixed case)', () => {
    const configuration = new Configuration()

    const dynamicLocationBeginAction1 = new DynamicLocationBeginAction()
    dynamicLocationBeginAction1.beginDate = DateTime.utc(2021, 2, 1, 12, 0, 0)

    const staticLocationBeginAction1 = new StaticLocationBeginAction()
    staticLocationBeginAction1.beginDate = DateTime.utc(2021, 4, 1, 12, 0, 0)

    const dynamicLocationBeginAction2 = new DynamicLocationBeginAction()
    dynamicLocationBeginAction2.beginDate = DateTime.utc(2021, 6, 1, 12, 0, 0)

    const staticLocationBeginAction2 = new StaticLocationBeginAction()
    staticLocationBeginAction2.beginDate = DateTime.utc(2021, 8, 1, 12, 0, 0)

    configuration.staticLocationBeginActions = [staticLocationBeginAction1, staticLocationBeginAction2]
    configuration.staticLocationEndActions = []
    configuration.dynamicLocationBeginActions = [dynamicLocationBeginAction1, dynamicLocationBeginAction2]
    configuration.dynamicLocationEndActions = []

    expect(getCurrentlyActiveLocationAction(configuration, staticLocationBeginAction1.beginDate)).toEqual(staticLocationBeginAction1)
    expect(getCurrentlyActiveLocationAction(configuration, dynamicLocationBeginAction2.beginDate)).toEqual(dynamicLocationBeginAction2)
  })
})
describe('getEndActionForActiveLocation', () => {
  it('should return null if there are no locations', () => {
    const configuration = new Configuration()
    const activeLocation = null

    const endAction = getEndActionForActiveLocation(configuration, activeLocation)

    expect(endAction).toBeNull()
  })
  it('also returns null if there is an active location given, but none in the configuraiton itself', () => {
    const configuration = new Configuration()
    const activeLocation = new StaticLocationBeginAction()
    activeLocation.beginDate = DateTime.utc(2021, 2, 1, 12, 0, 0)

    const endAction = getEndActionForActiveLocation(configuration, activeLocation)

    expect(endAction).toBeNull()
  })
  it('also returns null if there are location but no active one to search the end for', () => {
    const configuration = new Configuration()

    const dynamicLocationBeginAction1 = new DynamicLocationBeginAction()
    dynamicLocationBeginAction1.beginDate = DateTime.utc(2021, 2, 1, 12, 0, 0)

    const dynamicLocationEndAction1 = new DynamicLocationEndAction()
    dynamicLocationEndAction1.endDate = DateTime.utc(2021, 3, 1, 12, 0, 0)

    const staticLocationBeginAction1 = new StaticLocationBeginAction()
    staticLocationBeginAction1.beginDate = DateTime.utc(2021, 4, 1, 12, 0, 0)

    const staticLocationEndAction1 = new StaticLocationEndAction()
    staticLocationEndAction1.endDate = DateTime.utc(2021, 5, 1, 12, 0, 0)

    const dynamicLocationBeginAction2 = new DynamicLocationBeginAction()
    dynamicLocationBeginAction2.beginDate = DateTime.utc(2021, 6, 1, 12, 0, 0)

    const dynamicLocationEndAction2 = new DynamicLocationEndAction()
    dynamicLocationEndAction2.endDate = DateTime.utc(2021, 7, 1, 12, 0, 0)

    const staticLocationBeginAction2 = new StaticLocationBeginAction()
    staticLocationBeginAction2.beginDate = DateTime.utc(2021, 8, 1, 12, 0, 0)

    const staticLocationEndAction2 = new StaticLocationEndAction()
    staticLocationEndAction2.endDate = DateTime.utc(2021, 9, 1, 12, 0, 0)

    configuration.staticLocationBeginActions = [staticLocationBeginAction1, staticLocationBeginAction2]
    configuration.staticLocationEndActions = [staticLocationEndAction1, staticLocationEndAction2]
    configuration.dynamicLocationBeginActions = [dynamicLocationBeginAction1, dynamicLocationBeginAction2]
    configuration.dynamicLocationEndActions = [dynamicLocationEndAction1, dynamicLocationEndAction2]

    const activeLocation = null

    const endAction = getEndActionForActiveLocation(configuration, activeLocation)

    expect(endAction).toBeNull()
  })
  it('should find the according end actions for a setup with balanced begin and end actions', () => {
    const configuration = new Configuration()

    const dynamicLocationBeginAction1 = new DynamicLocationBeginAction()
    dynamicLocationBeginAction1.beginDate = DateTime.utc(2021, 2, 1, 12, 0, 0)

    const dynamicLocationEndAction1 = new DynamicLocationEndAction()
    dynamicLocationEndAction1.endDate = DateTime.utc(2021, 3, 1, 12, 0, 0)

    const staticLocationBeginAction1 = new StaticLocationBeginAction()
    staticLocationBeginAction1.beginDate = DateTime.utc(2021, 4, 1, 12, 0, 0)

    const staticLocationEndAction1 = new StaticLocationEndAction()
    staticLocationEndAction1.endDate = DateTime.utc(2021, 5, 1, 12, 0, 0)

    const dynamicLocationBeginAction2 = new DynamicLocationBeginAction()
    dynamicLocationBeginAction2.beginDate = DateTime.utc(2021, 6, 1, 12, 0, 0)

    const dynamicLocationEndAction2 = new DynamicLocationEndAction()
    dynamicLocationEndAction2.endDate = DateTime.utc(2021, 7, 1, 12, 0, 0)

    const staticLocationBeginAction2 = new StaticLocationBeginAction()
    staticLocationBeginAction2.beginDate = DateTime.utc(2021, 8, 1, 12, 0, 0)

    const staticLocationEndAction2 = new StaticLocationEndAction()
    staticLocationEndAction2.endDate = DateTime.utc(2021, 9, 1, 12, 0, 0)

    configuration.staticLocationBeginActions = [staticLocationBeginAction1, staticLocationBeginAction2]
    configuration.staticLocationEndActions = [staticLocationEndAction1, staticLocationEndAction2]
    configuration.dynamicLocationBeginActions = [dynamicLocationBeginAction1, dynamicLocationBeginAction2]
    configuration.dynamicLocationEndActions = [dynamicLocationEndAction1, dynamicLocationEndAction2]

    expect(getEndActionForActiveLocation(configuration, dynamicLocationBeginAction1)).toEqual(dynamicLocationEndAction1)
    expect(getEndActionForActiveLocation(configuration, dynamicLocationBeginAction2)).toEqual(dynamicLocationEndAction2)
    expect(getEndActionForActiveLocation(configuration, staticLocationBeginAction1)).toEqual(staticLocationEndAction1)
    expect(getEndActionForActiveLocation(configuration, staticLocationBeginAction2)).toEqual(staticLocationEndAction2)
  })
  it('should not give us an end action that was used for another begin (first dynamic, second static)', () => {
    // can happen due to a deleted end action
    const configuration = new Configuration()

    const dynamicLocationBeginAction1 = new DynamicLocationBeginAction()
    dynamicLocationBeginAction1.beginDate = DateTime.utc(2021, 2, 1, 12, 0, 0)

    const staticLocationBeginAction1 = new StaticLocationBeginAction()
    staticLocationBeginAction1.beginDate = DateTime.utc(2021, 4, 1, 12, 0, 0)

    const staticLocationEndAction1 = new StaticLocationEndAction()
    staticLocationEndAction1.endDate = DateTime.utc(2021, 5, 1, 12, 0, 0)

    configuration.staticLocationBeginActions = [staticLocationBeginAction1]
    configuration.staticLocationEndActions = [staticLocationEndAction1]
    configuration.dynamicLocationBeginActions = [dynamicLocationBeginAction1]
    configuration.dynamicLocationEndActions = []

    expect(getEndActionForActiveLocation(configuration, dynamicLocationBeginAction1)).toBeNull()
    expect(getEndActionForActiveLocation(configuration, staticLocationBeginAction1)).toEqual(staticLocationEndAction1)
  })
  it('should not give us an end action that was used for another begin (first static, second dynamic)', () => {
    // can happen due to a deleted end action
    const configuration = new Configuration()

    const staticLocationBeginAction1 = new StaticLocationBeginAction()
    staticLocationBeginAction1.beginDate = DateTime.utc(2021, 4, 1, 12, 0, 0)

    const dynamicLocationBeginAction2 = new DynamicLocationBeginAction()
    dynamicLocationBeginAction2.beginDate = DateTime.utc(2021, 6, 1, 12, 0, 0)

    const dynamicLocationEndAction2 = new DynamicLocationEndAction()
    dynamicLocationEndAction2.endDate = DateTime.utc(2021, 7, 1, 12, 0, 0)

    configuration.staticLocationBeginActions = [staticLocationBeginAction1]
    configuration.staticLocationEndActions = []
    configuration.dynamicLocationBeginActions = [dynamicLocationBeginAction2]
    configuration.dynamicLocationEndActions = [dynamicLocationEndAction2]

    expect(getEndActionForActiveLocation(configuration, staticLocationBeginAction1)).toBeNull()
    expect(getEndActionForActiveLocation(configuration, dynamicLocationBeginAction2)).toEqual(dynamicLocationEndAction2)
  })
  it('should not give us an end action that was used for another begin (both static)', () => {
    // can happen due to a deleted end action
    const configuration = new Configuration()

    const staticLocationBeginAction1 = new StaticLocationBeginAction()
    staticLocationBeginAction1.beginDate = DateTime.utc(2021, 4, 1, 12, 0, 0)

    const staticLocationBeginAction2 = new StaticLocationBeginAction()
    staticLocationBeginAction2.beginDate = DateTime.utc(2021, 6, 1, 12, 0, 0)

    const staticLocationEndAction2 = new StaticLocationEndAction()
    staticLocationEndAction2.endDate = DateTime.utc(2021, 7, 1, 12, 0, 0)

    configuration.staticLocationBeginActions = [staticLocationBeginAction1, staticLocationBeginAction2]
    configuration.staticLocationEndActions = [staticLocationEndAction2]
    configuration.dynamicLocationBeginActions = []
    configuration.dynamicLocationEndActions = []

    expect(getEndActionForActiveLocation(configuration, staticLocationBeginAction1)).toBeNull()
    expect(getEndActionForActiveLocation(configuration, staticLocationBeginAction2)).toEqual(staticLocationEndAction2)
  })
  it('should not give us an end action that was used for another begin (both dynamic)', () => {
    // can happen due to a deleted end action
    const configuration = new Configuration()

    const dynamicLocationBeginAction1 = new DynamicLocationBeginAction()
    dynamicLocationBeginAction1.beginDate = DateTime.utc(2021, 4, 1, 12, 0, 0)

    const dynamicLocationBeginAction2 = new DynamicLocationBeginAction()
    dynamicLocationBeginAction2.beginDate = DateTime.utc(2021, 6, 1, 12, 0, 0)

    const dynamicLocationEndAction2 = new DynamicLocationEndAction()
    dynamicLocationEndAction2.endDate = DateTime.utc(2021, 7, 1, 12, 0, 0)

    configuration.dynamicLocationBeginActions = [dynamicLocationBeginAction1, dynamicLocationBeginAction2]
    configuration.dynamicLocationEndActions = [dynamicLocationEndAction2]
    configuration.staticLocationBeginActions = []
    configuration.staticLocationEndActions = []

    expect(getEndActionForActiveLocation(configuration, dynamicLocationBeginAction1)).toBeNull()
    expect(getEndActionForActiveLocation(configuration, dynamicLocationBeginAction2)).toEqual(dynamicLocationEndAction2)
  })
})
describe('getNextActiveLocationBeginDate', () => {
  it('should just return null if there are no location actions', () => {
    const configuration = new Configuration()

    const nextBeginDate = getNextActiveLocationBeginDate(configuration, DateTime.utc(2021, 7, 1, 12, 0, 0))
    expect(nextBeginDate).toBeNull()
  })
  it('should return the date for the next location begin action', () => {
    const configuration = new Configuration()

    const dynamicLocationBeginAction1 = new DynamicLocationBeginAction()
    dynamicLocationBeginAction1.beginDate = DateTime.utc(2021, 2, 1, 12, 0, 0)

    const dynamicLocationEndAction1 = new DynamicLocationEndAction()
    dynamicLocationEndAction1.endDate = DateTime.utc(2021, 3, 1, 12, 0, 0)

    const staticLocationBeginAction1 = new StaticLocationBeginAction()
    staticLocationBeginAction1.beginDate = DateTime.utc(2021, 4, 1, 12, 0, 0)

    const staticLocationEndAction1 = new StaticLocationEndAction()
    staticLocationEndAction1.endDate = DateTime.utc(2021, 5, 1, 12, 0, 0)

    const dynamicLocationBeginAction2 = new DynamicLocationBeginAction()
    dynamicLocationBeginAction2.beginDate = DateTime.utc(2021, 6, 1, 12, 0, 0)

    const dynamicLocationEndAction2 = new DynamicLocationEndAction()
    dynamicLocationEndAction2.endDate = DateTime.utc(2021, 7, 1, 12, 0, 0)

    const staticLocationBeginAction2 = new StaticLocationBeginAction()
    staticLocationBeginAction2.beginDate = DateTime.utc(2021, 8, 1, 12, 0, 0)

    const staticLocationEndAction2 = new StaticLocationEndAction()
    staticLocationEndAction2.endDate = DateTime.utc(2021, 9, 1, 12, 0, 0)

    configuration.staticLocationBeginActions = [staticLocationBeginAction1, staticLocationBeginAction2]
    configuration.staticLocationEndActions = [staticLocationEndAction1, staticLocationEndAction2]
    configuration.dynamicLocationBeginActions = [dynamicLocationBeginAction1, dynamicLocationBeginAction2]
    configuration.dynamicLocationEndActions = [dynamicLocationEndAction1, dynamicLocationEndAction2]

    expect(getNextActiveLocationBeginDate(configuration, DateTime.utc(2021, 1, 1, 12, 0, 0))).toEqual(dynamicLocationBeginAction1.beginDate)
    // if we use right the date of the start action, then we get the very next start action date
    expect(getNextActiveLocationBeginDate(configuration, dynamicLocationBeginAction1.beginDate)).toEqual(staticLocationBeginAction1.beginDate)
    expect(getNextActiveLocationBeginDate(configuration, dynamicLocationEndAction1.endDate)).toEqual(staticLocationBeginAction1.beginDate)
    expect(getNextActiveLocationBeginDate(configuration, staticLocationBeginAction1.beginDate)).toEqual(dynamicLocationBeginAction2.beginDate)
    expect(getNextActiveLocationBeginDate(configuration, staticLocationEndAction1.endDate)).toEqual(dynamicLocationBeginAction2.beginDate)
    expect(getNextActiveLocationBeginDate(configuration, dynamicLocationBeginAction2.beginDate)).toEqual(staticLocationBeginAction2.beginDate)
    expect(getNextActiveLocationBeginDate(configuration, dynamicLocationEndAction2.endDate)).toEqual(staticLocationBeginAction2.beginDate)

    expect(getNextActiveLocationBeginDate(configuration, staticLocationBeginAction2.beginDate)).toBeNull()
    expect(getNextActiveLocationBeginDate(configuration, staticLocationEndAction2.endDate)).toBeNull()
  })
})

describe('getLatestActiveActionEndDate', () => {
  it('should just return null if there are no location actions', () => {
    const configuration = new Configuration()

    const nextBeginDate = getLatestActiveActionEndDate(configuration, DateTime.utc(2021, 7, 1, 12, 0, 0))
    expect(nextBeginDate).toBeNull()
  })
  it('should return the date for the next location begin action', () => {
    const configuration = new Configuration()

    const dynamicLocationBeginAction1 = new DynamicLocationBeginAction()
    dynamicLocationBeginAction1.beginDate = DateTime.utc(2021, 2, 1, 12, 0, 0)

    const dynamicLocationEndAction1 = new DynamicLocationEndAction()
    dynamicLocationEndAction1.endDate = DateTime.utc(2021, 3, 1, 12, 0, 0)

    const staticLocationBeginAction1 = new StaticLocationBeginAction()
    staticLocationBeginAction1.beginDate = DateTime.utc(2021, 4, 1, 12, 0, 0)

    const staticLocationEndAction1 = new StaticLocationEndAction()
    staticLocationEndAction1.endDate = DateTime.utc(2021, 5, 1, 12, 0, 0)

    const dynamicLocationBeginAction2 = new DynamicLocationBeginAction()
    dynamicLocationBeginAction2.beginDate = DateTime.utc(2021, 6, 1, 12, 0, 0)

    const dynamicLocationEndAction2 = new DynamicLocationEndAction()
    dynamicLocationEndAction2.endDate = DateTime.utc(2021, 7, 1, 12, 0, 0)

    const staticLocationBeginAction2 = new StaticLocationBeginAction()
    staticLocationBeginAction2.beginDate = DateTime.utc(2021, 8, 1, 12, 0, 0)

    const staticLocationEndAction2 = new StaticLocationEndAction()
    staticLocationEndAction2.endDate = DateTime.utc(2021, 9, 1, 12, 0, 0)

    configuration.staticLocationBeginActions = [staticLocationBeginAction1, staticLocationBeginAction2]
    configuration.staticLocationEndActions = [staticLocationEndAction1, staticLocationEndAction2]
    configuration.dynamicLocationBeginActions = [dynamicLocationBeginAction1, dynamicLocationBeginAction2]
    configuration.dynamicLocationEndActions = [dynamicLocationEndAction1, dynamicLocationEndAction2]

    expect(getLatestActiveActionEndDate(configuration, dynamicLocationBeginAction1.beginDate)).toBeNull()
    expect(getLatestActiveActionEndDate(configuration, dynamicLocationEndAction1.endDate)).toBeNull()
    expect(getLatestActiveActionEndDate(configuration, staticLocationBeginAction1.beginDate)).toEqual(dynamicLocationEndAction1.endDate)
    expect(getLatestActiveActionEndDate(configuration, staticLocationEndAction1.endDate)).toEqual(dynamicLocationEndAction1.endDate)
    expect(getLatestActiveActionEndDate(configuration, dynamicLocationBeginAction2.beginDate)).toEqual(staticLocationEndAction1.endDate)
    expect(getLatestActiveActionEndDate(configuration, dynamicLocationEndAction2.endDate)).toEqual(staticLocationEndAction1.endDate)

    expect(getLatestActiveActionEndDate(configuration, staticLocationBeginAction2.beginDate)).toEqual(dynamicLocationEndAction2.endDate)
    expect(getLatestActiveActionEndDate(configuration, staticLocationEndAction2.endDate)).toEqual(dynamicLocationEndAction2.endDate)

    expect(getLatestActiveActionEndDate(configuration, DateTime.utc(2021, 10, 1, 12, 0, 0))).toEqual(staticLocationEndAction2.endDate)
  })
})
