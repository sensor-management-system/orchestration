import { Status } from '@/models/Status'
import { StatusSerializer } from '@/serializers/jsonapi/StatusSerializer'

describe('StatusSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            active: true,
            category: null,
            definition: 'Data collection is complete. No new data values will be added.',
            name: 'Complete',
            note: null,
            provenance: null,
            provenance_uri: null,
            term: 'complete'
          },
          id: 'Complete',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/status/Complete/'
          },
          relationships: {},
          type: 'Status'
        }, {
          attributes: {
            active: true,
            category: null,
            definition: 'Data collection is ongoing.  New data values will be added periodically.',
            name: 'Ongoing...',
            note: null,
            provenance: null,
            provenance_uri: null,
            term: 'ongoing'
          },
          id: 'Ongoing',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/status/Ongoing/'
          },
          relationships: {},
          type: 'Status'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedStatus1 = Status.createFromObject({
        id: 'Complete',
        name: 'Complete',
        uri: 'status/Complete'
      })
      const expectedStatus2 = Status.createFromObject({
        id: 'Ongoing',
        name: 'Ongoing...',
        uri: 'status/Ongoing'
      })

      const serializer = new StatusSerializer('http://rz-vm64.gfz-potsdam.de:5001/api')

      const states = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(states)).toBeTruthy()
      expect(states.length).toEqual(2)
      expect(states[0]).toEqual(expectedStatus1)
      expect(states[1]).toEqual(expectedStatus2)
    })
  })
})
