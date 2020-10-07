import { CustomTextField } from '@/models/CustomTextField'

import CustomTextFieldSerializer from '@/serializers/jsonapi/CustomTextFieldSerializer'

describe('CustomTextFieldSerializer', () => {
  describe('#convertNestedJsonApiToModelList', () => {
    it('should convert a list of entries to models', () => {
      const jsonApiElements = [{
        id: '44',
        key: 'a',
        value: 'b'
      }, {
        id: '45',
        key: 'c',
        value: 'd'
      }]
      const expectedCustomField1 = CustomTextField.createFromObject({
        id: '44',
        key: 'a',
        value: 'b'
      })
      const expectedCustomField2 = CustomTextField.createFromObject({
        id: '45',
        key: 'c',
        value: 'd'
      })

      const serializer = new CustomTextFieldSerializer()

      const customfields = serializer.convertNestedJsonApiToModelList(jsonApiElements)

      expect(Array.isArray(customfields)).toBeTruthy()
      expect(customfields.length).toEqual(2)
      expect(customfields[0]).toEqual(expectedCustomField1)
      expect(customfields[1]).toEqual(expectedCustomField2)
    })
  })
  describe('#convertJsonApiElementToModel', () => {
    it('should convert an element to model', () => {
      const jsonApiElement = {
        id: '44',
        key: 'a',
        value: 'b'
      }
      const expectedCustomField = CustomTextField.createFromObject({
        id: '44',
        key: 'a',
        value: 'b'
      })

      const serializer = new CustomTextFieldSerializer()

      const customfield = serializer.convertJsonApiElementToModel(jsonApiElement)

      expect(customfield).toEqual(expectedCustomField)
    })
  })
})
