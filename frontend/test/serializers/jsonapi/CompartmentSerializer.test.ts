/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2022
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
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
