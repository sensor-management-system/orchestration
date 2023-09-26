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
import { Parameter } from '@/models/Parameter'

import {
  ParameterEntityType,
  ParameterRelationEntityType,
  IParameterRelation,
  ParameterSerializer
} from '@/serializers/jsonapi/ParameterSerializer'

import {
  IJsonApiEntityListEnvelope,
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiRelationships
} from '@/serializers/jsonapi/JsonApiTypes'

describe('ParameterSerializer', () => {
  describe('#convertJsonApiDataToModel', () => {
    it('should convert an example payload to a model', () => {
      const data = {
        id: '123',
        type: 'device_parameter',
        attributes: {
          label: 'Test Parameter',
          description: 'Test parameter description',
          unit_name: 'Test Unit',
          unit_uri: 'http://www.unit.com/test'
        }
      }

      const serializer = new ParameterSerializer(ParameterEntityType.DEVICE)
      const model = serializer.convertJsonApiDataToModel(data)

      expect(model.id).toEqual('123')
      expect(model.label).toEqual('Test Parameter')
      expect(model.description).toEqual('Test parameter description')
      expect(model.unitName).toEqual('Test Unit')
      expect(model.unitUri).toEqual('http://www.unit.com/test')
    })
  })
  describe('#convertJsonApiObjectToModel', () => {
    it('should convert an example payload to a model', () => {
      const data = {
        data: {
          id: '123',
          type: 'device_parameter',
          attributes: {
            label: 'Test Parameter',
            description: 'Test parameter description',
            unit_name: 'Test Unit',
            unit_uri: 'http://www.unit.com/test'
          },
          relationships: {}
        },
        included: []
      }

      const serializer = new ParameterSerializer(ParameterEntityType.DEVICE)
      const model = serializer.convertJsonApiObjectToModel(data)

      expect(model.id).toEqual('123')
      expect(model.label).toEqual('Test Parameter')
      expect(model.description).toEqual('Test parameter description')
      expect(model.unitName).toEqual('Test Unit')
      expect(model.unitUri).toEqual('http://www.unit.com/test')
    })
  })
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert an example payload with a list of parameters to a list of models', () => {
      const data: IJsonApiEntityListEnvelope = {
        data: [
          {
            id: '123',
            type: 'device_parameter',
            attributes: {
              label: 'Test Parameter 1',
              description: 'Test parameter description one',
              unit_name: 'Test Unit 1',
              unit_uri: 'http://www.unit.com/test1'
            },
            relationships: {}
          }, {
            id: '456',
            type: 'device_parameter',
            attributes: {
              label: 'Test Parameter 2',
              description: 'Test parameter description two',
              unit_name: 'Test Unit 2',
              unit_uri: 'http://www.unit.com/test2'
            },
            relationships: {}
          }
        ],
        included: []
      }

      const serializer = new ParameterSerializer(ParameterEntityType.DEVICE)
      const result = serializer.convertJsonApiObjectListToModelList(data)

      expect(result.length).toEqual(2)
      expect(result[0].id).toEqual('123')
      expect(result[0].label).toEqual('Test Parameter 1')
      expect(result[0].description).toEqual('Test parameter description one')
      expect(result[0].unitName).toEqual('Test Unit 1')
      expect(result[0].unitUri).toEqual('http://www.unit.com/test1')
      expect(result[1].id).toEqual('456')
      expect(result[1].label).toEqual('Test Parameter 2')
      expect(result[1].description).toEqual('Test parameter description two')
      expect(result[1].unitName).toEqual('Test Unit 2')
      expect(result[1].unitUri).toEqual('http://www.unit.com/test2')
    })
  })
  describe('#convertJsonApiRelationshipsModelList', () => {
    it('should convert an example payload with a relationships to parameters and included entities to a list of models', () => {
      const relationships: IJsonApiRelationships = {
        device_parameters: {
          data: [
            {
              id: '123',
              type: 'device_parameter'
            },
            {
              id: '456',
              type: 'device_parameter'
            }
          ]
        }
      }
      const included: IJsonApiEntityWithOptionalAttributes[] = [
        {
          id: '123',
          type: 'device_parameter',
          attributes: {
            label: 'Test Parameter 1',
            description: 'Test parameter description one',
            unit_name: 'Test Unit 1',
            unit_uri: 'http://www.unit.com/test1'
          }
        },
        {
          id: '456',
          type: 'device_parameter',
          attributes: {
            label: 'Test Parameter 2',
            description: 'Test parameter description two',
            unit_name: 'Test Unit 2',
            unit_uri: 'http://www.unit.com/test2'
          }
        }
      ]

      const serializer = new ParameterSerializer(ParameterEntityType.DEVICE)
      const result = serializer.convertJsonApiRelationshipsModelList(relationships, included)

      expect(result.length).toEqual(2)
      expect(result[0].id).toEqual('123')
      expect(result[0].label).toEqual('Test Parameter 1')
      expect(result[0].description).toEqual('Test parameter description one')
      expect(result[0].unitName).toEqual('Test Unit 1')
      expect(result[0].unitUri).toEqual('http://www.unit.com/test1')
      expect(result[1].id).toEqual('456')
      expect(result[1].label).toEqual('Test Parameter 2')
      expect(result[1].description).toEqual('Test parameter description two')
      expect(result[1].unitName).toEqual('Test Unit 2')
      expect(result[1].unitUri).toEqual('http://www.unit.com/test2')
    })
  })
  describe('#convertModelListToTupleListWithIdAndType', () => {
    it('should convert a list of parameters to a list of JSONAPI entities with id and type only', () => {
      const parameter1 = Parameter.createFromObject({
        id: '123',
        label: 'Test Parameter 1',
        description: 'Test parameter description one',
        unitName: 'Test Unit 1',
        unitUri: 'http://www.unit.com/test1'
      })
      const parameter2 = Parameter.createFromObject({
        id: '456',
        label: 'Test Parameter 2',
        description: 'Test parameter description two',
        unitName: 'Test Unit 2',
        unitUri: 'http://www.unit.com/test2'
      })
      const serializer = new ParameterSerializer(ParameterEntityType.DEVICE)
      const result = serializer.convertModelListToTupleListWithIdAndType([parameter1, parameter2])

      expect(result.length).toEqual(2)
      expect(result[0].type).toEqual('device_parameter')
      expect(result[0].id).toEqual('123')
      expect(result[1].type).toEqual('device_parameter')
      expect(result[1].id).toEqual('456')
    })
  })
  describe('#convertModelListToJsonApiRelationshipsObject', () => {
    it('should convert a list of parameters to a JSONAPI relationship object', () => {
      const parameter1 = Parameter.createFromObject({
        id: '123',
        label: 'Test Parameter 1',
        description: 'Test parameter description one',
        unitName: 'Test Unit 1',
        unitUri: 'http://www.unit.com/test1'
      })
      const parameter2 = Parameter.createFromObject({
        id: '456',
        label: 'Test Parameter 2',
        description: 'Test parameter description two',
        unitName: 'Test Unit 2',
        unitUri: 'http://www.unit.com/test2'
      })
      const serializer = new ParameterSerializer(ParameterEntityType.DEVICE)
      const result = serializer.convertModelListToJsonApiRelationshipObject([parameter1, parameter2])

      expect(result).toHaveProperty('device_parameters')
      expect(result.device_parameters).toHaveProperty('data')
      expect(result.device_parameters.data.length).toEqual(2)
      expect(result.device_parameters.data[0].type).toEqual('device_parameter')
      expect(result.device_parameters.data[0].id).toEqual('123')
      expect(result.device_parameters.data[1].type).toEqual('device_parameter')
      expect(result.device_parameters.data[1].id).toEqual('456')
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should convert a simple model with a device relation to a JSONAPI payload', () => {
      const parameter = Parameter.createFromObject({
        id: '123',
        label: 'Test Parameter',
        description: 'This is a test parameter',
        unitName: 'Test Unit',
        unitUri: 'http://www.unit.com/test'
      })
      const relation: IParameterRelation = {
        entityType: ParameterRelationEntityType.DEVICE,
        id: '456'
      }

      const serializer = new ParameterSerializer(ParameterEntityType.DEVICE)
      const jsonApiPayload = serializer.convertModelToJsonApiData(
        parameter,
        relation
      )

      expect(jsonApiPayload).toHaveProperty('id')
      expect(jsonApiPayload.id).toEqual('123')
      expect(jsonApiPayload).toHaveProperty('type')
      expect(jsonApiPayload.type).toEqual('device_parameter')
      expect(jsonApiPayload).toHaveProperty('attributes')
      expect(jsonApiPayload.attributes).toHaveProperty('label')
      expect(jsonApiPayload.attributes.label).toEqual('Test Parameter')
      expect(jsonApiPayload.attributes).toHaveProperty('description')
      expect(jsonApiPayload.attributes.description).toEqual('This is a test parameter')
      expect(jsonApiPayload.attributes).toHaveProperty('unit_name')
      expect(jsonApiPayload.attributes.unit_name).toEqual('Test Unit')
      expect(jsonApiPayload.attributes).toHaveProperty('unit_uri')
      expect(jsonApiPayload.attributes.unit_uri).toEqual('http://www.unit.com/test')
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
})
