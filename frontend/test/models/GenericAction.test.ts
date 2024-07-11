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
import { GenericAction } from '@/models/GenericAction'

describe('GenericAction', () => {
  test('create a GenericAction from an object', () => {
    const date1 = DateTime.fromISO('2021-05-27')
    const date2 = DateTime.fromISO('2021-05-28')

    const attachment = new Attachment()
    attachment.id = '1'
    attachment.label = 'an attachment'
    attachment.url = 'https://foo/baz'

    const contact = new Contact()
    contact.givenName = 'Homer'
    contact.familyName = 'Simpson'
    contact.email = 'homer.simpson@springfield.com'

    const action = GenericAction.createFromObject({
      id: '1',
      description: 'This is a generic action description',
      actionTypeName: 'Generic Device Action',
      actionTypeUrl: 'https://foo/bar',
      beginDate: date1,
      endDate: date2,
      contact,
      attachments: [attachment],
      icon: '',
      color: ''
    })

    expect(typeof action).toBe('object')
    expect(action).toHaveProperty('id', '1')
    expect(action).toHaveProperty('description', 'This is a generic action description')
    expect(action).toHaveProperty('actionTypeName', 'Generic Device Action')
    expect(action).toHaveProperty('actionTypeUrl', 'https://foo/bar')
    expect(action.beginDate).toBe(date1)
    expect(action.endDate).toBe(date2)
    expect(action.date).toBe(date1)
    expect(action.contact).toStrictEqual(contact)
    expect(action.attachments).toContainEqual(attachment)
    expect(action.isGenericAction).toBeTruthy()
  })
})
