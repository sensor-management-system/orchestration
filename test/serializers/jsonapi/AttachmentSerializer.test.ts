/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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
import { Attachment } from '@/models/Attachment'

import { AttachmentSerializer } from '@/serializers/jsonapi/AttachmentSerializer'

describe('AttachmentSerializer', () => {
  describe('#convertJsonApiElementToModel', () => {
    const jsonApiElement = {
      id: '3'
      // no label, no url
    }

    const expectedAttachment = new Attachment()
    expectedAttachment.id = '3'

    const serializer = new AttachmentSerializer()
    const attachment = serializer.convertJsonApiElementToModel(jsonApiElement)

    expect(attachment).toEqual(expectedAttachment)
  })
  describe('#convertNestedJsonApiToModelList', () => {
    it('should convert a list of entries to models', () => {
      const jsonApiElements = [{
        label: 'test label',
        url: 'http://test.test',
        id: '1'
      }, {
        label: 'test label 2',
        url: 'http://test.test2',
        id: '2'
      }]
      const expectedAttachment1 = Attachment.createFromObject({
        id: '1',
        url: 'http://test.test',
        label: 'test label'
      })
      const expectedAttachment2 = Attachment.createFromObject({
        id: '2',
        url: 'http://test.test2',
        label: 'test label 2'
      })

      const serializer = new AttachmentSerializer()

      const attachments = serializer.convertNestedJsonApiToModelList(jsonApiElements)

      expect(Array.isArray(attachments)).toBeTruthy()
      expect(attachments.length).toEqual(2)
      expect(attachments[0]).toEqual(expectedAttachment1)
      expect(attachments[1]).toEqual(expectedAttachment2)
    })
  })
  describe('#convertJsonApiElementToModel', () => {
    it('should convert an element to model', () => {
      const jsonApiElement = {
        label: 'test label',
        url: 'http://test.test',
        id: '1'
      }
      const expectedAttachment = Attachment.createFromObject({
        id: '1',
        url: 'http://test.test',
        label: 'test label'
      })

      const serializer = new AttachmentSerializer()

      const attachment = serializer.convertJsonApiElementToModel(jsonApiElement)

      expect(attachment).toEqual(expectedAttachment)
    })
  })
  describe('#convertModelListToNestedJsonApiArray', () => {
    it('should convert a list of attachments to a list of json objects', () => {
      const attachments = [
        Attachment.createFromObject({
          id: '2',
          label: 'GFZ',
          url: 'http://www.gfz-potsdam.de'
        }),
        Attachment.createFromObject({
          id: null,
          label: 'UFZ',
          url: 'http://www.ufz.de'
        })
      ]

      const serializer = new AttachmentSerializer()

      const elements = serializer.convertModelListToNestedJsonApiArray(attachments)

      expect(Array.isArray(elements)).toBeTruthy()
      expect(elements.length).toEqual(2)
      expect(elements[0]).toEqual({
        id: '2',
        label: 'GFZ',
        url: 'http://www.gfz-potsdam.de'
      })
      expect(elements[1]).toEqual({
        label: 'UFZ',
        url: 'http://www.ufz.de'
      })
    })
  })
})
