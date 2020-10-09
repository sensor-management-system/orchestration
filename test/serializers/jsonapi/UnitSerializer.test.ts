import Unit from '@/models/Unit'
import UnitSerializer from '@/serializers/jsonapi/UnitSerializer'

describe('UnitSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            active: true,
            term: 'gray',
            unitsabbreviation: 'Gy',
            unitslink: 'http://qudt.org/vocab/unit#Gray; http://unitsofmeasure.org/ucum.html#para-30',
            unitsname: 'Gray',
            unitstypecv: 'Absorbed dose'
          },
          id: 'Gray',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/unit/Gray/'
          },
          relationships: {
            unitstype: {
              data: null,
              links: {
                self: 'http://rz-vm64.gfz-potsdam.de:5001/api/unit/Gray/unitstype'
              }
            }
          },
          type: 'Unit'
        },
        {
          attributes: {
            active: true,
            term: 'rad',
            unitsabbreviation: '',
            unitslink: 'http://qudt.org/vocab/unit#Rad; http://unitsofmeasure.org/ucum.html#para-33',
            unitsname: 'RAD',
            unitstypecv: 'Absorbed dose'
          },
          id: 'RAD',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/unit/RAD/'
          },
          relationships: {
            unitstype: {
              data: null,
              links: {
                self: 'http://rz-vm64.gfz-potsdam.de:5001/api/unit/RAD/unitstype'
              }
            }
          },
          type: 'Unit'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedUnit1 = Unit.createFromObject({
        id: 'Gray',
        name: 'Gray [Gy]',
        uri: 'unit/Gray'
      })

      const expectedUnit2 = Unit.createFromObject({
        id: 'RAD',
        name: 'RAD',
        uri: 'unit/RAD'
      })

      const serializer = new UnitSerializer('http://rz-vm64.gfz-potsdam.de:5001/api')

      const units = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(units)).toBeTruthy()
      expect(units.length).toEqual(2)
      expect(units[0]).toEqual(expectedUnit1)
      expect(units[1]).toEqual(expectedUnit2)
    })
  })
})
