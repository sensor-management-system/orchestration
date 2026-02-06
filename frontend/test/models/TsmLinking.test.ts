/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2026
 * SPDX-License-Identifier: EUPL-1.2
 */

import { DateTime } from 'luxon'
import { TsmLinking } from '@/models/TsmLinking'
import { DeviceProperty } from '@/models/DeviceProperty'
import { DeviceMountAction } from '@/models/DeviceMountAction'
import { Device } from '@/models/Device'
import { Visibility } from '@/models/Visibility'
import { Contact } from '@/models/Contact'

describe('TsmLinking', () => {
  describe('#equalsByIdOrMountActionAndDeviceProperty', () => {
    it('should return true if IDs are equal', () => {
      const tsmLinking1 = new TsmLinking()
      tsmLinking1.id = '123'
      const tsmLinking2 = new TsmLinking()
      tsmLinking2.id = '123'
      expect(tsmLinking1.equalsByIdOrMountActionAndDeviceProperty(tsmLinking2)).toBeTruthy()
    })

    it('should return true if device properties and mount actions are equal', () => {
      const deviceProperty = new DeviceProperty()
      deviceProperty.id = 'prop1'

      const deviceMountAction = getDummyDeviceMountAction()
      deviceMountAction.id = 'action1'

      const tsmLinking1 = new TsmLinking()
      tsmLinking1.deviceProperty = deviceProperty
      tsmLinking1.deviceMountAction = deviceMountAction

      const tsmLinking2 = new TsmLinking()
      tsmLinking2.deviceProperty = deviceProperty
      tsmLinking2.deviceMountAction = deviceMountAction

      expect(tsmLinking1.equalsByIdOrMountActionAndDeviceProperty(tsmLinking2)).toBeTruthy()
    })

    it('should return false if IDs are not equal', () => {
      const tsmLinking1 = new TsmLinking()
      tsmLinking1.id = '123'

      const tsmLinking2 = new TsmLinking()
      tsmLinking2.id = '456'

      expect(tsmLinking1.equalsByIdOrMountActionAndDeviceProperty(tsmLinking2)).toBeFalsy()
    })

    it('should return false if device properties are equal but mount actions are not', () => {
      const deviceProperty = new DeviceProperty()
      deviceProperty.id = 'prop1'

      const deviceMountAction1 = getDummyDeviceMountAction()
      deviceMountAction1.id = 'action1'

      const deviceMountAction2 = getDummyDeviceMountAction()
      deviceMountAction2.id = 'action2'

      const tsmLinking1 = new TsmLinking()
      tsmLinking1.deviceProperty = deviceProperty
      tsmLinking1.deviceMountAction = deviceMountAction1

      const tsmLinking2 = new TsmLinking()
      tsmLinking2.deviceProperty = deviceProperty
      tsmLinking2.deviceMountAction = deviceMountAction2

      expect(tsmLinking1.equalsByIdOrMountActionAndDeviceProperty(tsmLinking2)).toBeFalsy()
    })

    it('should return false if mount actions are equal but device properties are not', () => {
      const deviceMountAction = getDummyDeviceMountAction()
      deviceMountAction.id = 'action1'

      const deviceProperty1 = new DeviceProperty()
      deviceProperty1.id = 'prop1'

      const deviceProperty2 = new DeviceProperty()
      deviceProperty2.id = 'prop2'

      const tsmLinking1 = new TsmLinking()
      tsmLinking1.deviceProperty = deviceProperty1
      tsmLinking1.deviceMountAction = deviceMountAction

      const tsmLinking2 = new TsmLinking()
      tsmLinking2.deviceProperty = deviceProperty2
      tsmLinking2.deviceMountAction = deviceMountAction

      expect(tsmLinking1.equalsByIdOrMountActionAndDeviceProperty(tsmLinking2)).toBeFalsy()
    })
  })

  describe('#hasSameId', () => {
    it('should return true if both have the same ID', () => {
      const tsmLinking1 = new TsmLinking()
      tsmLinking1.id = '123'
      const tsmLinking2 = new TsmLinking()
      tsmLinking2.id = '123'
      expect(tsmLinking1.hasSameId(tsmLinking2)).toBeTruthy()
    })

    it('should return false if one has ID and the other does not', () => {
      const tsmLinking1 = new TsmLinking()
      tsmLinking1.id = '123'
      const tsmLinking2 = new TsmLinking()
      expect(tsmLinking1.hasSameId(tsmLinking2)).toBeFalsy()
    })

    it('should return false if IDs are different', () => {
      const tsmLinking1 = new TsmLinking()
      tsmLinking1.id = '123'
      const tsmLinking2 = new TsmLinking()
      tsmLinking2.id = '456'
      expect(tsmLinking1.hasSameId(tsmLinking2)).toBeFalsy()
    })
  })

  describe('#hasSameDeviceProperties', () => {
    it('should return true if both have the same device property ID', () => {
      const deviceProperty = new DeviceProperty()
      deviceProperty.id = 'prop1'

      const tsmLinking1 = new TsmLinking()
      tsmLinking1.deviceProperty = deviceProperty

      const tsmLinking2 = new TsmLinking()
      tsmLinking2.deviceProperty = deviceProperty

      expect(tsmLinking1.hasSameDeviceProperties(tsmLinking2)).toBeTruthy()
    })

    it('should return false if one has device property and the other does not', () => {
      const deviceProperty = new DeviceProperty()
      deviceProperty.id = 'prop1'

      const tsmLinking1 = new TsmLinking()
      tsmLinking1.deviceProperty = deviceProperty

      const tsmLinking2 = new TsmLinking()

      expect(tsmLinking1.hasSameDeviceProperties(tsmLinking2)).toBeFalsy()
    })

    it('should return false if device property IDs are different', () => {
      const deviceProperty1 = new DeviceProperty()
      deviceProperty1.id = 'prop1'

      const deviceProperty2 = new DeviceProperty()
      deviceProperty2.id = 'prop2'

      const tsmLinking1 = new TsmLinking()
      tsmLinking1.deviceProperty = deviceProperty1

      const tsmLinking2 = new TsmLinking()
      tsmLinking2.deviceProperty = deviceProperty2

      expect(tsmLinking1.hasSameDeviceProperties(tsmLinking2)).toBeFalsy()
    })
  })

  describe('#hasSameMountAction', () => {
    it('should return true if both have the same mount action ID', () => {
      const deviceMountAction = getDummyDeviceMountAction()
      deviceMountAction.id = 'action1'

      const tsmLinking1 = new TsmLinking()
      tsmLinking1.deviceMountAction = deviceMountAction

      const tsmLinking2 = new TsmLinking()
      tsmLinking2.deviceMountAction = deviceMountAction

      expect(tsmLinking1.hasSameMountAction(tsmLinking2)).toBeTruthy()
    })

    it('should return false if one has mount action and the other does not', () => {
      const deviceMountAction = getDummyDeviceMountAction()
      deviceMountAction.id = 'action1'

      const tsmLinking1 = new TsmLinking()
      tsmLinking1.deviceMountAction = deviceMountAction

      const tsmLinking2 = new TsmLinking()

      expect(tsmLinking1.hasSameMountAction(tsmLinking2)).toBeFalsy()
    })

    it('should return false if mount action IDs are different', () => {
      const deviceMountAction1 = getDummyDeviceMountAction()
      deviceMountAction1.id = 'action1'

      const deviceMountAction2 = getDummyDeviceMountAction()
      deviceMountAction2.id = 'action2'

      const tsmLinking1 = new TsmLinking()
      tsmLinking1.deviceMountAction = deviceMountAction1

      const tsmLinking2 = new TsmLinking()
      tsmLinking2.deviceMountAction = deviceMountAction2

      expect(tsmLinking1.hasSameMountAction(tsmLinking2)).toBeFalsy()
    })
  })
})

