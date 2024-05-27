/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2024
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'
import { Attachment } from '@/models/Attachment'
import { Contact } from '@/models/Contact'
import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'
import { DeviceProperty } from '@/models/DeviceProperty'

describe('DeviceCalibrationAction', () => {
  test('create a DeviceCalibrationAction from an object', () => {
    const date1 = DateTime.fromISO('2021-05-27')
    const date2 = DateTime.fromISO('2021-06-03')

    const attachment = new Attachment()
    attachment.id = '1'
    attachment.label = 'an attachment'
    attachment.url = 'https://foo/baz'

    const contact = new Contact()
    contact.givenName = 'Homer'
    contact.familyName = 'Simpson'
    contact.email = 'homer.simpson@springfield.com'

    const measuredQuantity1 = new DeviceProperty()
    measuredQuantity1.label = 'Quantity 1'

    const action = DeviceCalibrationAction.createFromObject({
      id: '1',
      description: 'This is a device calibration action description',
      formula: 'x',
      value: 3,
      currentCalibrationDate: date1,
      nextCalibrationDate: date2,
      measuredQuantities: [measuredQuantity1],
      contact,
      attachments: [attachment],
      icon: '',
      color: ''
    })

    expect(typeof action).toBe('object')
    expect(action).toHaveProperty('id', '1')
    expect(action).toHaveProperty('description', 'This is a device calibration action description')
    expect(action).toHaveProperty('formula', 'x')
    expect(action).toHaveProperty('value', 3)
    expect(action.currentCalibrationDate).toBe(date1)
    expect(action.nextCalibrationDate).toBe(date2)
    expect(action.date).toBe(date1)
    expect(action.contact).toStrictEqual(contact)
    expect(action.attachments).toContainEqual(attachment)
    expect(action.measuredQuantities).toContainEqual(measuredQuantity1)
    expect(action.isDeviceCalibrationAction).toBeTruthy()
  })
})
