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
import Property from '@/models/Property'
import { PropertySerializer } from '@/serializers/jsonapi/PropertySerializer'

describe('PropertySerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            active: true,
            category: null,
            definition: 'Snow layers within the snowpack are a record of the winter’s weather. Like tree rings or strata of rock, layers can be traced to dates and conditions that formed them. One of the most important characteristics of a layer is its hardness. Harder snow is stronger and cohesive, while softer snow is weaker. ',
            name: 'Snow layer hardness',
            note: 'Added to support Critical Zone Observatory (CZO) data use cases. ',
            provenance: null,
            provenance_uri: 'http://cbavalanchecenter.org/interpreting-snowpack-layers-and-hardness/',
            term: 'snowLayerHardness'
          },
          id: 'Snow layer hardness',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/variablename/Snow%20layer%20hardness/'
          },
          relationships: {},
          type: 'Variablename'
        }, {
          attributes: {
            active: true,
            category: null,
            definition: 'The depth of water if a snow cover is completely melted, expressed in units of depth, on a corresponding horizontal surface area.',
            name: 'Snow water equivalent...',
            note: null,
            provenance: 'Originally from the CUAHSI HIS VariableNameCV.  See: http://his.cuahsi.org/mastercvreg/edit_cv11.aspx?tbl=VariableNameCV.',
            provenance_uri: null,
            term: 'snowWaterEquivalent'
          },
          id: 'Snow water equivalent',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/variablename/Snow%20water%20equivalent/'
          },
          relationships: {},
          type: 'Variablename'
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
        id: 'Snow layer hardness',
        name: 'Snow layer hardness',
        uri: 'variablename/Snow%20layer%20hardness'
      })
      const expectedProperty2 = Property.createFromObject({
        id: 'Snow water equivalent',
        name: 'Snow water equivalent...',
        uri: 'variablename/Snow%20water%20equivalent'
      })

      const serializer = new PropertySerializer('http://rz-vm64.gfz-potsdam.de:5001/api')

      const properties = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(properties)).toBeTruthy()
      expect(properties.length).toEqual(2)
      expect(properties[0]).toEqual(expectedProperty1)
      expect(properties[1]).toEqual(expectedProperty2)
    })
  })
})