function getDummyDeviceMountAction (): DeviceMountAction {
  return DeviceMountAction.createFromObject({
    id: '6',
    offsetX: 5,
    offsetY: 6,
    offsetZ: 7,
    epsgCode: '',
    x: null,
    y: null,
    z: null,
    elevationDatumName: '',
    elevationDatumUri: '',
    beginContact: Contact.createFromObject({
      id: '4',
      givenName: 'Max',
      familyName: 'Mustermann',
      email: 'max@muster.mann',
      organization: '',
      website: '',
      orcid: '',
      createdAt: null,
      updatedAt: null,
      createdByUserId: null
    }),
    endContact: null,
    beginDescription: 'Second action',
    endDescription: '',
    beginDate: DateTime.fromISO('2022-04-14T12:08:13Z', { zone: 'UTC' }),
    endDate: null,
    label: '',
    device: Device.createFromObject({
      id: '7',
      serialNumber: '100123',
      model: '1815',
      description: 'Soil Moisture station device Boeken_BF1',
      deviceTypeUri: 'type/device',
      statusUri: 'status/existing',
      website: 'http://www.tereno.net/abc',
      longName: 'Soil moisture station device Boeken BF1, Germany',
      inventoryNumber: '1001234',
      manufacturerName: 'ABC-XYZ',
      shortName: 'boeken_BF11',
      statusName: 'existing',
      deviceTypeName: 'Device',
      persistentIdentifier: 'boeken_BF11',
      manufacturerUri: 'manufacturer/xy',
      contacts: [],
      createdBy: null,
      createdByUserId: null,
      createdAt: null,
      updatedAt: null,
      updateDescription: '',
      updatedBy: null,
      permissionGroups: [],
      visibility: Visibility.Internal,
      attachments: [],
      images: [],
      customFields: [],
      properties: [],
      parameters: [],
      archived: false,
      keywords: [],
      country: ''
    }),
    parentPlatform: null,
    parentDevice: null
  })
}
