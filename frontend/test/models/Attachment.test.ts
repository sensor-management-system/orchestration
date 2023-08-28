/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2023
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for
 *   Geosciences (GFZ, https://www.gfz-potsdam.de)
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
import { Attachment } from '@/models/Attachment'

describe('Attachment Models', () => {
  test('create a Attachment from an object', () => {
    const attachment = Attachment.createFromObject({
      id: '1',
      url: 'https://foo/test.png',
      label: 'Testpicture',
      isUpload: true,
      createdAt: DateTime.utc(2023, 2, 28, 12, 0, 0)
    })
    expect(typeof attachment).toBe('object')
    expect(attachment).toHaveProperty('id', '1')
    expect(attachment).toHaveProperty('url', 'https://foo/test.png')
    expect(attachment).toHaveProperty('label', 'Testpicture')
    expect(attachment).toHaveProperty('isUpload', true)
    expect(attachment).toHaveProperty('createdAt', DateTime.utc(2023, 2, 28, 12, 0, 0))
  })
})
