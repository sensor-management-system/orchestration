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
import { CustomTextField } from '@/models/CustomTextField'

import { CustomTextFieldSerializer } from '@/serializers/jsonapi/CustomTextFieldSerializer'

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
  describe('#convertModelListToNestedJsonApiArray', () => {
    it('should convert a list of custom text fields to a list of json objects', () => {
      const customfields = [
        CustomTextField.createFromObject({
          id: '1',
          key: 'First custom field',
          value: 'First custom value'
        }),
        CustomTextField.createFromObject({
          id: null,
          key: 'Second custom field',
          value: ''
        })
      ]

      const serializer = new CustomTextFieldSerializer()

      const elements = serializer.convertModelListToNestedJsonApiArray(customfields)

      expect(Array.isArray(elements)).toBeTruthy()
      expect(elements.length).toEqual(2)
      expect(elements[0]).toEqual({
        id: '1',
        key: 'First custom field',
        value: 'First custom value'
      })
      expect(elements[1]).toEqual({
        key: 'Second custom field',
        value: ''
      })
    })
  })
})
