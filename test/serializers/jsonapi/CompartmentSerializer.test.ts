/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2022
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
            category: null,
            definition: 'Variables associated with age',
            note: null,
            provenance: 'Originally from PetDB. Syntax modified to remove underscores.',
            provenance_uri: null,
            status: 'ACCEPTED',
            term: 'Age'
          },
          id: '1',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/compartments/1/'
          },
          relationships: {
            global_provenence: {
              data: null
            }
          },
          type: 'Compartment'
        }, {
          attributes: {
            category: 'category',
            definition: 'Variables associated with biological organisms',
            note: 'note',
            provenance: 'Originally from CUAHSI HIS GeneralCategoryCV. See http://his.cuahsi.org/mastercvreg/edit_cv11.aspx?tbl=GeneralCategoryCV.',
            provenance_uri: 'uri',
            status: 'ACCEPTED',
            term: 'Biota'
          },
          id: '2',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/compartments/2/'
          },
          relationships: {
            global_provenance: {
              data: {
                id: '1',
                type: 'GlobalProvenance'
              }
            }
          },
          type: 'Compartment'
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
        id: '1',
        name: 'Age',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/compartments/1/',
        definition: 'Variables associated with age',
        category: '',
        note: '',
        provenance: 'Originally from PetDB. Syntax modified to remove underscores.',
        provenanceUri: '',
        globalProvenanceId: null
      })
      const expectedCompartment2 = Compartment.createFromObject({
        id: '2',
        name: 'Biota',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/compartments/2/',
        definition: 'Variables associated with biological organisms',
        category: 'category',
        note: 'note',
        provenance: 'Originally from CUAHSI HIS GeneralCategoryCV. See http://his.cuahsi.org/mastercvreg/edit_cv11.aspx?tbl=GeneralCategoryCV.',
        provenanceUri: 'uri',
        globalProvenanceId: '1'
      })

      const serializer = new CompartmentSerializer()

      const compartments = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(compartments)).toBeTruthy()
      expect(compartments.length).toEqual(2)
      expect(compartments[0]).toEqual(expectedCompartment1)
      expect(compartments[1]).toEqual(expectedCompartment2)
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should transform the model to json payload', () => {
      const compartment = Compartment.createFromObject({
        id: '2',
        name: 'Biota',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/compartments/2/',
        definition: 'Variables associated with biological organisms',
        category: 'category',
        note: 'note',
        provenance: 'Originally from CUAHSI HIS GeneralCategoryCV. See http://his.cuahsi.org/mastercvreg/edit_cv11.aspx?tbl=GeneralCategoryCV.',
        provenanceUri: 'uri',
        globalProvenanceId: '1'
      })

      const expectedResult = {
        id: '2',
        type: 'Compartment',
        attributes: {
          term: 'Biota',
          definition: 'Variables associated with biological organisms',
          category: 'category',
          note: 'note',
          provenance: 'Originally from CUAHSI HIS GeneralCategoryCV. See http://his.cuahsi.org/mastercvreg/edit_cv11.aspx?tbl=GeneralCategoryCV.',
          provenance_uri: 'uri'
        },
        relationships: {
          global_provenance: {
            data: {
              id: '1',
              type: 'GlobalProvenance'
            }
          }
        }
      }

      const serializer = new CompartmentSerializer()
      const result = serializer.convertModelToJsonApiData(compartment)

      expect(result).toEqual(expectedResult)
    })
  })
})
