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
