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
import { DeviceType } from '@/models/DeviceType'
import { DeviceTypeSerializer } from '@/serializers/jsonapi/DeviceTypeSerializer'

describe('DeviceTypeSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            category: 'Communications component',
            definition: 'An electrical device that converts electric power into radio waves and vice versa.',
            note: null,
            provenance: 'Definition adapted from Wikipedia. See http://en.wikipedia.org/wiki/Antenna_(radio)',
            provenance_uri: null,
            status: 'Accepted',
            term: 'Antenna'
          },
          id: '1',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/equipmenttypes/1/'
          },
          relationships: {
            global_provenence: {
              data: null
            }
          },
          type: 'EquipmentType'
        }, {
          attributes: {
            category: 'Instrument',
            definition: 'A survey level that makes use of a compensator that ensures the line of sight remains horizontal once the operator has roughly leveled the instrument.',
            note: 'simple note',
            provenance: 'Definition adapted from Wikipedia. See http://en.wikipedia.org/wiki/Levelling',
            provenance_uri: 'abc',
            status: 'Accepted',
            term: 'AutomaticLevel'
          },
          id: '2',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/equipmenttypes/2/'
          },
          relationships: {
            global_provenance: {
              data: {
                id: '1',
                type: 'GlobalProvenance'
              }
            }
          },
          type: 'EquipmentType'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedDeviceType1 = DeviceType.createFromObject({
        id: '1',
        name: 'Antenna',
        definition: 'An electrical device that converts electric power into radio waves and vice versa.',
        provenance: 'Definition adapted from Wikipedia. See http://en.wikipedia.org/wiki/Antenna_(radio)',
        provenanceUri: '',
        note: '',
        category: 'Communications component',
        globalProvenanceId: null,
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/equipmenttypes/1/'

      })
      const expectedDeviceType2 = DeviceType.createFromObject({
        id: '2',
        name: 'AutomaticLevel',
        category: 'Instrument',
        definition: 'A survey level that makes use of a compensator that ensures the line of sight remains horizontal once the operator has roughly leveled the instrument.',
        provenance: 'Definition adapted from Wikipedia. See http://en.wikipedia.org/wiki/Levelling',
        provenanceUri: 'abc',
        note: 'simple note',
        globalProvenanceId: '1',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/equipmenttypes/2/'
      })

      const serializer = new DeviceTypeSerializer()

      const deviceTypes = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(deviceTypes)).toBeTruthy()
      expect(deviceTypes.length).toEqual(2)
      expect(deviceTypes[0]).toEqual(expectedDeviceType1)
      expect(deviceTypes[1]).toEqual(expectedDeviceType2)
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should transform the model to json payload', () => {
      const deviceType = DeviceType.createFromObject({
        id: '2',
        name: 'AutomaticLevel',
        category: 'Instrument',
        definition: 'A survey level that makes use of a compensator that ensures the line of sight remains horizontal once the operator has roughly leveled the instrument.',
        provenance: 'Definition adapted from Wikipedia. See http://en.wikipedia.org/wiki/Levelling',
        provenanceUri: 'abc',
        note: 'simple note',
        globalProvenanceId: '1',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/equipmenttypes/2/'
      })

      const expectedResult = {
        id: '2',
        type: 'EquipmentType',
        attributes: {
          term: 'AutomaticLevel',
          category: 'Instrument',
          definition: 'A survey level that makes use of a compensator that ensures the line of sight remains horizontal once the operator has roughly leveled the instrument.',
          provenance: 'Definition adapted from Wikipedia. See http://en.wikipedia.org/wiki/Levelling',
          provenance_uri: 'abc',
          note: 'simple note'
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

      const serializer = new DeviceTypeSerializer()
      const result = serializer.convertModelToJsonApiData(deviceType)

      expect(result).toEqual(expectedResult)
    })
  })
})
