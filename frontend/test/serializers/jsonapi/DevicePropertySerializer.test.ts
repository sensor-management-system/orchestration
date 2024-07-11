/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DeviceProperty } from '@/models/DeviceProperty'
import { MeasuringRange } from '@/models/MeasuringRange'

import { DevicePropertySerializer } from '@/serializers/jsonapi/DevicePropertySerializer'

describe('DevicePropertySerializer', () => {
  describe('#convertModelListToNestedJsonApiArray', () => {
    it('should convert a list of device properties to a list of json objects', () => {
      const properties = [
        DeviceProperty.createFromObject({
          id: '3',
          label: 'Prop 1',
          compartmentUri: 'compartment/Comp1',
          compartmentName: 'Comp 1',
          unitUri: 'unit/Unit1',
          unitName: 'Unit 1',
          samplingMediaUri: 'medium/Medium1',
          samplingMediaName: 'Medium 1',
          propertyUri: 'property/Prop1',
          propertyName: 'Property 1',
          measuringRange: MeasuringRange.createFromObject({
            min: -7,
            max: 7
          }),
          accuracy: 0.5,
          accuracyUnitUri: 'http://foo/unit/2',
          accuracyUnitName: 'cm',
          failureValue: -999,
          resolution: 0.001,
          resolutionUnitUri: 'http://foo/unit/1',
          resolutionUnitName: 'mm',
          aggregationTypeUri: 'http://foo/aggregationtypes/1',
          aggregationTypeName: 'Average',
          description: 'first property'
        }),
        DeviceProperty.createFromObject({
          id: null,
          label: 'Prop 2',
          compartmentUri: '',
          compartmentName: '',
          unitUri: '',
          unitName: '',
          samplingMediaUri: '',
          samplingMediaName: '',
          propertyUri: '',
          propertyName: '',
          measuringRange: MeasuringRange.createFromObject({
            min: null,
            max: null
          }),
          accuracy: null,
          accuracyUnitUri: '',
          accuracyUnitName: '',
          failureValue: null,
          resolution: 0.001,
          resolutionUnitUri: 'http://foo/unit/1',
          resolutionUnitName: 'mm',
          aggregationTypeUri: 'http://foo/aggregationtypes/2',
          aggregationTypeName: 'Mean',
          description: 'second property'
        })
      ]

      const serializer = new DevicePropertySerializer()

      const elements = serializer.convertModelListToNestedJsonApiArray(properties)

      expect(Array.isArray(elements)).toBeTruthy()
      expect(elements[0]).toEqual({
        id: '3',
        label: 'Prop 1',
        compartment_uri: 'compartment/Comp1',
        compartment_name: 'Comp 1',
        unit_uri: 'unit/Unit1',
        unit_name: 'Unit 1',
        sampling_media_uri: 'medium/Medium1',
        sampling_media_name: 'Medium 1',
        property_uri: 'property/Prop1',
        property_name: 'Property 1',
        measuring_range_min: -7,
        measuring_range_max: 7,
        accuracy: 0.5,
        accuracy_unit_uri: 'http://foo/unit/2',
        accuracy_unit_name: 'cm',
        failure_value: -999,
        resolution: 0.001,
        resolution_unit_uri: 'http://foo/unit/1',
        resolution_unit_name: 'mm',
        aggregation_type_uri: 'http://foo/aggregationtypes/1',
        aggregation_type_name: 'Average',
        description: 'first property'
      })
      expect(elements[1]).toEqual({
        label: 'Prop 2',
        compartment_uri: '',
        compartment_name: '',
        unit_uri: '',
        unit_name: '',
        sampling_media_uri: '',
        sampling_media_name: '',
        property_uri: '',
        property_name: '',
        measuring_range_min: null,
        measuring_range_max: null,
        accuracy: null,
        accuracy_unit_uri: '',
        accuracy_unit_name: '',
        failure_value: null,
        resolution: 0.001,
        resolution_unit_uri: 'http://foo/unit/1',
        resolution_unit_name: 'mm',
        aggregation_type_uri: 'http://foo/aggregationtypes/2',
        aggregation_type_name: 'Mean',
        description: 'second property'
      })
    })
  })
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should create a list of device properties', () => {
      const data = {
        data: [{
          id: '123',
          type: 'device_property',
          attributes: {
            compartment_name: 'Climate',
            unit_uri: 'abc',
            sampling_media_name: 'Other',
            compartment_uri: 'variabletype/Climate',
            property_name: 'Water vapor concentration',
            accuracy: 0.1,
            accuracy_unit_uri: 'http://foo/unit/2',
            accuracy_unit_name: 'cm',
            measuring_range_min: 10,
            measuring_range_max: -10,
            label: 'water vapor',
            property_uri: 'variablename/Water%20vapor%20concentration',
            unit_name: '%',
            failure_value: -234,
            sampling_media_uri: 'medium/Other',
            resolution: 0.001,
            resolution_unit_uri: 'http://foo/unit/1',
            resolution_unit_name: 'mm',
            aggregation_type_uri: 'http://foo/aggregationtypes/1',
            aggregation_type_name: 'Average'
          },
          relationships: {}
        }, {
          id: '456',
          type: 'device_property',
          attributes: {
            compartment_name: 'Resources',
            unit_uri: 'xyz',
            sampling_media_name: 'ether',
            compartment_uri: 'variabletype/Resources',
            property_name: 'abc',
            accuracy: -2.9,
            accuracy_unit_uri: 'http://foo/unit/33',
            accuracy_unit_name: 'kg',
            measuring_range_min: 100,
            measuring_range_max: -100,
            label: 'abc - prop',
            property_uri: 'variablename/abc',
            unit_name: 'n',
            failure_value: -999,
            sampling_media_uri: 'medium/ether',
            resolution: 0.008,
            resolution_unit_uri: 'http://foo/unit/100',
            resolution_unit_name: '°C',
            aggregation_type_uri: 'http://foo/aggregationtypes/2',
            aggregation_type_name: 'Mean',
            description: 'abc description'
          },
          relationships: {}
        }],
        included: []
      }
      const serializer = new DevicePropertySerializer()
      const models = serializer.convertJsonApiObjectListToModelList(data)

      expect(models.length).toEqual(2)
      expect(models[0].id).toEqual('123')
      expect(models[0].compartmentName).toEqual('Climate')
      expect(models[0].unitUri).toEqual('abc')
      expect(models[0].samplingMediaName).toEqual('Other')
      expect(models[0].compartmentUri).toEqual('variabletype/Climate')
      expect(models[0].propertyName).toEqual('Water vapor concentration')
      expect(models[0].accuracy).toEqual(0.1)
      expect(models[0].accuracyUnitUri).toEqual('http://foo/unit/2')
      expect(models[0].accuracyUnitName).toEqual('cm')
      // I know it is the wrong ordering
      expect(models[0].measuringRange.min).toEqual(10)
      expect(models[0].measuringRange.max).toEqual(-10)
      expect(models[0].label).toEqual('water vapor')
      expect(models[0].propertyUri).toEqual('variablename/Water%20vapor%20concentration')
      expect(models[0].unitName).toEqual('%')
      expect(models[0].failureValue).toEqual(-234)
      expect(models[0].samplingMediaUri).toEqual('medium/Other')
      expect(models[0].resolution).toEqual(0.001)
      expect(models[0].resolutionUnitUri).toEqual('http://foo/unit/1')
      expect(models[0].resolutionUnitName).toEqual('mm')
      expect(models[0].aggregationTypeUri).toEqual('http://foo/aggregationtypes/1')
      expect(models[0].aggregationTypeName).toEqual('Average')
      expect(models[0].description).toEqual('')

      expect(models[1].id).toEqual('456')
      expect(models[1].compartmentName).toEqual('Resources')
      expect(models[1].unitUri).toEqual('xyz')
      expect(models[1].samplingMediaName).toEqual('ether')
      expect(models[1].compartmentUri).toEqual('variabletype/Resources')
      expect(models[1].propertyName).toEqual('abc')
      expect(models[1].accuracy).toEqual(-2.9)
      expect(models[1].accuracyUnitUri).toEqual('http://foo/unit/33')
      expect(models[1].accuracyUnitName).toEqual('kg')
      expect(models[1].measuringRange.min).toEqual(100)
      expect(models[1].measuringRange.max).toEqual(-100)
      expect(models[1].label).toEqual('abc - prop')
      expect(models[1].propertyUri).toEqual('variablename/abc')
      expect(models[1].unitName).toEqual('n')
      expect(models[1].failureValue).toEqual(-999)
      expect(models[1].samplingMediaUri).toEqual('medium/ether')
      expect(models[1].resolution).toEqual(0.008)
      expect(models[1].resolutionUnitUri).toEqual('http://foo/unit/100')
      expect(models[1].resolutionUnitName).toEqual('°C')
      expect(models[1].aggregationTypeUri).toEqual('http://foo/aggregationtypes/2')
      expect(models[1].aggregationTypeName).toEqual('Mean')
      expect(models[1].description).toEqual('abc description')
    })
  })
  describe('#convertJsonApiObjectToModel', () => {
    it('should create the model from the json:api object', () => {
      const data = {
        data: {
          id: '123',
          type: 'device_property',
          attributes: {
            compartment_name: 'Climate',
            unit_uri: 'abc',
            sampling_media_name: 'Other',
            compartment_uri: 'variabletype/Climate',
            property_name: 'Water vapor concentration',
            accuracy: 0.1,
            accuracy_unit_uri: 'http://foo/unit/2',
            accuracy_unit_name: 'cm',
            measuring_range_min: 10,
            measuring_range_max: -10,
            label: 'water vapor',
            property_uri: 'variablename/Water%20vapor%20concentration',
            unit_name: '%',
            failure_value: -234,
            sampling_media_uri: 'medium/Other',
            resolution: 0.001,
            resolution_unit_uri: 'http://foo/unit/1',
            resolution_unit_name: 'mm',
            aggregation_type_uri: 'http://foo/aggregationtypes/3',
            aggregation_type_name: 'Mode',
            description: 'desc'
          },
          relationships: {}
        },
        included: []
      }
      const serializer = new DevicePropertySerializer()
      const model = serializer.convertJsonApiObjectToModel(data)

      expect(model.id).toEqual('123')
      expect(model.compartmentName).toEqual('Climate')
      expect(model.unitUri).toEqual('abc')
      expect(model.samplingMediaName).toEqual('Other')
      expect(model.compartmentUri).toEqual('variabletype/Climate')
      expect(model.propertyName).toEqual('Water vapor concentration')
      expect(model.accuracy).toEqual(0.1)
      expect(model.accuracyUnitUri).toEqual('http://foo/unit/2')
      expect(model.accuracyUnitName).toEqual('cm')
      expect(model.measuringRange.min).toEqual(10)
      expect(model.measuringRange.max).toEqual(-10)
      expect(model.label).toEqual('water vapor')
      expect(model.propertyUri).toEqual('variablename/Water%20vapor%20concentration')
      expect(model.unitName).toEqual('%')
      expect(model.failureValue).toEqual(-234)
      expect(model.samplingMediaUri).toEqual('medium/Other')
      expect(model.resolution).toEqual(0.001)
      expect(model.resolutionUnitUri).toEqual('http://foo/unit/1')
      expect(model.resolutionUnitName).toEqual('mm')
      expect(model.aggregationTypeUri).toEqual('http://foo/aggregationtypes/3')
      expect(model.aggregationTypeName).toEqual('Mode')
      expect(model.description).toEqual('desc')
    })
    it('should also fill the attributes with empty strings if missing', () => {
      const data = {
        data: {
          id: '123',
          type: 'device_property',
          attributes: {},
          relationships: {}
        },
        included: []
      }
      const serializer = new DevicePropertySerializer()
      const model = serializer.convertJsonApiObjectToModel(data)

      expect(model.id).toEqual('123')
      expect(model.compartmentName).toEqual('')
      expect(model.unitUri).toEqual('')
      expect(model.samplingMediaName).toEqual('')
      expect(model.compartmentUri).toEqual('')
      expect(model.propertyName).toEqual('')
      expect(model.accuracy).toEqual(null)
      expect(model.accuracyUnitUri).toEqual('')
      expect(model.accuracyUnitName).toEqual('')
      expect(model.measuringRange.min).toEqual(null)
      expect(model.measuringRange.max).toEqual(null)
      expect(model.label).toEqual('')
      expect(model.propertyUri).toEqual('')
      expect(model.unitName).toEqual('')
      expect(model.failureValue).toEqual(null)
      expect(model.samplingMediaUri).toEqual('')
      expect(model.resolution).toEqual(null)
      expect(model.resolutionUnitUri).toEqual('')
      expect(model.resolutionUnitName).toEqual('')
      expect(model.aggregationTypeUri).toEqual('')
      expect(model.aggregationTypeName).toEqual('')
      expect(model.description).toEqual('')
    })
    it('should handle non-numeric values as null', () => {
      const data = {
        data: {
          id: '123',
          type: 'device_property',
          attributes: {
            compartment_name: 'Climate',
            unit_uri: 'abc',
            sampling_media_name: 'Other',
            compartment_uri: 'variabletype/Climate',
            property_name: 'Water vapor concentration',
            accuracy: null,
            measuring_range_min: null,
            measuring_range_max: null,
            label: 'water vapor',
            property_uri: 'variablename/Water%20vapor%20concentration',
            unit_name: '%',
            failure_value: null,
            sampling_media_uri: 'medium/Other',
            resolution: null,
            resolution_unit_uri: 'http://foo/unit/1',
            resolution_unit_name: 'mm'
          },
          relationships: {}
        },
        included: []
      }
      const serializer = new DevicePropertySerializer()
      const model = serializer.convertJsonApiObjectToModel(data)

      expect(model.accuracy).toBeNull()
      expect(model.measuringRange.min).toBeNull()
      expect(model.measuringRange.max).toBeNull()
      expect(model.failureValue).toBeNull()
      expect(model.resolution).toBeNull()
    })
    it('should handle numeric 0 as 0', () => {
      const data = {
        data: {
          id: '123',
          type: 'device_property',
          attributes: {
            compartment_name: 'Climate',
            unit_uri: 'abc',
            sampling_media_name: 'Other',
            compartment_uri: 'variabletype/Climate',
            property_name: 'Water vapor concentration',
            accuracy: 0,
            measuring_range_min: 0,
            measuring_range_max: 0,
            label: 'water vapor',
            property_uri: 'variablename/Water%20vapor%20concentration',
            unit_name: '%',
            failure_value: 0,
            sampling_media_uri: 'medium/Other',
            resolution: 0,
            resolution_unit_uri: 'http://foo/unit/1',
            resolution_unit_name: 'mm'
          },
          relationships: {}
        },
        included: []
      }
      const serializer = new DevicePropertySerializer()
      const model = serializer.convertJsonApiObjectToModel(data)

      expect(model.accuracy).toBe(0)
      expect(model.measuringRange.min).toBe(0)
      expect(model.measuringRange.max).toBe(0)
      expect(model.failureValue).toBe(0)
      expect(model.resolution).toBe(0)
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should convert device property to a json:api payload', () => {
      const deviceProperty = DeviceProperty.createFromObject({
        id: '123',
        compartmentName: 'Climate',
        unitUri: 'abc',
        samplingMediaName: 'Other',
        compartmentUri: 'variabletype/Climate',
        propertyName: 'Water vapor concentration',
        accuracy: 0.1,
        accuracyUnitUri: 'http://foo/unit/2',
        accuracyUnitName: 'cm',
        measuringRange: MeasuringRange.createFromObject({
          min: 10,
          max: -10
        }),
        label: 'water vapor',
        propertyUri: 'variablename/Water%20vapor%20concentration',
        unitName: '%',
        failureValue: -234,
        samplingMediaUri: 'medium/Other',
        resolution: 0.001,
        resolutionUnitUri: 'http://foo/unit/1',
        resolutionUnitName: 'mm',
        aggregationTypeUri: 'http://foo/aggregationtypes/1',
        aggregationTypeName: 'Average',
        description: 'desc'
      })
      const serializer = new DevicePropertySerializer()
      const deviceId = '456'

      const jsonApiPayload = serializer.convertModelToJsonApiData(deviceProperty, deviceId)

      expect(jsonApiPayload).toHaveProperty('id')
      expect(jsonApiPayload.id).toEqual('123')
      expect(jsonApiPayload).toHaveProperty('type')
      expect(jsonApiPayload.type).toEqual('device_property')
      expect(jsonApiPayload).toHaveProperty('attributes')
      expect(jsonApiPayload.attributes).toHaveProperty('compartment_name')
      expect(jsonApiPayload.attributes.compartment_name).toEqual('Climate')
      expect(jsonApiPayload.attributes).toHaveProperty('unit_uri')
      expect(jsonApiPayload.attributes.unit_uri).toEqual('abc')
      expect(jsonApiPayload.attributes).toHaveProperty('sampling_media_name')
      expect(jsonApiPayload.attributes.sampling_media_name).toEqual('Other')
      expect(jsonApiPayload.attributes).toHaveProperty('compartment_uri')
      expect(jsonApiPayload.attributes.compartment_uri).toEqual('variabletype/Climate')
      expect(jsonApiPayload.attributes).toHaveProperty('property_name')
      expect(jsonApiPayload.attributes.property_name).toEqual('Water vapor concentration')
      expect(jsonApiPayload.attributes).toHaveProperty('accuracy')
      expect(jsonApiPayload.attributes.accuracy).toEqual(0.1)
      expect(jsonApiPayload.attributes).toHaveProperty('accuracy_unit_uri')
      expect(jsonApiPayload.attributes.accuracy_unit_uri).toEqual('http://foo/unit/2')
      expect(jsonApiPayload.attributes).toHaveProperty('accuracy_unit_name')
      expect(jsonApiPayload.attributes.accuracy_unit_name).toEqual('cm')
      expect(jsonApiPayload.attributes).toHaveProperty('measuring_range_min')
      expect(jsonApiPayload.attributes.measuring_range_min).toEqual(10)
      expect(jsonApiPayload.attributes).toHaveProperty('measuring_range_max')
      expect(jsonApiPayload.attributes.measuring_range_max).toEqual(-10)
      expect(jsonApiPayload.attributes).toHaveProperty('label')
      expect(jsonApiPayload.attributes.label).toEqual('water vapor')
      expect(jsonApiPayload.attributes).toHaveProperty('property_uri')
      expect(jsonApiPayload.attributes.property_uri).toEqual('variablename/Water%20vapor%20concentration')
      expect(jsonApiPayload.attributes).toHaveProperty('unit_name')
      expect(jsonApiPayload.attributes.unit_name).toEqual('%')
      expect(jsonApiPayload.attributes).toHaveProperty('failure_value')
      expect(jsonApiPayload.attributes.failure_value).toEqual(-234)
      expect(jsonApiPayload.attributes).toHaveProperty('sampling_media_uri')
      expect(jsonApiPayload.attributes.sampling_media_uri).toEqual('medium/Other')
      expect(jsonApiPayload.attributes).toHaveProperty('resolution')
      expect(jsonApiPayload.attributes.resolution).toEqual(0.001)
      expect(jsonApiPayload.attributes).toHaveProperty('resolution_unit_uri')
      expect(jsonApiPayload.attributes.resolution_unit_uri).toEqual('http://foo/unit/1')
      expect(jsonApiPayload.attributes).toHaveProperty('resolution_unit_name')
      expect(jsonApiPayload.attributes.resolution_unit_name).toEqual('mm')
      expect(jsonApiPayload.attributes).toHaveProperty('aggregation_type_uri')
      expect(jsonApiPayload.attributes.aggregation_type_uri).toEqual('http://foo/aggregationtypes/1')
      expect(jsonApiPayload.attributes).toHaveProperty('aggregation_type_name')
      expect(jsonApiPayload.attributes.aggregation_type_name).toEqual('Average')
      expect(jsonApiPayload.attributes).toHaveProperty('description')
      expect(jsonApiPayload.attributes.description).toEqual('desc')

      expect(jsonApiPayload).toHaveProperty('relationships')
      expect(jsonApiPayload.relationships).toHaveProperty('device')
      expect(jsonApiPayload.relationships?.device).toHaveProperty('data')
      const deviceData: any = jsonApiPayload.relationships?.device.data
      expect(deviceData).toHaveProperty('id')
      expect(deviceData.id).toEqual('456')
      expect(deviceData).toHaveProperty('type')
      expect(deviceData.type).toEqual('device')
    })
    it('should also work if we don\'t have an id yet', () => {
      const deviceProperty = DeviceProperty.createFromObject({
        id: null,
        compartmentName: 'Climate',
        unitUri: 'abc',
        samplingMediaName: 'Other',
        compartmentUri: 'variabletype/Climate',
        propertyName: 'Water vapor concentration',
        accuracy: 0.1,
        accuracyUnitUri: 'http://foo/unit/2',
        accuracyUnitName: 'cm',
        measuringRange: MeasuringRange.createFromObject({
          min: 10,
          max: -10
        }),
        label: 'water vapor',
        propertyUri: 'variablename/Water%20vapor%20concentration',
        unitName: '%',
        failureValue: -234,
        samplingMediaUri: 'medium/Other',
        resolution: 0.001,
        resolutionUnitUri: 'http://foo/unit/1',
        resolutionUnitName: 'mm',
        aggregationTypeUri: 'http://foo/aggregationtypes/4',
        aggregationTypeName: 'Sum',
        description: 'desc'
      })
      const serializer = new DevicePropertySerializer()
      const deviceId = '456'

      const jsonApiPayload = serializer.convertModelToJsonApiData(deviceProperty, deviceId)

      expect(jsonApiPayload).not.toHaveProperty('id')
      expect(jsonApiPayload).toHaveProperty('type')
      expect(jsonApiPayload.type).toEqual('device_property')
      expect(jsonApiPayload).toHaveProperty('attributes')
      expect(jsonApiPayload.attributes).toHaveProperty('compartment_name')
      expect(jsonApiPayload.attributes.compartment_name).toEqual('Climate')
      expect(jsonApiPayload.attributes).toHaveProperty('unit_uri')
      expect(jsonApiPayload.attributes.unit_uri).toEqual('abc')
      expect(jsonApiPayload.attributes).toHaveProperty('sampling_media_name')
      expect(jsonApiPayload.attributes.sampling_media_name).toEqual('Other')
      expect(jsonApiPayload.attributes).toHaveProperty('compartment_uri')
      expect(jsonApiPayload.attributes.compartment_uri).toEqual('variabletype/Climate')
      expect(jsonApiPayload.attributes).toHaveProperty('property_name')
      expect(jsonApiPayload.attributes.property_name).toEqual('Water vapor concentration')
      expect(jsonApiPayload.attributes).toHaveProperty('accuracy')
      expect(jsonApiPayload.attributes.accuracy).toEqual(0.1)
      expect(jsonApiPayload.attributes).toHaveProperty('accuracy_unit_uri')
      expect(jsonApiPayload.attributes.accuracy_unit_uri).toEqual('http://foo/unit/2')
      expect(jsonApiPayload.attributes).toHaveProperty('accuracy_unit_name')
      expect(jsonApiPayload.attributes.accuracy_unit_name).toEqual('cm')
      expect(jsonApiPayload.attributes).toHaveProperty('measuring_range_min')
      expect(jsonApiPayload.attributes.measuring_range_min).toEqual(10)
      expect(jsonApiPayload.attributes).toHaveProperty('measuring_range_max')
      expect(jsonApiPayload.attributes.measuring_range_max).toEqual(-10)
      expect(jsonApiPayload.attributes).toHaveProperty('label')
      expect(jsonApiPayload.attributes.label).toEqual('water vapor')
      expect(jsonApiPayload.attributes).toHaveProperty('property_uri')
      expect(jsonApiPayload.attributes.property_uri).toEqual('variablename/Water%20vapor%20concentration')
      expect(jsonApiPayload.attributes).toHaveProperty('unit_name')
      expect(jsonApiPayload.attributes.unit_name).toEqual('%')
      expect(jsonApiPayload.attributes).toHaveProperty('failure_value')
      expect(jsonApiPayload.attributes.failure_value).toEqual(-234)
      expect(jsonApiPayload.attributes).toHaveProperty('sampling_media_uri')
      expect(jsonApiPayload.attributes.sampling_media_uri).toEqual('medium/Other')
      expect(jsonApiPayload.attributes).toHaveProperty('resolution')
      expect(jsonApiPayload.attributes.resolution).toEqual(0.001)
      expect(jsonApiPayload.attributes).toHaveProperty('resolution_unit_uri')
      expect(jsonApiPayload.attributes.resolution_unit_uri).toEqual('http://foo/unit/1')
      expect(jsonApiPayload.attributes).toHaveProperty('resolution_unit_name')
      expect(jsonApiPayload.attributes.resolution_unit_name).toEqual('mm')
      expect(jsonApiPayload.attributes).toHaveProperty('aggregation_type_uri')
      expect(jsonApiPayload.attributes.aggregation_type_uri).toEqual('http://foo/aggregationtypes/4')
      expect(jsonApiPayload.attributes).toHaveProperty('aggregation_type_name')
      expect(jsonApiPayload.attributes.aggregation_type_name).toEqual('Sum')
      expect(jsonApiPayload.attributes).toHaveProperty('description')
      expect(jsonApiPayload.attributes.description).toEqual('desc')

      expect(jsonApiPayload).toHaveProperty('relationships')
      expect(jsonApiPayload.relationships).toHaveProperty('device')
      expect(jsonApiPayload.relationships?.device).toHaveProperty('data')
      const deviceData: any = jsonApiPayload.relationships?.device.data
      expect(deviceData).toHaveProperty('id')
      expect(deviceData.id).toEqual('456')
      expect(deviceData).toHaveProperty('type')
      expect(deviceData.type).toEqual('device')
    })
  })
})
