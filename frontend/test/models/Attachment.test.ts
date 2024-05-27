/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'
import { Attachment } from '@/models/Attachment'

describe('Attachment Models', () => {
  test('create a Attachment from an object', () => {
    const attachment = Attachment.createFromObject({
      id: '1',
      url: 'https://foo/test.png',
      label: 'Testpicture',
      description: 'An example attachment',
      isUpload: true,
      createdAt: DateTime.utc(2023, 2, 28, 12, 0, 0)
    })
    expect(typeof attachment).toBe('object')
    expect(attachment).toHaveProperty('id', '1')
    expect(attachment).toHaveProperty('url', 'https://foo/test.png')
    expect(attachment).toHaveProperty('label', 'Testpicture')
    expect(attachment).toHaveProperty('description', 'An example attachment')
    expect(attachment).toHaveProperty('isUpload', true)
    expect(attachment).toHaveProperty('createdAt', DateTime.utc(2023, 2, 28, 12, 0, 0))
  })
})
