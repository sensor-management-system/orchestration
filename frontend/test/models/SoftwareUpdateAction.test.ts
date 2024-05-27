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
import { SoftwareUpdateAction } from '@/models/SoftwareUpdateAction'

describe('SoftwareUpdateAction', () => {
  test('create a SoftwareUpdateAction from an object', () => {
    const date1 = DateTime.fromISO('2021-05-27')

    const attachment = new Attachment()
    attachment.id = '1'
    attachment.label = 'an attachment'
    attachment.url = 'https://foo/baz'

    const contact = new Contact()
    contact.givenName = 'Homer'
    contact.familyName = 'Simpson'
    contact.email = 'homer.simpson@springfield.com'

    const action = SoftwareUpdateAction.createFromObject({
      id: '1',
      description: 'This is a software update action description',
      softwareTypeName: 'Software Update',
      softwareTypeUrl: 'https://foo/bar',
      updateDate: date1,
      version: '1.03',
      repositoryUrl: 'https://git.gfz-potsdam.de/sensor-system-management/frontend',
      contact,
      attachments: [attachment],
      icon: '',
      color: ''
    })

    expect(typeof action).toBe('object')
    expect(action).toHaveProperty('id', '1')
    expect(action).toHaveProperty('description', 'This is a software update action description')
    expect(action).toHaveProperty('softwareTypeName', 'Software Update')
    expect(action).toHaveProperty('softwareTypeUrl', 'https://foo/bar')
    expect(action).toHaveProperty('version', '1.03')
    expect(action).toHaveProperty('repositoryUrl', 'https://git.gfz-potsdam.de/sensor-system-management/frontend')
    expect(action.updateDate).toBe(date1)
    expect(action.date).toBe(date1)
    expect(action.contact).toStrictEqual(contact)
    expect(action.attachments).toContainEqual(attachment)
    expect(action.isSoftwareUpdateAction).toBeTruthy()
  })
})
