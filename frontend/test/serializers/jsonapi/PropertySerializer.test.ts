/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { Property } from '@/models/Property'
import { PropertySerializer } from '@/serializers/jsonapi/PropertySerializer'

describe('PropertySerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            category: null,
            definition: 'Snow layers within the snowpack are a record of the winter’s weather. Like tree rings or strata of rock, layers can be traced to dates and conditions that formed them. One of the most important characteristics of a layer is its hardness. Harder snow is stronger and cohesive, while softer snow is weaker. ',
            note: 'Added to support Critical Zone Observatory (CZO) data use cases. ',
            provenance: null,
            provenance_uri: 'http://cbavalanchecenter.org/interpreting-snowpack-layers-and-hardness/',
            status: 'Accepted',
            term: 'Snow Layer Hardness'
          },
          id: '1',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/measuredquantities/1/'
          },
          relationships: {
            sampling_media: {
              data: {
                type: 'SamplingMedium',
                id: '5'
              }
            },
            global_provenance: {
              data: null
            },
            aggregation_type: {
              data: {
                type: 'AggregationType',
                id: '1'
              }
            }
          },
          type: 'MeasuredQuantity'
        }, {
          attributes: {
            category: 'cat',
            definition: 'The depth of water if a snow cover is completely melted, expressed in units of depth, on a corresponding horizontal surface area.',
            note: 'note',
            provenance: 'Originally from the CUAHSI HIS VariableNameCV.  See: http://his.cuahsi.org/mastercvreg/edit_cv11.aspx?tbl=VariableNameCV.',
            provenance_uri: 'uri',
            status: 'Accepted',
            term: 'Snow Water Equivalent'
          },
          id: '2',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/measuredquantities/2/'
          },
          relationships: {
            sampling_media: {
              data: {
                type: 'SamplingMedium',
                id: '2'
              }
            },
            global_provenance: {
              data: {
                id: '1',
                type: 'GlobalProvenance'
              }
            },
            aggregation_type: {
              data: {
                type: 'AggregationType',
                id: '2'
              }
            }
          },
          type: 'MeasuredQuantity'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedProperty1 = Property.createFromObject({
        id: '1',
        name: 'Snow Layer Hardness',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/measuredquantities/1/',
        definition: 'Snow layers within the snowpack are a record of the winter’s weather. Like tree rings or strata of rock, layers can be traced to dates and conditions that formed them. One of the most important characteristics of a layer is its hardness. Harder snow is stronger and cohesive, while softer snow is weaker. ',
        samplingMediaId: '5',
        note: 'Added to support Critical Zone Observatory (CZO) data use cases. ',
        category: '',
        provenance: '',
        provenanceUri: 'http://cbavalanchecenter.org/interpreting-snowpack-layers-and-hardness/',
        globalProvenanceId: null,
        aggregationTypeId: '1'
      })
      const expectedProperty2 = Property.createFromObject({
        id: '2',
        name: 'Snow Water Equivalent',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/measuredquantities/2/',
        definition: 'The depth of water if a snow cover is completely melted, expressed in units of depth, on a corresponding horizontal surface area.',
        samplingMediaId: '2',
        category: 'cat',
        note: 'note',
        provenance: 'Originally from the CUAHSI HIS VariableNameCV.  See: http://his.cuahsi.org/mastercvreg/edit_cv11.aspx?tbl=VariableNameCV.',
        provenanceUri: 'uri',
        globalProvenanceId: '1',
        aggregationTypeId: '2'
      })

      const serializer = new PropertySerializer()

      const properties = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(properties)).toBeTruthy()
      expect(properties.length).toEqual(2)
      expect(properties[0]).toEqual(expectedProperty1)
      expect(properties[1]).toEqual(expectedProperty2)
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should transform the model to json payload', () => {
      const cvProperty = Property.createFromObject({
        id: '2',
        name: 'Snow Water Equivalent',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/measuredquantities/2/',
        definition: 'The depth of water if a snow cover is completely melted, expressed in units of depth, on a corresponding horizontal surface area.',
        samplingMediaId: '2',
        category: 'cat',
        note: 'note',
        provenance: 'Originally from the CUAHSI HIS VariableNameCV.  See: http://his.cuahsi.org/mastercvreg/edit_cv11.aspx?tbl=VariableNameCV.',
        provenanceUri: 'uri',
        globalProvenanceId: '1',
        aggregationTypeId: '2'
      })

      const expectedResult = {
        attributes: {
          category: 'cat',
          definition: 'The depth of water if a snow cover is completely melted, expressed in units of depth, on a corresponding horizontal surface area.',
          note: 'note',
          provenance: 'Originally from the CUAHSI HIS VariableNameCV.  See: http://his.cuahsi.org/mastercvreg/edit_cv11.aspx?tbl=VariableNameCV.',
          provenance_uri: 'uri',
          term: 'Snow Water Equivalent'
        },
        id: '2',
        relationships: {
          sampling_media: {
            data: {
              type: 'SamplingMedium',
              id: '2'
            }
          },
          global_provenance: {
            data: {
              id: '1',
              type: 'GlobalProvenance'
            }
          },
          aggregation_type: {
            data: {
              type: 'AggregationType',
              id: '2'
            }
          }
        },
        type: 'MeasuredQuantity'
      }

      const serializer = new PropertySerializer()
      const result = serializer.convertModelToJsonApiData(cvProperty)

      expect(result).toEqual(expectedResult)
    })
  })
})
