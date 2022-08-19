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
import { Platform } from '@/models/Platform'
import { PlatformMountAction } from '@/models/PlatformMountAction'
import { Contact } from '@/models/Contact'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Device } from '@/models/Device'
import { Visibility } from '@/models/Visibility'

import { buildConfigurationTree } from '@/modelUtils/mountHelpers'
import configurationHelper from '@/utils/configurationHelper'
import { PlatformNode } from '@/viewmodels/PlatformNode'

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
      beginDescription: 'This is the very first mount',
      endDescription: '',
      beginContact: contact1,
      endContact: null,
      beginDate: DateTime.utc(2021, 12, 15, 9, 0, 0),
      endDate: null,
      parentPlatform: null
    })
    const deviceMountAction1 = DeviceMountAction.createFromObject({
      id: '1112',
      device: device1,
      offsetX: -1,
      offsetY: -2,
      offsetZ: -3,
      beginDescription: 'Mount of the device on the platform',
      endDescription: '',
      beginContact: contact1,
      endContact: null,
      parentPlatform: platform1,
      beginDate: DateTime.utc(2021, 12, 15, 9, 0, 0),
      endDate: null
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
      deviceMountActions: [deviceMountAction1],
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
