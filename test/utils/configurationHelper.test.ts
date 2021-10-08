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
import { StaticLocationBeginAction } from '@/models/StaticLocationBeginAction'
import { StaticLocationEndAction } from '@/models/StaticLocationEndAction'

import { IActionDateWithTextItem } from '@/utils/configurationInterfaces'
import ConfigurationHelper from '@/utils/configurationHelper'

describe('#getActionDatesWithTextByConfiguration', () => {
  it('should return a sorted list of action dates', () => {
    const configuration = new Configuration()

    const staticLocationBeginAction1 = new StaticLocationBeginAction()
    staticLocationBeginAction1.beginDate = DateTime.utc(2021, 1, 1, 12, 0, 0)
    const staticLocationEndAction1 = new StaticLocationEndAction()
    staticLocationEndAction1.endDate = DateTime.utc(2021, 1, 1, 20, 0, 0)

    const staticLocationBeginAction2 = new StaticLocationBeginAction()
    staticLocationBeginAction2.beginDate = DateTime.utc(1999, 8, 1, 10, 0, 0)
    const staticLocationEndAction2 = new StaticLocationEndAction()
    staticLocationEndAction2.endDate = DateTime.utc(1999, 8, 15, 10, 0, 0)

    const dynamicLocationBeginAction1 = new DynamicLocationBeginAction()
    dynamicLocationBeginAction1.beginDate = DateTime.utc(2020, 3, 1, 10, 0, 0)
    const dynamicLocationEndAction1 = new DynamicLocationEndAction()
    dynamicLocationEndAction1.endDate = DateTime.utc(2020, 3, 31, 10, 0, 0)

    configuration.staticLocationBeginActions = [
      staticLocationBeginAction1,
      staticLocationBeginAction2
    ]
    configuration.staticLocationEndActions = [
      staticLocationEndAction1,
      staticLocationEndAction2
    ]
    configuration.dynamicLocationBeginActions = [
      dynamicLocationBeginAction1
    ]
    configuration.dynamicLocationEndActions = [
      dynamicLocationEndAction1
    ]
    const selectedDate = DateTime.utc(2021, 10, 6, 12, 0, 0)
    const actionDates: IActionDateWithTextItem[] = ConfigurationHelper.getActionDatesWithTextsByConfiguration(configuration, selectedDate, { useMounts: false, useLoctions: true })

    expect(actionDates.length).toEqual(8)
    expect(actionDates[0]).toHaveProperty('date', DateTime.utc(1999, 8, 1, 10, 0, 0))
    expect(actionDates[0]).toHaveProperty('text', '1999-08-01 10:00 - Static location begin')
    expect(actionDates[1]).toHaveProperty('date', DateTime.utc(1999, 8, 15, 10, 0, 0))
    expect(actionDates[1]).toHaveProperty('text', '1999-08-15 10:00 - Static location end')
    expect(actionDates[2]).toHaveProperty('date', DateTime.utc(2020, 3, 1, 10, 0, 0))
    expect(actionDates[2]).toHaveProperty('text', '2020-03-01 10:00 - Dynamic location begin')
    expect(actionDates[3]).toHaveProperty('date', DateTime.utc(2020, 3, 31, 10, 0, 0))
    expect(actionDates[3]).toHaveProperty('text', '2020-03-31 10:00 - Dynamic location end')
    expect(actionDates[4]).toHaveProperty('date', DateTime.utc(2021, 1, 1, 12, 0, 0))
    expect(actionDates[4]).toHaveProperty('text', '2021-01-01 12:00 - Static location begin')
    expect(actionDates[5]).toHaveProperty('date', DateTime.utc(2021, 1, 1, 20, 0, 0))
    expect(actionDates[5]).toHaveProperty('text', '2021-01-01 20:00 - Static location end')
    expect(actionDates[6]).toHaveProperty('date', DateTime.utc(2021, 10, 6, 12, 0, 0))
    expect(actionDates[6]).toHaveProperty('text', '2021-10-06 12:00 - Selected')
    // the 7th item is now - which we can't text because of the time
  })
})
