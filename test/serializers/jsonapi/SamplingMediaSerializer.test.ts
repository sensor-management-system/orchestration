import SamplingMedia from '@/models/SamplingMedia'
import SamplingMediaSerializer from '@/serializers/jsonapi/SamplingMediaSerializer'

describe('SamplingMediaSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            active: true,
            category: null,
            definition: 'Specimen collection of ambient air or sensor emplaced to measure properties of ambient air.',
            name: 'Air',
            note: null,
            provenance: null,
            provenance_uri: null,
            term: 'air'
          },
          id: 'Air',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/medium/Air/'
          },
          relationships: {},
          type: 'Medium'
        }, {
          attributes: {
            active: true,
            category: null,
            definition: 'An instrument, sensor or other piece of human-made equipment upon which a measurement is made, such as datalogger temperature or battery voltage.',
            name: 'Equipment++',
            note: null,
            provenance: null,
            provenance_uri: null,
            term: 'equipment'
          },
          id: 'Equipment',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/medium/Equipment/'
          },
          relationships: {},
          type: 'Medium'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedSamplingMedium1 = SamplingMedia.createFromObject({
        id: 'Air',
        name: 'Air',
        uri: 'medium/Air'
      })
      const expectedSamplingMedium2 = SamplingMedia.createFromObject({
        id: 'Equipment',
        name: 'Equipment++',
        uri: 'medium/Equipment'
      })

      const serializer = new SamplingMediaSerializer('http://rz-vm64.gfz-potsdam.de:5001/api')

      const samplingMedia = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(samplingMedia)).toBeTruthy()
      expect(samplingMedia.length).toEqual(2)
      expect(samplingMedia[0]).toEqual(expectedSamplingMedium1)
      expect(samplingMedia[1]).toEqual(expectedSamplingMedium2)
    })
  })
})
