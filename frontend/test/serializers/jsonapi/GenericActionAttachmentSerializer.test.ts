/**
 * @license EUPL-1.2
 * SPDX-FileCopyrightText: 2020 - 2023
 * - Nils Brinckmann <nils.brinckmann@gfz-potsdam.de>
 * - Marc Hanisch <marc.hanisch@gfz-potsdam.de>
 * - Tim Eder <tim.eder@ufz.de>
 * - Helmholtz Centre Potsdam - GFZ German Research Centre for Geosciences (GFZ, https://www.gfz-potsdam.de)
 *
 * SPDX-License-Identifier: EUPL-1.2
 */
import { Attachment } from '@/models/Attachment'

import {
  GenericConfigurationActionAttachmentSerializer,
  GenericDeviceActionAttachmentSerializer,
  GenericPlatformActionAttachmentSerializer
} from '@/serializers/jsonapi/GenericActionAttachmentSerializer'

import {
  IJsonApiEntityEnvelope,
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiRelationships
} from '@/serializers/jsonapi/JsonApiTypes'

describe('GenericActionAttachmentSerializer', () => {
  describe('GenericDeviceActionAttachmentSerializer', () => {
    function getExampleObjectResponse (): IJsonApiEntityEnvelope {
      return {
        data: {
          type: 'generic_device_action',
          relationships: {
            generic_device_action_attachments: {
              links: {
                related: '/rdm/svm-api/v1/generic-device-actions/9/relationships/generic-device-action-attachments'
              },
              data: [
                {
                  type: 'generic_device_action_attachment',
                  id: '6'
                },
                {
                  type: 'generic_device_action_attachment',
                  id: '7'
                }
              ]
            },
            device: {
              links: {
                self: '/rdm/svm-api/v1/generic-device-actions/9/relationships/device',
                related: '/rdm/svm-api/v1/devices/204'
              },
              data: {
                type: 'device',
                id: '204'
              }
            },
            contact: {
              links: {
                self: '/rdm/svm-api/v1/generic-device-actions/9/relationships/contact',
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
            created_at: '2021-05-12T08:19:56.781661',
            action_type_name: 'Device visit',
            begin_date: '2021-05-21T00:00:00',
            end_date: '2021-05-30T00:00:00',
            action_type_uri: '',
            description: 'dfdfdf'
          },
          id: '9',
          links: {
            self: '/rdm/svm-api/v1/generic-device-actions/9'
          }
        },
        links: {
          self: '/rdm/svm-api/v1/generic-device-actions/9'
        },
        included: [
          {
            type: 'generic_device_action_attachment',
            relationships: {
              attachment: {
                links: {
                  self: '/rdm/svm-api/v1/generic-device-action-attachments/6/relationships/attachment',
                  related: '/rdm/svm-api/v1/device-attachments/51'
                },
                data: {
                  type: 'device_attachment',
                  id: '51'
                }
              },
              action: {
                links: {
                  self: '/rdm/svm-api/v1/generic-device-action-attachments/6/relationships/action',
                  related: '/rdm/svm-api/v1/generic-device-actions/9'
                }
              }
            },
            id: '6',
            links: {
              self: '/rdm/svm-api/v1/generic-device-action-attachments/6'
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
              label: 'Foo.de',
              description: 'The foo'
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
                  self: '/rdm/svm-api/v1/generic-device-action-attachments/7/relationships/attachment',
                  related: '/rdm/svm-api/v1/device-attachments/52'
                },
                data: {
                  type: 'device_attachment',
                  id: '52'
                }
              },
              action: {
                links: {
                  self: '/rdm/svm-api/v1/generic-device-action-attachments/7/relationships/action',
                  related: '/rdm/svm-api/v1/generic-device-actions/9'
                }
              }
            },
            id: '7',
            links: {
              self: '/rdm/svm-api/v1/generic-device-action-attachments/7'
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
              label: 'Bar.baz',
              description: 'The bar'
            },
            id: '52',
            links: {
              self: '/rdm/svm-api/v1/device-attachments/52'
            }
          }
        ],
        jsonapi: {
          version: '1.0'
        }
      }
    }

    describe('constructing and types', () => {
      it('should return a correct action type name', () => {
        const serializer = new GenericDeviceActionAttachmentSerializer()
        expect(serializer.getActionTypeName()).toEqual('generic_device_action')
      })
      it('should return a correct action attachment type name', () => {
        const serializer = new GenericDeviceActionAttachmentSerializer()
        expect(serializer.getActionAttachmentTypeName()).toEqual('generic_device_action_attachment')
      })
      it('should return a the plural form of the action attachment type name', () => {
        const serializer = new GenericDeviceActionAttachmentSerializer()
        expect(serializer.getActionAttachmentTypeNamePlural()).toEqual('generic_device_action_attachments')
      })
      it('should return a correct attachment type name', () => {
        const serializer = new GenericDeviceActionAttachmentSerializer()
        expect(serializer.getAttachmentTypeName()).toEqual('device_attachment')
      })
      it('should return an attachment serializer', () => {
        const serializer = new GenericDeviceActionAttachmentSerializer()
        expect(typeof serializer.attachmentSerializer).toBe('object')
      })
    })
    describe('#convertModelToJsonApiData', () => {
      it('should return a JSON API object from an attachment and an action id', () => {
        const attachment = Attachment.createFromObject({
          id: '1',
          label: 'Foo',
          url: 'https://bar.baz',
          description: 'The foo',
          isUpload: false,
          createdAt: null
        })
        const actionId = '2'

        const expectedApiModel: IJsonApiEntityWithOptionalId = {
          type: 'generic_device_action_attachment',
          attributes: {},
          relationships: {
            action: {
              data: {
                type: 'generic_device_action',
                id: '2'
              }
            },
            attachment: {
              data: {
                type: 'device_attachment',
                id: '1'
              }
            }
          }
        }

        const serializer = new GenericDeviceActionAttachmentSerializer()
        const apiModel = serializer.convertModelToJsonApiData(attachment, actionId)

        expect(apiModel).toEqual(expectedApiModel)
      })
    })
    describe('#convertJsonApiRelationshipsModelList', () => {
      it('should return a serialized list of attachments from an list of included API entities', () => {
        const attachment1 = Attachment.createFromObject({
          id: '51',
          label: 'Foo.de',
          url: 'https://foo.de',
          description: 'The foo',
          isUpload: false,
          createdAt: null
        })
        const attachment2 = Attachment.createFromObject({
          id: '52',
          label: 'Bar.baz',
          url: 'https://bar.baz',
          description: 'The bar',
          isUpload: false,
          createdAt: null
        })

        const response = getExampleObjectResponse()
        const serializer = new GenericDeviceActionAttachmentSerializer()

        const attachmentList = serializer.convertJsonApiRelationshipsModelList(response.data.relationships as IJsonApiRelationships, response.included as IJsonApiEntityWithOptionalAttributes[])

        expect(attachmentList).toHaveLength(2)
        expect(attachmentList).toContainEqual(attachment1)
        expect(attachmentList).toContainEqual(attachment2)
      })
    })
  })
  describe('GenericPlatformActionAttachmentSerializer', () => {
    describe('constructing and types', () => {
      it('should return a correct action type name', () => {
        const serializer = new GenericPlatformActionAttachmentSerializer()
        expect(serializer.getActionTypeName()).toEqual('generic_platform_action')
      })
      it('should return a correct action attachment type name', () => {
        const serializer = new GenericPlatformActionAttachmentSerializer()
        expect(serializer.getActionAttachmentTypeName()).toEqual('generic_platform_action_attachment')
      })
      it('should return a the plural form of the action attachment type name', () => {
        const serializer = new GenericPlatformActionAttachmentSerializer()
        expect(serializer.getActionAttachmentTypeNamePlural()).toEqual('generic_platform_action_attachments')
      })
      it('should return a correct attachment type name', () => {
        const serializer = new GenericPlatformActionAttachmentSerializer()
        expect(serializer.getAttachmentTypeName()).toEqual('platform_attachment')
      })
      it('should return an attachment serializer', () => {
        const serializer = new GenericPlatformActionAttachmentSerializer()
        expect(typeof serializer.attachmentSerializer).toBe('object')
      })
    })
  })

  describe('GenericConfigurationActionAttachmentSerializer', () => {
    describe('constructing and types', () => {
      it('should return a correct action type name', () => {
        const serializer = new GenericConfigurationActionAttachmentSerializer()
        expect(serializer.getActionTypeName()).toEqual('generic_configuration_action')
      })
      it('should return a correct action attachment type name', () => {
        const serializer = new GenericConfigurationActionAttachmentSerializer()
        expect(serializer.getActionAttachmentTypeName()).toEqual('generic_configuration_action_attachment')
      })
      it('should return a the plural form of the action attachment type name', () => {
        const serializer = new GenericConfigurationActionAttachmentSerializer()
        expect(serializer.getActionAttachmentTypeNamePlural()).toEqual('generic_configuration_action_attachments')
      })
      it('should return a correct attachment type name', () => {
        const serializer = new GenericConfigurationActionAttachmentSerializer()
        expect(serializer.getAttachmentTypeName()).toEqual('configuration_attachment')
      })
      it('should return an attachment serializer', () => {
        const serializer = new GenericConfigurationActionAttachmentSerializer()
        expect(typeof serializer.attachmentSerializer).toBe('object')
      })
    })
  })
})
