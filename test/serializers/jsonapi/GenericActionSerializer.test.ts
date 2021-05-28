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
import { DateTime } from 'luxon'

import { Attachment } from '@/models/Attachment'
import { GenericAction } from '@/models/GenericAction'
import { Contact } from '@/models/Contact'

import {
  GenericDeviceActionSerializer,
  GenericPlatformActionSerializer
} from '@/serializers/jsonapi/GenericActionSerializer'

import {
  IJsonApiEntityEnvelope,
  IJsonApiEntityListEnvelope,
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiRelationships
} from '@/serializers/jsonapi/JsonApiTypes'

describe('GenericActionSerializer', () => {
  function getExampleObjectResponse (): IJsonApiEntityEnvelope {
    return {
      data: {
        type: 'generic_device_action',
        relationships: {
          generic_device_action_attachments: {
            links: {
              related: '/rdm/svm-api/v1/generic-device-actions/7/relationships/generic-device-action-attachments'
            },
            data: [
              {
                type: 'generic_device_action_attachment',
                id: '21'
              }
            ]
          },
          device: {
            links: {
              self: '/rdm/svm-api/v1/generic-device-actions/7/relationships/device',
              related: '/rdm/svm-api/v1/devices/204'
            },
            data: {
              type: 'device',
              id: '204'
            }
          },
          contact: {
            links: {
              self: '/rdm/svm-api/v1/generic-device-actions/7/relationships/contact',
              related: '/rdm/svm-api/v1/contacts/14'
            },
            data: {
              type: 'contact',
              id: '14'
            }
          }
        },
        attributes: {
          updated_at: '2021-05-27T07:08:35.964720',
          created_at: '2021-05-07T09:57:38.203251',
          action_type_name: 'Device maintainance',
          begin_date: '2021-05-23T00:00:00',
          end_date: '2021-06-01T00:00:00',
          action_type_uri: '',
          description: 'Bla'
        },
        id: '7',
        links: {
          self: '/rdm/svm-api/v1/generic-device-actions/7'
        }
      },
      links: {
        self: '/rdm/svm-api/v1/generic-device-actions/7'
      },
      included: [
        {
          type: 'contact',
          relationships: {
            platforms: {
              links: {
                related: '/rdm/svm-api/v1/contacts/14/relationships/platforms'
              },
              data: [

              ]
            },
            user: {
              links: {
                self: '/rdm/svm-api/v1/contacts/14/relationships/user'
              },
              data: {
                type: 'user',
                id: '6'
              }
            },
            configurations: {
              links: {
                related: '/rdm/svm-api/v1/contacts/14/relationships/configurations'
              },
              data: [

              ]
            },
            devices: {
              links: {
                related: '/rdm/svm-api/v1/contacts/14/relationships/devices'
              },
              data: [
                {
                  type: 'device',
                  id: '250'
                }
              ]
            }
          },
          attributes: {
            family_name: 'Hanisch',
            email: 'marc.hanisch@gfz-potsdam.de',
            website: '',
            given_name: 'Marc'
          },
          id: '14',
          links: {
            self: '/rdm/svm-api/v1/contacts/14'
          }
        }
      ],
      jsonapi: {
        version: '1.0'
      }
    }
  }

  function getExampleObjectListResponse (): IJsonApiEntityListEnvelope {
    return {
      data: [
        {
          type: 'generic_device_action',
          relationships: {
            generic_device_action_attachments: {
              links: {
                related: '/rdm/svm-api/v1/generic-device-actions/4/relationships/generic-device-action-attachments'
              },
              data: [
                {
                  type: 'generic_device_action_attachment',
                  id: '1'
                },
                {
                  type: 'generic_device_action_attachment',
                  id: '2'
                }
              ]
            },
            device: {
              links: {
                self: '/rdm/svm-api/v1/generic-device-actions/4/relationships/device',
                related: '/rdm/svm-api/v1/devices/204'
              },
              data: {
                type: 'device',
                id: '204'
              }
            },
            contact: {
              links: {
                self: '/rdm/svm-api/v1/generic-device-actions/4/relationships/contact',
                related: '/rdm/svm-api/v1/contacts/14'
              },
              data: {
                type: 'contact',
                id: '14'
              }
            }
          },
          attributes: {
            updated_at: null,
            created_at: '2021-05-07T09:11:59.289773',
            action_type_name: 'Device maintainance',
            begin_date: '2021-05-03T00:00:00',
            end_date: '2021-05-04T00:00:00',
            action_type_uri: '',
            description: 'yet another maintainance'
          },
          id: '4',
          links: {
            self: '/rdm/svm-api/v1/generic-device-actions/4'
          }
        },
        {
          type: 'generic_device_action',
          relationships: {
            generic_device_action_attachments: {
              links: {
                related: '/rdm/svm-api/v1/generic-device-actions/5/relationships/generic-device-action-attachments'
              },
              data: [
                {
                  type: 'generic_device_action_attachment',
                  id: '3'
                }
              ]
            },
            device: {
              links: {
                self: '/rdm/svm-api/v1/generic-device-actions/5/relationships/device',
                related: '/rdm/svm-api/v1/devices/204'
              },
              data: {
                type: 'device',
                id: '204'
              }
            },
            contact: {
              links: {
                self: '/rdm/svm-api/v1/generic-device-actions/5/relationships/contact',
                related: '/rdm/svm-api/v1/contacts/14'
              },
              data: {
                type: 'contact',
                id: '14'
              }
            }
          },
          attributes: {
            updated_at: null,
            created_at: '2021-05-07T09:23:53.678558',
            action_type_name: 'Device visit',
            begin_date: '2021-05-09T00:00:00',
            end_date: '2021-05-12T00:00:00',
            action_type_uri: '',
            description: 'Site was nice!'
          },
          id: '5',
          links: {
            self: '/rdm/svm-api/v1/generic-device-actions/5'
          }
        }
      ],
      links: {
        self: 'http://rz-vm64.gfz-potsdam.de:5000/rdm/svm-api/v1/generic-device-actions?page%5Bsize%5D=10000&include=contact%2Cgeneric_device_action_attachments.attachment'
      },
      included: [
        {
          type: 'generic_device_action_attachment',
          relationships: {
            attachment: {
              links: {
                self: '/rdm/svm-api/v1/generic-device-action-attachments/1/relationships/attachment',
                related: '/rdm/svm-api/v1/device-attachments/51'
              },
              data: {
                type: 'device_attachment',
                id: '51'
              }
            },
            action: {
              links: {
                self: '/rdm/svm-api/v1/generic-device-action-attachments/1/relationships/action',
                related: '/rdm/svm-api/v1/generic-device-actions/4'
              }
            }
          },
          id: '1',
          links: {
            self: '/rdm/svm-api/v1/generic-device-action-attachments/1'
          }
        },
        {
          type: 'device_attachment',
          relationships: {
            device: {
              links: {
                self: '/rdm/svm-api/v1/device-attachments/51/relationships/device',
                related: '/rdm/svm-api/v1/devices/204'
              },
              data: {
                type: 'device',
                id: '204'
              }
            }
          },
          attributes: {
            url: 'https://foo.de',
            label: 'Foo.de'
          },
          id: '51',
          links: {
            self: '/rdm/svm-api/v1/device-attachments/51'
          }
        },
        {
          type: 'generic_device_action_attachment',
          relationships: {
            attachment: {
              links: {
                self: '/rdm/svm-api/v1/generic-device-action-attachments/2/relationships/attachment',
                related: '/rdm/svm-api/v1/device-attachments/52'
              },
              data: {
                type: 'device_attachment',
                id: '52'
              }
            },
            action: {
              links: {
                self: '/rdm/svm-api/v1/generic-device-action-attachments/2/relationships/action',
                related: '/rdm/svm-api/v1/generic-device-actions/4'
              }
            }
          },
          id: '2',
          links: {
            self: '/rdm/svm-api/v1/generic-device-action-attachments/2'
          }
        },
        {
          type: 'device_attachment',
          relationships: {
            device: {
              links: {
                self: '/rdm/svm-api/v1/device-attachments/52/relationships/device',
                related: '/rdm/svm-api/v1/devices/204'
              },
              data: {
                type: 'device',
                id: '204'
              }
            }
          },
          attributes: {
            url: 'https://bar.baz',
            label: 'Bar.baz'
          },
          id: '52',
          links: {
            self: '/rdm/svm-api/v1/device-attachments/52'
          }
        },
        {
          type: 'contact',
          relationships: {
            user: {
              links: {
                self: '/rdm/svm-api/v1/contacts/14/relationships/user'
              },
              data: {
                type: 'user',
                id: '6'
              }
            }
          },
          attributes: {
            family_name: 'Hanisch',
            email: 'marc.hanisch@gfz-potsdam.de',
            website: '',
            given_name: 'Marc'
          },
          id: '14',
          links: {
            self: '/rdm/svm-api/v1/contacts/14'
          }
        },
        {
          type: 'generic_device_action_attachment',
          relationships: {
            attachment: {
              links: {
                self: '/rdm/svm-api/v1/generic-device-action-attachments/3/relationships/attachment',
                related: '/rdm/svm-api/v1/device-attachments/52'
              },
              data: {
                type: 'device_attachment',
                id: '52'
              }
            },
            action: {
              links: {
                self: '/rdm/svm-api/v1/generic-device-action-attachments/3/relationships/action',
                related: '/rdm/svm-api/v1/generic-device-actions/5'
              }
            }
          },
          id: '3',
          links: {
            self: '/rdm/svm-api/v1/generic-device-action-attachments/3'
          }
        }
      ],
      meta: {
        count: 2
      },
      jsonapi: {
        version: '1.0'
      }
    }
  }

  function getExampleDeviceResponse (): IJsonApiEntityEnvelope {
    return {
      data: {
        type: 'device',
        attributes: {
          persistent_identifier: null,
          model: 'SM1',
          website: 'http://www.adcon.com',
          short_name: 'Adcon SM1 soil moisture / temperature sensor FTDR Zeitlow 1',
          serial_number: '',
          updated_at: '2021-04-26T09:03:01.944689',
          long_name: 'Adcon SM 1 soil moisture / temperature sensor',
          device_type_uri: '',
          status_name: 'In Use',
          dual_use: false,
          device_type_name: 'Frequency/Time Domain Reflectometer (FTDR)(Soil moisture and temperature)',
          description: '',
          inventory_number: '',
          manufacturer_name: 'OTT Hydromet GmbH',
          created_at: '2021-01-18T07:07:24.360000',
          manufacturer_uri: 'OTT Hydromet GmbH',
          status_uri: 'http://rz-vm64.gfz-potsdam.de:8000/api/v1/equipmentstatus/2/'
        },
        relationships: {
          generic_device_actions: {
            links: {
              related: '/rdm/svm-api/v1/devices/204/relationships/generic-device-actions'
            },
            data: [
              {
                type: 'generic_device_action',
                id: '3'
              },
              {
                type: 'generic_device_action',
                id: '4'
              }
            ]
          }
        },
        id: '204',
        links: {
          self: '/rdm/svm-api/v1/devices/204'
        }
      },
      links: {
        self: '/rdm/svm-api/v1/devices/204'
      },
      included: [
        {
          type: 'generic_device_action',
          relationships: {
            generic_device_action_attachments: {
              links: {
                related: '/rdm/svm-api/v1/generic-device-actions/3/relationships/generic-device-action-attachments'
              },
              data: [

              ]
            },
            device: {
              links: {
                self: '/rdm/svm-api/v1/generic-device-actions/3/relationships/device',
                related: '/rdm/svm-api/v1/devices/204'
              },
              data: {
                type: 'device',
                id: '204'
              }
            },
            contact: {
              links: {
                self: '/rdm/svm-api/v1/generic-device-actions/3/relationships/contact',
                related: '/rdm/svm-api/v1/contacts/14'
              },
              data: {
                type: 'contact',
                id: '14'
              }
            }
          },
          attributes: {
            updated_at: null,
            created_at: '2021-05-06T12:54:18.899177',
            action_type_name: 'Device maintainance',
            begin_date: '2021-05-01T00:00:00',
            end_date: '2021-05-03T00:00:00',
            action_type_uri: '',
            description: 'Rasenmähen'
          },
          id: '3',
          links: {
            self: '/rdm/svm-api/v1/generic-device-actions/3'
          }
        },
        {
          type: 'generic_device_action',
          relationships: {
            generic_device_action_attachments: {
              links: {
                related: '/rdm/svm-api/v1/generic-device-actions/4/relationships/generic-device-action-attachments'
              },
              data: [
                {
                  type: 'generic_device_action_attachment',
                  id: '1'
                },
                {
                  type: 'generic_device_action_attachment',
                  id: '2'
                }
              ]
            },
            device: {
              links: {
                self: '/rdm/svm-api/v1/generic-device-actions/4/relationships/device',
                related: '/rdm/svm-api/v1/devices/204'
              },
              data: {
                type: 'device',
                id: '204'
              }
            },
            contact: {
              links: {
                self: '/rdm/svm-api/v1/generic-device-actions/4/relationships/contact',
                related: '/rdm/svm-api/v1/contacts/14'
              },
              data: {
                type: 'contact',
                id: '14'
              }
            }
          },
          attributes: {
            updated_at: null,
            created_at: '2021-05-07T09:11:59.289773',
            action_type_name: 'Device maintainance',
            begin_date: '2021-05-03T00:00:00',
            end_date: '2021-05-04T00:00:00',
            action_type_uri: '',
            description: 'yet another maintainance'
          },
          id: '4',
          links: {
            self: '/rdm/svm-api/v1/generic-device-actions/4'
          }
        }
      ],
      jsonapi: {
        version: '1.0'
      }
    }
  }

  function getExampleObjectResponseWithIncludedActionAttachments (): IJsonApiEntityEnvelope {
    return {
      data: {
        type: 'generic_device_action',
        relationships: {
          generic_device_action_attachments: {
            links: {
              related: '/rdm/svm-api/v1/generic-device-actions/7/relationships/generic-device-action-attachments'
            },
            data: [
              {
                type: 'generic_device_action_attachment',
                id: '21'
              }
            ]
          },
          device: {
            links: {
              self: '/rdm/svm-api/v1/generic-device-actions/7/relationships/device',
              related: '/rdm/svm-api/v1/devices/204'
            },
            data: {
              type: 'device',
              id: '204'
            }
          },
          contact: {
            links: {
              self: '/rdm/svm-api/v1/generic-device-actions/7/relationships/contact',
              related: '/rdm/svm-api/v1/contacts/14'
            },
            data: {
              type: 'contact',
              id: '14'
            }
          }
        },
        attributes: {
          updated_at: '2021-05-28T11:12:54.938479',
          created_at: '2021-05-07T09:57:38.203251',
          action_type_name: 'Device maintainance',
          begin_date: '2021-05-23T00:00:00',
          end_date: '2021-06-01T00:00:00',
          action_type_uri: '',
          description: 'Bla'
        },
        id: '7',
        links: {
          self: '/rdm/svm-api/v1/generic-device-actions/7'
        }
      },
      links: {
        self: '/rdm/svm-api/v1/generic-device-actions/7'
      },
      included: [
        {
          type: 'generic_device_action_attachment',
          relationships: {
            attachment: {
              links: {
                self: '/rdm/svm-api/v1/generic-device-action-attachments/21/relationships/attachment',
                related: '/rdm/svm-api/v1/device-attachments/51'
              },
              data: {
                type: 'device_attachment',
                id: '51'
              }
            },
            action: {
              links: {
                self: '/rdm/svm-api/v1/generic-device-action-attachments/21/relationships/action',
                related: '/rdm/svm-api/v1/generic-device-actions/7'
              }
            }
          },
          id: '21',
          links: {
            self: '/rdm/svm-api/v1/generic-device-action-attachments/21'
          }
        },
        {
          type: 'device_attachment',
          relationships: {
            device: {
              links: {
                self: '/rdm/svm-api/v1/device-attachments/51/relationships/device',
                related: '/rdm/svm-api/v1/devices/204'
              },
              data: {
                type: 'device',
                id: '204'
              }
            }
          },
          attributes: {
            url: 'https://foo.de',
            label: 'Foo.de'
          },
          id: '51',
          links: {
            self: '/rdm/svm-api/v1/device-attachments/51'
          }
        }
      ],
      jsonapi: {
        version: '1.0'
      }
    }
  }

  describe('GenericDeviceActionSerializer', () => {
    describe('constructing and types', () => {
      it('should return \'device\' as its type', () => {
        const serializer = new GenericDeviceActionSerializer()
        expect(serializer.type).toEqual('device')
      })
      it('should return a correct action type name', () => {
        const serializer = new GenericDeviceActionSerializer()
        expect(serializer.getActionTypeName()).toEqual('generic_device_action')
      })
      it('should return a the plural form of the action type name', () => {
        const serializer = new GenericDeviceActionSerializer()
        expect(serializer.getActionTypeNamePlural()).toEqual('generic_device_actions')
      })
      it('should return a correction action attachment type name', () => {
        const serializer = new GenericDeviceActionSerializer()
        expect(serializer.getActionAttachmentTypeName()).toEqual('generic_device_action_attachment')
      })
    })
    describe('#convertJsonApiObjectToModel', () => {
      it('should return a serialized generic action from an API response', () => {
        const contact = Contact.createFromObject({
          id: '14',
          givenName: 'Marc',
          familyName: 'Hanisch',
          email: 'marc.hanisch@gfz-potsdam.de',
          website: ''
        })
        const expectedAction = new GenericAction()
        expectedAction.id = '7'
        expectedAction.description = 'Bla'
        expectedAction.actionTypeName = 'Device maintainance'
        expectedAction.actionTypeUrl = ''
        expectedAction.beginDate = DateTime.fromISO('2021-05-23T00:00:00', { zone: 'UTC' })
        expectedAction.endDate = DateTime.fromISO('2021-06-01T00:00:00', { zone: 'UTC' })
        expectedAction.contact = contact

        const serializer = new GenericDeviceActionSerializer()
        const action = serializer.convertJsonApiObjectToModel(getExampleObjectResponse())

        expect(action).toEqual(expectedAction)
      })
    })
    describe('#convertJsonApiDataToModel', () => {
      it('should return a serialized generic action from an API response object', () => {
        const contact = Contact.createFromObject({
          id: '14',
          givenName: 'Marc',
          familyName: 'Hanisch',
          email: 'marc.hanisch@gfz-potsdam.de',
          website: ''
        })
        const expectedAction = new GenericAction()
        expectedAction.id = '7'
        expectedAction.description = 'Bla'
        expectedAction.actionTypeName = 'Device maintainance'
        expectedAction.actionTypeUrl = ''
        expectedAction.beginDate = DateTime.fromISO('2021-05-23T00:00:00', { zone: 'UTC' })
        expectedAction.endDate = DateTime.fromISO('2021-06-01T00:00:00', { zone: 'UTC' })
        expectedAction.contact = contact

        const serializer = new GenericDeviceActionSerializer()
        const data = getExampleObjectResponse().data
        const included = getExampleObjectResponse().included
        const action = serializer.convertJsonApiDataToModel(data, included as IJsonApiEntityWithOptionalAttributes[])

        expect(action).toEqual(expectedAction)
      })
    })
    describe('#convertJsonApiRelationshipsModelList', () => {
      it('should return a serialized list of generic actions from an list of included API entities', () => {
        const serializer = new GenericDeviceActionSerializer()
        const response = getExampleDeviceResponse()

        const relationships = response.data.relationships
        const included = response.included

        const expectedAction1 = new GenericAction()
        expectedAction1.id = '3'
        expectedAction1.description = 'Rasenmähen'
        expectedAction1.actionTypeName = 'Device maintainance'
        expectedAction1.actionTypeUrl = ''
        expectedAction1.beginDate = DateTime.fromISO('2021-05-01T00:00:00', { zone: 'UTC' })
        expectedAction1.endDate = DateTime.fromISO('2021-05-03T00:00:00', { zone: 'UTC' })

        const expectedAction2 = new GenericAction()
        expectedAction2.id = '4'
        expectedAction2.description = 'yet another maintainance'
        expectedAction2.actionTypeName = 'Device maintainance'
        expectedAction2.actionTypeUrl = ''
        expectedAction2.beginDate = DateTime.fromISO('2021-05-03T00:00:00', { zone: 'UTC' })
        expectedAction2.endDate = DateTime.fromISO('2021-05-04T00:00:00', { zone: 'UTC' })

        const actionList = serializer.convertJsonApiRelationshipsModelList(relationships as IJsonApiRelationships, included as IJsonApiEntityWithOptionalAttributes[])

        expect(actionList).toHaveProperty('genericDeviceActions')
        expect(actionList.genericDeviceActions).toContainEqual(expectedAction1)
        expect(actionList.genericDeviceActions).toContainEqual(expectedAction2)
      })
    })
    describe('#convertJsonApiObjectListToModelList', () => {
      it('should return a list of serialized generic action from an API response', () => {
        const contact = Contact.createFromObject({
          id: '14',
          givenName: 'Marc',
          familyName: 'Hanisch',
          email: 'marc.hanisch@gfz-potsdam.de',
          website: ''
        })
        const attachment1 = Attachment.createFromObject({
          id: '51',
          label: 'Foo.de',
          url: 'https://foo.de'
        })
        const attachment2 = Attachment.createFromObject({
          id: '52',
          label: 'Bar.baz',
          url: 'https://bar.baz'
        })
        const expectedAction1 = new GenericAction()
        expectedAction1.id = '4'
        expectedAction1.description = 'yet another maintainance'
        expectedAction1.actionTypeName = 'Device maintainance'
        expectedAction1.actionTypeUrl = ''
        expectedAction1.beginDate = DateTime.fromISO('2021-05-03T00:00:00', { zone: 'UTC' })
        expectedAction1.endDate = DateTime.fromISO('2021-05-04T00:00:00', { zone: 'UTC' })
        expectedAction1.contact = contact
        expectedAction1.attachments = [
          attachment1,
          attachment2
        ]

        const expectedAction2 = new GenericAction()
        expectedAction2.id = '5'
        expectedAction2.description = 'Site was nice!'
        expectedAction2.actionTypeName = 'Device visit'
        expectedAction2.actionTypeUrl = ''
        expectedAction2.beginDate = DateTime.fromISO('2021-05-09T00:00:00', { zone: 'UTC' })
        expectedAction2.endDate = DateTime.fromISO('2021-05-12T00:00:00', { zone: 'UTC' })
        expectedAction2.contact = contact
        expectedAction2.attachments = [
          attachment2
        ]

        const serializer = new GenericDeviceActionSerializer()
        const actionList = serializer.convertJsonApiObjectListToModelList(getExampleObjectListResponse())

        expect(actionList).toContainEqual(expectedAction1)
        expect(actionList).toContainEqual(expectedAction2)
      })
    })
    describe('#convertModelToJsonApiData', () => {
      it('should return a JSON API representation from a generic action model', () => {
        const contact = Contact.createFromObject({
          id: '14',
          givenName: 'Marc',
          familyName: 'Hanisch',
          email: 'marc.hanisch@gfz-potsdam.de',
          website: ''
        })

        const action = new GenericAction()
        action.id = '7'
        action.description = 'Bla'
        action.actionTypeName = 'Device maintainance'
        action.actionTypeUrl = ''
        action.beginDate = DateTime.fromISO('2021-05-23T00:00:00', { zone: 'UTC' })
        action.endDate = DateTime.fromISO('2021-06-01T00:00:00', { zone: 'UTC' })
        action.contact = contact

        const expectedApiModel: IJsonApiEntityWithOptionalId = {
          type: 'generic_device_action',
          id: '7',
          attributes: {
            description: 'Bla',
            action_type_name: 'Device maintainance',
            action_type_uri: '',
            begin_date: '2021-05-23T00:00:00.000Z',
            end_date: '2021-06-01T00:00:00.000Z'
          },
          relationships: {
            device: {
              data: {
                type: 'device',
                id: '204'
              }
            },
            contact: {
              data: {
                type: 'contact',
                id: '14'
              }
            }
          }
        }

        const serializer = new GenericDeviceActionSerializer()
        const apiModel = serializer.convertModelToJsonApiData(action, '204')

        expect(apiModel).toEqual(expectedApiModel)
      })
    })
    describe('#convertModelToJsonApiRelationshipObject', () => {
      it('should return a JSON API relationships object from a generic action model', () => {
        const action = new GenericAction()
        action.id = '7'

        const expectedRelationship: IJsonApiRelationships = {
          generic_device_action: {
            data: {
              id: '7',
              type: 'generic_device_action'
            }
          }
        }
        const serializer = new GenericDeviceActionSerializer()
        const apiRelationship = serializer.convertModelToJsonApiRelationshipObject(action)

        expect(apiRelationship).toEqual(expectedRelationship)
      })
    })
    describe('#convertJsonApiIncludedGenericActionAttachmentsToIdList', () => {
      it('should return a list of generic_device_action_attachment ids / attachment ids mappings', () => {
        const expectedMappings = [
          {
            genericActionAttachmentId: '21',
            attachmentId: '51'
          }
        ]
        const serializer = new GenericDeviceActionSerializer()
        const data = getExampleObjectResponseWithIncludedActionAttachments()
        const mappings = serializer.convertJsonApiIncludedGenericActionAttachmentsToIdList(data.included as IJsonApiEntityWithOptionalAttributes[])

        expect(mappings).toEqual(expectedMappings)
      })
    })
  })

  describe('GenericPlatformActionSerializer', () => {
    describe('constructing and types', () => {
      it('should return \'platform\' as its type', () => {
        const serializer = new GenericPlatformActionSerializer()
        expect(serializer.type).toEqual('platform')
      })
      it('should return a correct action type name', () => {
        const serializer = new GenericPlatformActionSerializer()
        expect(serializer.getActionTypeName()).toEqual('generic_platform_action')
      })
      it('should return a the plural form of the action type name', () => {
        const serializer = new GenericPlatformActionSerializer()
        expect(serializer.getActionTypeNamePlural()).toEqual('generic_platform_actions')
      })
      it('should return a correction action attachment type name', () => {
        const serializer = new GenericPlatformActionSerializer()
        expect(serializer.getActionAttachmentTypeName()).toEqual('generic_platform_action_attachment')
      })
    })
  })
})
describe('GenericDeviceActionSerializer', () => {
})
