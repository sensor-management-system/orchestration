import Manufacturer from '@/models/Manufacturer'
import ManufacturerSerializer from '@/serializers/jsonapi/ManufacturerSerializer'

describe('ManufacturerSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            active: true,
            category: null,
            definition: 'ecoTech Umwelt-Meßsysteme GmbH',
            name: 'Ecotech',
            note: null,
            provenance: null,
            provenance_uri: null,
            term: 'ecotech'
          },
          id: 'Ecotech',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/manufacturer/Ecotech/'
          },
          relationships: {},
          type: 'Manufacturer'
        }, {
          attributes: {
            active: true,
            category: null,
            definition: 'Campbell Scientific Ltd.',
            name: 'Campbell ++',
            note: null,
            provenance: null,
            provenance_uri: null,
            term: 'campbell'
          },
          id: 'Campbell',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/manufacturer/Campbell/'
          },
          relationships: {},
          type: 'Manufacturer'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedManufacturer1 = Manufacturer.createFromObject({
        id: 'Ecotech',
        name: 'Ecotech',
        uri: 'manufacturer/Ecotech'
      })
      const expectedManufacturer2 = Manufacturer.createFromObject({
        id: 'Campbell',
        name: 'Campbell ++',
        uri: 'manufacturer/Campbell'
      })

      const serializer = new ManufacturerSerializer('http://rz-vm64.gfz-potsdam.de:5001/api')

      const manufacturers = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(manufacturers)).toBeTruthy()
      expect(manufacturers.length).toEqual(2)
      expect(manufacturers[0]).toEqual(expectedManufacturer1)
      expect(manufacturers[1]).toEqual(expectedManufacturer2)
    })
  })
})
