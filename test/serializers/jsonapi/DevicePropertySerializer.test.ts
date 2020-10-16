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
import { DeviceProperty } from '@/models/DeviceProperty'
import { MeasuringRange } from '@/models/MeasuringRange'

import { DevicePropertySerializer } from '@/serializers/jsonapi/DevicePropertySerializer'

describe('DevicePropertySerializer', () => {
  describe('#convertNestedJsonApiToModelList', () => {
    it('should convert a list of entries', () => {
      const jsonApiElements = [{
        compartment_name: 'Climate',
        unit_uri: '',
        sampling_media_name: 'Other',
        compartment_uri: 'variabletype/Climate',
        property_name: 'Water vapor concentration',
        accuracy: null,
        measuring_range_min: null,
        measuring_range_max: null,
        label: 'water vapor',
        property_uri: 'variablename/Water%20vapor%20concentration',
        id: '39',
        unit_name: '',
        failure_value: null,
        sampling_media_uri: 'medium/Other'
      }, {
        compartment_name: 'a',
        unit_uri: 'b',
        sampling_media_name: 'c',
        compartment_uri: 'd',
        property_name: 'e',
        accuracy: 1,
        measuring_range_min: 2,
        measuring_range_max: 3,
        label: 'f',
        property_uri: 'g',
        id: '40',
        unit_name: 'j',
        failure_value: 4,
        sampling_media_uri: 'k'
      }]

      const expectedProperty1 = DeviceProperty.createFromObject({
        compartmentName: 'Climate',
        unitUri: '',
        samplingMediaName: 'Other',
        compartmentUri: 'variabletype/Climate',
        propertyName: 'Water vapor concentration',
        accuracy: null,
        measuringRange: MeasuringRange.createFromObject({
          min: null,
          max: null
        }),
        label: 'water vapor',
        propertyUri: 'variablename/Water%20vapor%20concentration',
        id: '39',
        unitName: '',
        failureValue: null,
        samplingMediaUri: 'medium/Other'
      })

      const expectedProperty2 = DeviceProperty.createFromObject({
        compartmentName: 'a',
        unitUri: 'b',
        samplingMediaName: 'c',
        compartmentUri: 'd',
        propertyName: 'e',
        accuracy: 1,
        measuringRange: MeasuringRange.createFromObject({
          min: 2,
          max: 3
        }),
        label: 'f',
        propertyUri: 'g',
        id: '40',
        unitName: 'j',
        failureValue: 4,
        samplingMediaUri: 'k'
      })

      const serializer = new DevicePropertySerializer()

      const properties = serializer.convertNestedJsonApiToModelList(jsonApiElements)

      expect(Array.isArray(properties)).toBeTruthy()
      expect(properties.length).toEqual(2)
      expect(properties[0]).toEqual(expectedProperty1)
      expect(properties[1]).toEqual(expectedProperty2)
    })
  })
  describe('#convertJsonApiElementToModel', () => {
    it('should convert a element', () => {
      const jsonApiElement = {
        compartment_name: 'Climate',
        unit_uri: '',
        sampling_media_name: 'Other',
        compartment_uri: 'variabletype/Climate',
        property_name: 'Water vapor concentration',
        accuracy: null,
        measuring_range_min: null,
        measuring_range_max: null,
        label: 'water vapor',
        property_uri: 'variablename/Water%20vapor%20concentration',
        id: '39',
        unit_name: '',
        failure_value: null,
        sampling_media_uri: 'medium/Other'
      }

      const expectedProperty = DeviceProperty.createFromObject({
        compartmentName: 'Climate',
        unitUri: '',
        samplingMediaName: 'Other',
        compartmentUri: 'variabletype/Climate',
        propertyName: 'Water vapor concentration',
        accuracy: null,
        measuringRange: MeasuringRange.createFromObject({
          min: null,
          max: null
        }),
        label: 'water vapor',
        propertyUri: 'variablename/Water%20vapor%20concentration',
        id: '39',
        unitName: '',
        failureValue: null,
        samplingMediaUri: 'medium/Other'
      })
      const serializer = new DevicePropertySerializer()

      const property = serializer.convertJsonApiElementToModel(jsonApiElement)

      expect(property).toEqual(expectedProperty)
    })
  })
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
          failureValue: -999
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
          failureValue: null
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
        failure_value: -999
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
        failure_value: null
      })
    })
  })
})
