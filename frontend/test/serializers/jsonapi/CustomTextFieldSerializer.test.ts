/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
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

import {
  CustomTextFieldEntityType,
  CustomTextFieldRelationEntityType,
  CustomTextFieldSerializer
} from '@/serializers/jsonapi/CustomTextFieldSerializer'

import {
  IJsonApiEntityListEnvelope
} from '@/serializers/jsonapi/JsonApiTypes'

describe('CustomTextFieldSerializer', () => {
  describe('#convertNestedJsonApiToModelList', () => {
    it('should convert a list of entries to models', () => {
      const jsonApiElements = [{
        id: '44',
        key: 'a',
        value: 'b',
        description: 'a key'
      }, {
        id: '45',
        key: 'c',
        value: 'd',
        description: 'c key'
      }]
      const expectedCustomField1 = CustomTextField.createFromObject({
        id: '44',
        key: 'a',
        value: 'b',
        description: 'a key'
      })
      const expectedCustomField2 = CustomTextField.createFromObject({
        id: '45',
        key: 'c',
        value: 'd',
        description: 'c key'
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
        value: 'b',
        description: 'c'
      }
      const expectedCustomField = CustomTextField.createFromObject({
        id: '44',
        key: 'a',
        value: 'b',
        description: 'c'
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
          value: 'First custom value',
          description: 'First description'
        }),
        CustomTextField.createFromObject({
          id: null,
          key: 'Second custom field',
          value: '',
          description: ''
        })
      ]

      const serializer = new CustomTextFieldSerializer()

      const elements = serializer.convertModelListToNestedJsonApiArray(customfields)

      expect(Array.isArray(elements)).toBeTruthy()
      expect(elements.length).toEqual(2)
      expect(elements[0]).toEqual({
        id: '1',
        key: 'First custom field',
        value: 'First custom value',
        description: 'First description'
      })
      expect(elements[1]).toEqual({
        key: 'Second custom field',
        value: '',
        description: ''
      })
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should convert a simple model to a json:api payload', () => {
      const customfield = CustomTextField.createFromObject({
        id: '123',
        key: 'some key',
        value: 'test test test',
        description: 'some description'
      })
      const serializer = new CustomTextFieldSerializer(CustomTextFieldEntityType.DEVICE)
      const deviceId = '456'

      const jsonApiPayload = serializer.convertModelToJsonApiData(
        customfield,
        {
          entityType: CustomTextFieldRelationEntityType.DEVICE,
          id: deviceId
        }
      )

      expect(jsonApiPayload).toHaveProperty('id')
      expect(jsonApiPayload.id).toEqual('123')
      expect(jsonApiPayload).toHaveProperty('type')
      expect(jsonApiPayload.type).toEqual('customfield')
      expect(jsonApiPayload).toHaveProperty('attributes')
      expect(jsonApiPayload.attributes).toHaveProperty('key')
      expect(jsonApiPayload.attributes.key).toEqual('some key')
      expect(jsonApiPayload.attributes).toHaveProperty('value')
      expect(jsonApiPayload.attributes.value).toEqual('test test test')
      expect(jsonApiPayload.attributes).toHaveProperty('description')
      expect(jsonApiPayload.attributes.description).toEqual('some description')
      expect(jsonApiPayload).toHaveProperty('relationships')
      expect(jsonApiPayload.relationships).toHaveProperty('device')
      expect(jsonApiPayload.relationships!.device).toHaveProperty('data')
      const deviceData: any = jsonApiPayload.relationships!.device.data
      expect(deviceData).toHaveProperty('id')
      expect(deviceData.id).toEqual('456')
      expect(deviceData).toHaveProperty('type')
      expect(deviceData.type).toEqual('device')
    })
    it('should convert a simple model to a json:api payload with a configuration relation', () => {
      const customfield = CustomTextField.createFromObject({
        id: '123',
        key: 'some key',
        value: 'test test test',
        description: 'some description'
      })
      const serializer = new CustomTextFieldSerializer(CustomTextFieldEntityType.CONFIGURATION)
      const configurationId = '456'

      const jsonApiPayload = serializer.convertModelToJsonApiData(
        customfield,
        {
          entityType: CustomTextFieldRelationEntityType.CONFIGURATION,
          id: configurationId
        }
      )

      expect(jsonApiPayload).toHaveProperty('id')
      expect(jsonApiPayload.id).toEqual('123')
      expect(jsonApiPayload).toHaveProperty('type')
      expect(jsonApiPayload.type).toEqual('configuration_customfield')
      expect(jsonApiPayload).toHaveProperty('attributes')
      expect(jsonApiPayload.attributes).toHaveProperty('key')
      expect(jsonApiPayload.attributes.key).toEqual('some key')
      expect(jsonApiPayload.attributes).toHaveProperty('value')
      expect(jsonApiPayload.attributes.value).toEqual('test test test')
      expect(jsonApiPayload.attributes).toHaveProperty('description')
      expect(jsonApiPayload.attributes.description).toEqual('some description')
      expect(jsonApiPayload).toHaveProperty('relationships')
      expect(jsonApiPayload.relationships).toHaveProperty('configuration')
      expect(jsonApiPayload.relationships!.configuration).toHaveProperty('data')
      const configurationData: any = jsonApiPayload.relationships!.configuration.data
      expect(configurationData).toHaveProperty('id')
      expect(configurationData.id).toEqual('456')
      expect(configurationData).toHaveProperty('type')
      expect(configurationData.type).toEqual('configuration')
    })
    it('should also be possible if there is no id yet', () => {
      const customfield = CustomTextField.createFromObject({
        id: null,
        key: 'some key',
        value: 'test test test',
        description: 'some description'
      })
      const serializer = new CustomTextFieldSerializer(CustomTextFieldEntityType.DEVICE)
      const deviceId = '456'

      const jsonApiPayload = serializer.convertModelToJsonApiData(
        customfield,
        {
          entityType: CustomTextFieldRelationEntityType.DEVICE,
          id: deviceId
        }
      )

      expect(jsonApiPayload).not.toHaveProperty('id')
      expect(jsonApiPayload).toHaveProperty('type')
      expect(jsonApiPayload.type).toEqual('customfield')
      expect(jsonApiPayload).toHaveProperty('attributes')
      expect(jsonApiPayload.attributes).toHaveProperty('key')
      expect(jsonApiPayload.attributes.key).toEqual('some key')
      expect(jsonApiPayload.attributes).toHaveProperty('value')
      expect(jsonApiPayload.attributes.value).toEqual('test test test')
      expect(jsonApiPayload.attributes).toHaveProperty('description')
      expect(jsonApiPayload.attributes.description).toEqual('some description')
      expect(jsonApiPayload).toHaveProperty('relationships')
      expect(jsonApiPayload.relationships).toHaveProperty('device')
      expect(jsonApiPayload.relationships!.device).toHaveProperty('data')
      const deviceData: any = jsonApiPayload.relationships!.device.data
      expect(deviceData).toHaveProperty('id')
      expect(deviceData.id).toEqual('456')
      expect(deviceData).toHaveProperty('type')
      expect(deviceData.type).toEqual('device')
    })
  })
  describe('#convertJsonApiDataToModel', () => {
    it('should convert an example payload to a model', () => {
      const data = {
        id: '123',
        type: 'customfield',
        attributes: {
          key: 'institute',
          value: 'GFZ'
        }
      }

      const serializer = new CustomTextFieldSerializer()
      const model = serializer.convertJsonApiDataToModel(data)

      expect(model.id).toEqual('123')
      expect(model.key).toEqual('institute')
      expect(model.value).toEqual('GFZ')
    })
    it('should also convert missing values to empty strings', () => {
      const data = {
        id: '123',
        type: 'customfield',
        attributes: {
        }
      }

      const serializer = new CustomTextFieldSerializer()
      const model = serializer.convertJsonApiDataToModel(data)

      expect(model.id).toEqual('123')
      expect(model.key).toEqual('')
      expect(model.value).toEqual('')
    })
  })
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert two paylods to customTextField models', () => {
      const data: IJsonApiEntityListEnvelope = {
        data: [
          {
            id: '123',
            type: 'customfield',
            attributes: {
              key: 'Website GFZ',
              value: 'www.gfz-potsdam.de'
            },
            relationships: {}
          }, {
            id: '124',
            type: 'customfield',
            attributes: {
              key: 'Website UFZ',
              value: 'www.ufz.de'
            },
            relationships: {}
          }
        ],
        included: []
      }

      const serializer = new CustomTextFieldSerializer()
      const models = serializer.convertJsonApiObjectListToModelList(data)

      expect(models.length).toEqual(2)
      expect(models[0].id).toEqual('123')
      expect(models[0].key).toEqual('Website GFZ')
      expect(models[0].value).toEqual('www.gfz-potsdam.de')

      expect(models[1].id).toEqual('124')
      expect(models[1].key).toEqual('Website UFZ')
      expect(models[1].value).toEqual('www.ufz.de')
    })
  })
  describe('#convertJsonApiObjectToModel', () => {
    it('should convert an example payload to a model', () => {
      const data = {
        data: {
          id: '123',
          type: 'customfield',
          attributes: {
            key: 'institute',
            value: 'GFZ'
          },
          relationships: {}
        },
        included: []
      }

      const serializer = new CustomTextFieldSerializer()
      const model = serializer.convertJsonApiObjectToModel(data)

      expect(model.id).toEqual('123')
      expect(model.key).toEqual('institute')
      expect(model.value).toEqual('GFZ')
    })
  })
})
