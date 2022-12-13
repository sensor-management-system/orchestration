/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020, 2021
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
import { ActionType } from '@/models/ActionType'
import { ActionTypeSerializer } from '@/serializers/jsonapi/ActionTypeSerializer'

describe('ActionTypeSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a list of two elements to a model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          attributes: {
            term: 'Configuration Maintenance',
            definition: 'A configuration (i.e. station) is maintained (i.e. check of functionality). configurationMaintenance actions can be followed by platformMaintenance or deviveMaintenance actions to be explicit.',
            provenance: null,
            provenance_uri: null,
            category: null,
            note: null,
            status: 'ACCEPTED'
          },
          id: '8',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/actiontypes/8/'
          },
          relationships: {
            global_provenance: {
              data: null
            },
            action_category: {
              data: {
                id: '1',
                type: 'ActionCategory'
              }
            }
          },
          type: 'ActionType'
        }, {
          attributes: {
            term: 'Configuration Observation',
            definition: 'An observation is made at configuration level (i.e. station is covered by leafs). configurationObservation actions can be followed by platformObservation or deviveObservation actions to be explicit.',
            provenance: 'prov',
            provenance_uri: 'uri',
            category: 'cat',
            note: 'note',
            status: 'ACCEPTED'
          },
          id: '9',
          links: {
            self: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/actiontypes/9/'
          },
          relationships: {
            global_provenance: {
              data: {
                id: '1',
                type: 'GlobalProvenance'
              }
            },
            action_category: {
              data: {
                id: '2',
                type: 'ActionCategory'
              }
            }
          },
          type: 'ActionType'
        }],
        included: [],
        jsonapi: {
          version: '1.0'
        },
        meta: {
          count: 2
        }
      }

      const expectedActionType1 = ActionType.createFromObject({
        id: '8',
        name: 'Configuration Maintenance',
        definition: 'A configuration (i.e. station) is maintained (i.e. check of functionality). configurationMaintenance actions can be followed by platformMaintenance or deviveMaintenance actions to be explicit.',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/actiontypes/8/',
        provenance: '',
        provenanceUri: '',
        category: '',
        note: '',
        globalProvenanceId: null,
        actionCategoryId: '1'
      })
      const expectedActionType2 = ActionType.createFromObject({
        id: '9',
        name: 'Configuration Observation',
        definition: 'An observation is made at configuration level (i.e. station is covered by leafs). configurationObservation actions can be followed by platformObservation or deviveObservation actions to be explicit.',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/actiontypes/9/',
        provenance: 'prov',
        provenanceUri: 'uri',
        category: 'cat',
        note: 'note',
        globalProvenanceId: '1',
        actionCategoryId: '2'
      })

      const serializer = new ActionTypeSerializer()

      const actiontypes = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(actiontypes)).toBeTruthy()
      expect(actiontypes.length).toEqual(2)
      expect(actiontypes[0]).toEqual(expectedActionType1)
      expect(actiontypes[1]).toEqual(expectedActionType2)
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should transform the model to json payload', () => {
      const actionType = ActionType.createFromObject({
        id: '9',
        name: 'Configuration Observation',
        definition: 'An observation is made at configuration level (i.e. station is covered by leafs). configurationObservation actions can be followed by platformObservation or deviveObservation actions to be explicit.',
        uri: 'http://rz-vm64.gfz-potsdam.de:5001/api/v1/actiontypes/9/',
        provenance: 'prov',
        provenanceUri: 'uri',
        category: 'cat',
        note: 'note',
        globalProvenanceId: '1',
        actionCategoryId: '2'
      })

      const expectedResult = {
        attributes: {
          term: 'Configuration Observation',
          definition: 'An observation is made at configuration level (i.e. station is covered by leafs). configurationObservation actions can be followed by platformObservation or deviveObservation actions to be explicit.',
          provenance: 'prov',
          provenance_uri: 'uri',
          category: 'cat',
          note: 'note'
        },
        id: '9',
        type: 'ActionType',
        relationships: {
          global_provenance: {
            data: {
              id: '1',
              type: 'GlobalProvenance'
            }
          },
          action_category: {
            data: {
              id: '2',
              type: 'ActionCategory'
            }
          }
        }
      }

      const serializer = new ActionTypeSerializer()
      const result = serializer.convertModelToJsonApiData(actionType)

      expect(result).toEqual(expectedResult)
    })
  })
})
