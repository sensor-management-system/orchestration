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
