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
