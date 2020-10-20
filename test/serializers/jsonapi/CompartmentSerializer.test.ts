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
import { Compartment } from '@/models/Compartment'
import { CompartmentSerializer } from '@/serializers/jsonapi/CompartmentSerializer'

describe('CompartmentSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            active: true,
            category: null,
            definition: 'Variables associated with age',
            name: 'Age',
            note: null,
            provenance: 'Originally from PetDB. Syntax modified to remove underscores.',
            provenance_uri: null,
            term: 'age'
          },
          id: 'Age',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/variabletype/Age/'
          },
          relationships: {},
          type: 'Variabletype'
        }, {
          attributes: {
            active: true,
            category: null,
            definition: 'Variables associated with biological organisms',
            name: 'Biota...',
            note: null,
            provenance: 'Originally from CUAHSI HIS GeneralCategoryCV. See http://his.cuahsi.org/mastercvreg/edit_cv11.aspx?tbl=GeneralCategoryCV.',
            provenance_uri: null,
            term: 'Biota'
          },
          id: 'Biota',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/variabletype/Biota/'
          },
          relationships: {},
          type: 'Variabletype'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedCompartment1 = Compartment.createFromObject({
        id: 'Age',
        name: 'Age',
        uri: 'variabletype/Age'
      })
      const expectedCompartment2 = Compartment.createFromObject({
        id: 'Biota',
        name: 'Biota...',
        uri: 'variabletype/Biota'
      })

      const serializer = new CompartmentSerializer('http://rz-vm64.gfz-potsdam.de:5001/api')

      const compartments = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(compartments)).toBeTruthy()
      expect(compartments.length).toEqual(2)
      expect(compartments[0]).toEqual(expectedCompartment1)
      expect(compartments[1]).toEqual(expectedCompartment2)
    })
  })
})
