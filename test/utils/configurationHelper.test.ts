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
import { Platform } from '@/models/Platform'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { Contact } from '@/models/Contact'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Device } from '@/models/Device'
import { Visibility } from '@/models/Visibility'

import { buildConfigurationTree } from '@/modelUtils/mountHelpers'
import configurationHelper from '@/utils/configurationHelper'
import { PlatformNode } from '@/viewmodels/PlatformNode'

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
    const actionDates: IActionDateWithTextItem[] = configurationHelper.getActionDatesWithTextsByConfiguration(configuration, selectedDate, { useMounts: false, useLoctions: true })

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
describe('#addNewMountAction', () => {
  it('should add a new platformMountAction to our configuration', () => {
    const platform1 = Platform.createFromObject({
      shortName: 'platform 1',
      id: '111',
      longName: '',
      platformTypeName: '',
      platformTypeUri: '',
      persistentIdentifier: '',
      serialNumber: '',
      inventoryNumber: '',
      website: '',
      manufacturerName: '',
      manufacturerUri: '',
      statusName: '',
      statusUri: '',
      attachments: [],
      contacts: [],
      model: '',
      description: '',
      createdAt: DateTime.utc(2021, 12, 15, 8, 54, 13),
      updatedAt: DateTime.utc(2021, 12, 15, 8, 54, 13),
      createdBy: null,
      updatedBy: null,
      createdByUserId: null,
      permissionGroups: [],
      visibility: Visibility.Internal
    })
    const device1 = Device.createFromObject({
      shortName: 'device 1',
      id: '222',
      longName: '',
      deviceTypeName: '',
      deviceTypeUri: '',
      persistentIdentifier: '',
      serialNumber: '',
      inventoryNumber: '',
      website: '',
      manufacturerName: '',
      manufacturerUri: '',
      statusName: '',
      statusUri: '',
      attachments: [],
      contacts: [],
      model: '',
      createdAt: DateTime.utc(2021, 12, 15, 8, 54, 13),
      updatedAt: DateTime.utc(2021, 12, 15, 8, 54, 13),
      description: '',
      dualUse: false,
      properties: [],
      customFields: [],
      createdBy: null,
      updatedBy: null,
      createdByUserId: null,
      permissionGroups: [],
      visibility: Visibility.Internal
    })
    const contact1 = Contact.createFromObject({
      id: '111111',
      givenName: 'Homer',
      familyName: 'S',
      email: 'homer.j@s',
      website: ''
    })
    const platformMountAction1 = PlatformMountAction.createFromObject({
      id: '1111',
      platform: platform1,
      offsetX: 1,
      offsetY: 2,
      offsetZ: 3,
      description: 'This is the very first mount',
      contact: contact1,
      date: DateTime.utc(2021, 12, 15, 9, 0, 0),
      parentPlatform: null
    })
    const deviceMountAction1 = DeviceMountAction.createFromObject({
      id: '1112',
      device: device1,
      offsetX: -1,
      offsetY: -2,
      offsetZ: -3,
      description: 'Mount of the device on the platform',
      contact: contact1,
      parentPlatform: platform1,
      date: DateTime.utc(2021, 12, 15, 9, 0, 0)
    })
    const configuration = Configuration.createFromObject({
      id: '123',
      label: 'test config',
      startDate: null,
      endDate: null,
      projectName: '',
      projectUri: '',
      staticLocationBeginActions: [],
      staticLocationEndActions: [],
      dynamicLocationBeginActions: [],
      dynamicLocationEndActions: [],
      platformMountActions: [platformMountAction1],
      platformUnmountActions: [],
      deviceMountActions: [deviceMountAction1],
      deviceUnmountActions: [],
      contacts: [],
      status: '',
      location: null,
      permissionGroup: null,
      visibility: Visibility.Internal,
      createdAt: null,
      updatedAt: null,
      createdBy: null,
      updatedBy: null,
      createdByUserId: null
    })

    const selectedDate = DateTime.utc(2021, 12, 15, 9, 15, 0)
    const tree = buildConfigurationTree(configuration, selectedDate)
    const platformTreeNode: PlatformNode = tree.getPlatformById(platform1.id!)! // id of the platform & not the mount of the platform

    expect(platformTreeNode).not.toBeNull()

    configurationHelper.addNewMountAction(platformTreeNode, {
      offsetX: 29,
      offsetY: 30,
      offsetZ: 17,
      description: 'Changed offsets for platform',
      contact: contact1
    }, configuration, selectedDate, platformTreeNode)

    expect(configuration.platformMountActions.length).toEqual(2)
    expect(configuration.platformMountActions[0].offsetX).toEqual(1)
    expect(configuration.platformMountActions[1].offsetX).toEqual(29)
  })
})
