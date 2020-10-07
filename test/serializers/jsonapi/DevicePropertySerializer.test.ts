import {
  DeviceProperty
} from '@/models/DeviceProperty'
import {
  MeasuringRange
} from '@/models/MeasuringRange'

import DevicePropertySerializer from '@/serializers/jsonapi/DevicePropertySerializer'

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
})
