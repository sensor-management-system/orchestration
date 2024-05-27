/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { DateTime } from 'luxon'

import { Contact } from '@/models/Contact'
import { ParameterChangeAction } from '@/models/ParameterChangeAction'

import {
  ParameterChangeActionEntityType,
  ParameterChangeActionRelationEntityType,
  IParameterChangeActionRelation,
  ParameterChangeActionSerializer
} from '@/serializers/jsonapi/ParameterChangeActionSerializer'

import {
  IJsonApiEntityEnvelope,
  IJsonApiEntityListEnvelope,
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiRelationships
} from '@/serializers/jsonapi/JsonApiTypes'

describe('ParameterChangeActionSerializer', () => {
  describe('#convertJsonApiDataToModel', () => {
    it('should convert an example payload to a model', () => {
      const data: IJsonApiEntityWithOptionalAttributes = {
        id: '2',
        type: 'device_parameter_value_change_action',
        attributes: {
          description: 'value change',
          value: '20',
          date: '2023-07-01T10:05:15.194629+00:00',
          created_at: '2023-07-14T11:07:31.194629+00:00',
          updated_at: '2023-07-14T11:47:01.636331+00:00'
        },
        relationships: {
          created_by: {
            data: {
              type: 'user',
              id: '9'
            }
          },
          updated_by: {
            data: {
              type: 'user',
              id: '9'
            }
          },
          contact: {
            data: {
              type: 'contact',
              id: '1'
            }
          },
          device_parameter: {
            data: {
              type: 'device_parameter',
              id: '1'
            }
          }
        }
      }

      const included: IJsonApiEntityWithOptionalAttributes[] = [
        {
          type: 'user',
          id: '9',
          attributes: {
            subject: 'contact@example.com'
          },
          relationships: {
            contact: {
              data: {
                type: 'contact',
                id: '1'
              }
            }
          }
        },
        {
          type: 'contact',
          id: '1',
          attributes: {
            active: true,
            email: 'contact@example.com',
            family_name: 'Example',
            given_name: 'Eric',
            orcid: null,
            organization: 'example.com',
            website: 'http://example.com'
          }
        },
        {
          type: 'device_parameter',
          id: '1',
          attributes: {
            label: 'Parameter 1',
            description: 'Unit description',
            unit_name: 'Unit 1',
            unit_uri: 'http://example.com/unit1'
          }
        }
      ]

      const serializer = new ParameterChangeActionSerializer(ParameterChangeActionEntityType.DEVICE_PARAMETER_VALUE_CHANGE)
      const model = serializer.convertJsonApiDataToModel(data, included)

      expect(model.id).toEqual('2')
      expect(model.description).toEqual('value change')
      expect(model.value).toEqual('20')
      expect(model.date!).not.toBeNull()
      expect(model.date!.year).toEqual(2023)
      expect(model.date!.month).toEqual(7)
      expect(model.date!.day).toEqual(1)
      expect(model.date!.hour).toEqual(10)
      expect(model.date!.minute).toEqual(5)
      expect(model.date!.second).toEqual(15)
      expect(model.date!.zoneName).toEqual('UTC')
      // we just test for the id of the param, as the parameter serializer is
      // already tested in its own test
      expect(model.parameter).not.toBeNull()
      expect(model.parameter!.id).toEqual('1')
      // we just test for the id of the contact, as the contact serializer is
      // already tested in its own test
      expect(model.contact).not.toBeNull()
      expect(model.contact!.id).toEqual('1')
      expect(model.createdBy).not.toBeNull()
      expect(model.createdBy!.id).toEqual('1')
      expect(model.updatedBy).not.toBeNull()
      expect(model.updatedBy!.id).toEqual('1')
    })
  })
  describe('#convertJsonApiObjectToModel', () => {
    it('should convert an example payload to a model', () => {
      const data: IJsonApiEntityEnvelope = {
        data: {
          id: '2',
          type: 'device_parameter_value_change_action',
          attributes: {
            description: 'value change',
            value: '20',
            date: '2023-07-01T10:05:15.194629+00:00',
            created_at: '2023-07-14T11:07:31.194629+00:00',
            updated_at: '2023-07-14T11:47:01.636331+00:00'
          },
          relationships: {
            created_by: {
              data: {
                type: 'user',
                id: '9'
              }
            },
            updated_by: {
              data: {
                type: 'user',
                id: '9'
              }
            },
            contact: {
              data: {
                type: 'contact',
                id: '1'
              }
            },
            device_parameter: {
              data: {
                type: 'device_parameter',
                id: '1'
              }
            }
          }
        },
        included: [
          {
            type: 'user',
            id: '9',
            attributes: {
              subject: 'contact@example.com'
            },
            relationships: {
              contact: {
                data: {
                  type: 'contact',
                  id: '1'
                }
              }
            }
          },
          {
            type: 'contact',
            id: '1',
            attributes: {
              active: true,
              email: 'contact@example.com',
              family_name: 'Example',
              given_name: 'Eric',
              orcid: null,
              organization: 'example.com',
              website: 'http://example.com'
            }
          },
          {
            type: 'device_parameter',
            id: '1',
            attributes: {
              label: 'Parameter 1',
              description: 'Unit description',
              unit_name: 'Unit 1',
              unit_uri: 'http://example.com/unit1'
            }
          }
        ]
      }

      const serializer = new ParameterChangeActionSerializer(ParameterChangeActionEntityType.DEVICE_PARAMETER_VALUE_CHANGE)
      const model = serializer.convertJsonApiObjectToModel(data)

      expect(model.id).toEqual('2')
      expect(model.description).toEqual('value change')
      expect(model.value).toEqual('20')
      expect(model.date!).not.toBeNull()
      expect(model.date!.year).toEqual(2023)
      expect(model.date!.month).toEqual(7)
      expect(model.date!.day).toEqual(1)
      expect(model.date!.hour).toEqual(10)
      expect(model.date!.minute).toEqual(5)
      expect(model.date!.second).toEqual(15)
      expect(model.date!.zoneName).toEqual('UTC')
      // we just test for the id of the param, as the parameter serializer is
      // already tested in its own test
      expect(model.parameter).not.toBeNull()
      expect(model.parameter!.id).toEqual('1')
      // we just test for the id of the contact, as the contact serializer is
      // already tested in its own test
      expect(model.contact).not.toBeNull()
      expect(model.contact!.id).toEqual('1')
      expect(model.createdBy).not.toBeNull()
      expect(model.createdBy!.id).toEqual('1')
      expect(model.updatedBy).not.toBeNull()
      expect(model.updatedBy!.id).toEqual('1')
    })
  })
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert an example payload with a list of parameter change actions to a list of models', () => {
      const data: IJsonApiEntityListEnvelope = {
        data: [
          {
            id: '2',
            type: 'device_parameter_value_change_action',
            attributes: {
              description: 'value change',
              value: '20',
              date: '2023-07-01T10:05:15.194629+00:00',
              created_at: '2023-07-14T11:07:31.194629+00:00',
              updated_at: '2023-07-14T11:47:01.636331+00:00'
            },
            relationships: {
              created_by: {
                data: {
                  type: 'user',
                  id: '9'
                }
              },
              updated_by: {
                data: {
                  type: 'user',
                  id: '9'
                }
              },
              contact: {
                data: {
                  type: 'contact',
                  id: '1'
                }
              },
              device_parameter: {
                data: {
                  type: 'device_parameter',
                  id: '1'
                }
              }
            }
          },
          {
            id: '3',
            type: 'device_parameter_value_change_action',
            attributes: {
              description: 'value change 2',
              value: '30',
              date: '2023-07-02T10:05:15.194629+00:00',
              created_at: '2023-07-15T11:07:31.194629+00:00',
              updated_at: '2023-07-15T11:47:01.636331+00:00'
            },
            relationships: {
              created_by: {
                data: {
                  type: 'user',
                  id: '10'
                }
              },
              updated_by: {
                data: {
                  type: 'user',
                  id: '10'
                }
              },
              contact: {
                data: {
                  type: 'contact',
                  id: '2'
                }
              },
              device_parameter: {
                data: {
                  type: 'device_parameter',
                  id: '1'
                }
              }
            }
          }
        ],
        included: [
          {
            type: 'user',
            id: '9',
            attributes: {
              subject: 'contact@example.com'
            },
            relationships: {
              contact: {
                data: {
                  type: 'contact',
                  id: '1'
                }
              }
            }
          },
          {
            type: 'user',
            id: '10',
            attributes: {
              subject: 'contact2@example.com'
            },
            relationships: {
              contact: {
                data: {
                  type: 'contact',
                  id: '2'
                }
              }
            }
          },
          {
            type: 'contact',
            id: '1',
            attributes: {
              active: true,
              email: 'contact@example.com',
              family_name: 'Example',
              given_name: 'Eric',
              orcid: null,
              organization: 'example.com',
              website: 'http://example.com'
            }
          },
          {
            type: 'contact',
            id: '2',
            attributes: {
              active: true,
              email: 'contact2@example.com',
              family_name: 'Example',
              given_name: 'Barbara',
              orcid: null,
              organization: 'example.com',
              website: 'http://example.com'
            }
          },
          {
            type: 'device_parameter',
            id: '1',
            attributes: {
              label: 'Parameter 1',
              description: 'Unit description',
              unit_name: 'Unit 1',
              unit_uri: 'http://example.com/unit1'
            }
          }
        ]
      }

      const serializer = new ParameterChangeActionSerializer(ParameterChangeActionEntityType.DEVICE_PARAMETER_VALUE_CHANGE)
      const result = serializer.convertJsonApiObjectListToModelList(data)

      expect(result).toHaveLength(2)
      // first change
      expect(result[0].id).toEqual('2')
      expect(result[0].description).toEqual('value change')
      expect(result[0].value).toEqual('20')
      expect(result[0].date!).not.toBeNull()
      expect(result[0].date!.year).toEqual(2023)
      expect(result[0].date!.month).toEqual(7)
      expect(result[0].date!.day).toEqual(1)
      expect(result[0].date!.hour).toEqual(10)
      expect(result[0].date!.minute).toEqual(5)
      expect(result[0].date!.second).toEqual(15)
      expect(result[0].date!.zoneName).toEqual('UTC')
      // we just test for the id of the param, as the parameter serializer is
      // already tested in its own test
      expect(result[0].parameter).not.toBeNull()
      expect(result[0].parameter!.id).toEqual('1')
      // we just test for the id of the contact, as the contact serializer is
      // already tested in its own test
      expect(result[0].contact).not.toBeNull()
      expect(result[0].contact!.id).toEqual('1')
      expect(result[0].createdBy).not.toBeNull()
      expect(result[0].createdBy!.id).toEqual('1')
      expect(result[0].updatedBy).not.toBeNull()
      expect(result[0].updatedBy!.id).toEqual('1')
      // second change
      expect(result[1].id).toEqual('3')
      expect(result[1].description).toEqual('value change 2')
      expect(result[1].value).toEqual('30')
      expect(result[1].date!).not.toBeNull()
      expect(result[1].date!.year).toEqual(2023)
      expect(result[1].date!.month).toEqual(7)
      expect(result[1].date!.day).toEqual(2)
      expect(result[1].date!.hour).toEqual(10)
      expect(result[1].date!.minute).toEqual(5)
      expect(result[1].date!.second).toEqual(15)
      expect(result[1].date!.zoneName).toEqual('UTC')
      // we just test for the id of the param, as the parameter serializer is
      // already tested in its own test
      expect(result[1].parameter).not.toBeNull()
      expect(result[1].parameter!.id).toEqual('1')
      // we just test for the id of the contact, as the contact serializer is
      // already tested in its own test
      expect(result[1].contact).not.toBeNull()
      expect(result[1].contact!.id).toEqual('2')
      expect(result[1].createdBy).not.toBeNull()
      expect(result[1].createdBy!.id).toEqual('2')
      expect(result[1].updatedBy).not.toBeNull()
      expect(result[1].updatedBy!.id).toEqual('2')
    })
  })
  describe('#convertJsonApiRelationshipsModelList', () => {
    it('should convert an example payload with a relationships to parameters and included entities to a list of models', () => {
      const relationships: IJsonApiRelationships = {
        device_parameter_value_change_actions: {
          data: [
            {
              id: '123',
              type: 'device_parameter_value_change_action'
            },
            {
              id: '456',
              type: 'device_parameter_value_change_action'
            }
          ]
        }
      }
      const included: IJsonApiEntityWithOptionalAttributes[] = [
        {
          id: '123',
          type: 'device_parameter_value_change_action',
          attributes: {
            value: '10',
            description: 'Test value change one',
            date: '2023-07-02T10:05:15.194629+00:00'
          }
        },
        {
          id: '456',
          type: 'device_parameter_value_change_action',
          attributes: {
            value: '20',
            description: 'Test value change two',
            date: '2023-07-03T10:05:15.194629+00:00'
          }
        }
      ]

      const serializer = new ParameterChangeActionSerializer(ParameterChangeActionEntityType.DEVICE_PARAMETER_VALUE_CHANGE)
      const result = serializer.convertJsonApiRelationshipsModelList(relationships, included)

      // the test will not cover relations to parameters or contacts, as it
      // internally calls the method #convertJsonApiDataToModel which is
      // already tested above
      expect(result.length).toEqual(2)
      expect(result[0].id).toEqual('123')
      expect(result[0].value).toEqual('10')
      expect(result[0].description).toEqual('Test value change one')
      expect(result[1].id).toEqual('456')
      expect(result[1].value).toEqual('20')
      expect(result[1].description).toEqual('Test value change two')
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should convert a simple model with a parameter and contact relation to a JSONAPI payload', () => {
      // we don't need to create a full contact, as just the id is used in the
      // serializer
      const contact = new Contact()
      contact.id = '9'

      const action = ParameterChangeAction.createFromObject({
        id: '123',
        description: 'Parameter change action test',
        value: '10',
        date: DateTime.utc(2023, 7, 20, 11, 40),
        contact
      })
      // we don't need to create a full parameter relation, as just the id is
      // used in the serializer
      const relation: IParameterChangeActionRelation = {
        entityType: ParameterChangeActionRelationEntityType.DEVICE_PARAMETER,
        id: '1'
      }

      const serializer = new ParameterChangeActionSerializer(ParameterChangeActionEntityType.DEVICE_PARAMETER_VALUE_CHANGE)
      const jsonApiPayload = serializer.convertModelToJsonApiData(
        action,
        relation
      )

      expect(jsonApiPayload).toHaveProperty('id')
      expect(jsonApiPayload.id).toEqual('123')
      expect(jsonApiPayload).toHaveProperty('type')
      expect(jsonApiPayload.type).toEqual('device_parameter_value_change_action')
      expect(jsonApiPayload).toHaveProperty('attributes')
      expect(jsonApiPayload.attributes).toHaveProperty('description')
      expect(jsonApiPayload.attributes.description).toEqual('Parameter change action test')
      expect(jsonApiPayload.attributes).toHaveProperty('value')
      expect(jsonApiPayload.attributes.value).toEqual('10')
      expect(jsonApiPayload.attributes).toHaveProperty('date')
      expect(jsonApiPayload.attributes.date.toISO()).toEqual('2023-07-20T11:40:00.000Z')
      expect(jsonApiPayload).toHaveProperty('relationships')
      // relation to the parameter
      expect(jsonApiPayload.relationships).toHaveProperty('device_parameter')
      expect(jsonApiPayload.relationships!.device_parameter).toHaveProperty('data')
      const deviceParameterData: any = jsonApiPayload.relationships!.device_parameter.data
      expect(deviceParameterData).toHaveProperty('id')
      expect(deviceParameterData.id).toEqual('1')
      expect(deviceParameterData).toHaveProperty('type')
      expect(deviceParameterData.type).toEqual('device_parameter')
      // relation to the contact
      expect(jsonApiPayload.relationships).toHaveProperty('contact')
      expect(jsonApiPayload.relationships!.device_parameter).toHaveProperty('data')
      const contactData: any = jsonApiPayload.relationships!.contact.data
      expect(contactData).toHaveProperty('id')
      expect(contactData.id).toEqual('9')
      expect(contactData).toHaveProperty('type')
      expect(contactData.type).toEqual('contact')
    })
  })
  describe('#convertModelListToTupleListWithIdAndType', () => {
    it('should convert a list of parameter change actions to a list of JSONAPI entities with id and type only', () => {
      // no need to create a full object, as the serializer only uses the id of the instances
      const action1 = ParameterChangeAction.createFromObject({
        id: '123',
        description: 'Test parameter change action one',
        value: 'ABC'
      })
      const action2 = ParameterChangeAction.createFromObject({
        id: '456',
        description: 'Test parameter change action two',
        value: '90'
      })
      const serializer = new ParameterChangeActionSerializer(ParameterChangeActionEntityType.DEVICE_PARAMETER_VALUE_CHANGE)
      const result = serializer.convertModelListToTupleListWithIdAndType([action1, action2])

      expect(result.length).toEqual(2)
      expect(result[0].type).toEqual('device_parameter_value_change_action')
      expect(result[0].id).toEqual('123')
      expect(result[1].type).toEqual('device_parameter_value_change_action')
      expect(result[1].id).toEqual('456')
    })
  })
  describe('#convertModelListToJsonApiRelationshipsObject', () => {
    it('should convert a list of parameter change actions to a JSONAPI relationship object', () => {
      // no need to create a full object, as the serializer only uses the id of the instances
      const action1 = ParameterChangeAction.createFromObject({
        id: '123',
        description: 'Test parameter change action one',
        value: 'ABC'
      })
      const action2 = ParameterChangeAction.createFromObject({
        id: '456',
        description: 'Test parameter change action two',
        value: '90'
      })
      const serializer = new ParameterChangeActionSerializer(ParameterChangeActionEntityType.DEVICE_PARAMETER_VALUE_CHANGE)
      const result = serializer.convertModelListToJsonApiRelationshipObject([action1, action2])

      expect(result).toHaveProperty('device_parameter_value_change_actions')
      expect(result.device_parameter_value_change_actions).toHaveProperty('data')
      expect(result.device_parameter_value_change_actions.data.length).toEqual(2)
      expect(result.device_parameter_value_change_actions.data[0].type).toEqual('device_parameter_value_change_action')
      expect(result.device_parameter_value_change_actions.data[0].id).toEqual('123')
      expect(result.device_parameter_value_change_actions.data[1].type).toEqual('device_parameter_value_change_action')
      expect(result.device_parameter_value_change_actions.data[1].id).toEqual('456')
    })
  })
})
