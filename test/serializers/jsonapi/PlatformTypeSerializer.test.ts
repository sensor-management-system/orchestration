import { PlatformType } from '@/models/PlatformType'
import { PlatformTypeSerializer } from '@/serializers/jsonapi/PlatformTypeSerializer'

describe('PlatformTypeSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            active: true,
            category: null,
            definition: null,
            name: 'Station',
            note: null,
            provenance: null,
            provenance_uri: null,
            term: 'station'
          },
          id: 'Station',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/platformtype/Station/'
          },
          relationships: {},
          type: 'Platformtype'
        }, {
          attributes: {
            active: true,
            category: null,
            definition: null,
            name: 'Drone +',
            note: null,
            provenance: null,
            provenance_uri: null,
            term: 'drone'
          },
          id: 'Drone',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/platformtype/Drone/'
          },
          relationships: {},
          type: 'Platformtype'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedPlatformType1 = PlatformType.createFromObject({
        id: 'Station',
        name: 'Station',
        uri: 'platformtype/Station'
      })
      const expectedPlatformType2 = PlatformType.createFromObject({
        id: 'Drone',
        name: 'Drone +',
        uri: 'platformtype/Drone'
      })

      const serializer = new PlatformTypeSerializer('http://rz-vm64.gfz-potsdam.de:5001/api')

      const platformTypes = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(platformTypes)).toBeTruthy()
      expect(platformTypes.length).toEqual(2)
      expect(platformTypes[0]).toEqual(expectedPlatformType1)
      expect(platformTypes[1]).toEqual(expectedPlatformType2)
    })
  })
})
