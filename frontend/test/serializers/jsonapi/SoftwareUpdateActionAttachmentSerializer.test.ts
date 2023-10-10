/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020 - 2023
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
import { Attachment } from '@/models/Attachment'

import {
  DeviceSoftwareUpdateActionAttachmentSerializer,
  PlatformSoftwareUpdateActionAttachmentSerializer
} from '@/serializers/jsonapi/SoftwareUpdateActionAttachmentSerializer'

import {
  IJsonApiEntityEnvelope,
  IJsonApiEntityWithOptionalId,
  IJsonApiEntityWithOptionalAttributes,
  IJsonApiRelationships
} from '@/serializers/jsonapi/JsonApiTypes'

describe('SoftwareUpdateActionAttachmentSerializer', () => {
  describe('DeviceSoftwareUpdateActionAttachmentSerializer', () => {
    function getExampleObjectResponse (): IJsonApiEntityEnvelope {
      return {
        data: {
          type: 'device_software_update_action',
          relationships: {
            device_software_update_action_attachments: {
              links: {
                related: '/rdm/svm-api/v1/device-software-update-actions/9/relationships/device-software-update-action-attachments'
              },
              data: [
                {
                  type: 'device_software_update_action_attachment',
                  id: '6'
                },
                {
                  type: 'device_software_update_action_attachment',
                  id: '7'
                }
              ]
            },
            device: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-actions/9/relationships/device',
                related: '/rdm/svm-api/v1/devices/204'
              },
              data: {
                type: 'device',
                id: '204'
              }
            },
            contact: {
              links: {
                self: '/rdm/svm-api/v1/device-software-update-actions/9/relationships/contact',
                related: '/rdm/svm-api/v1/contacts/14'
              },
              data: {
                type: 'contact',
                id: '14'
              }
            }
          },
          attributes: {
            software_type_uri: 'https://cv/firmware',
            software_type_name: 'Firmware',
            update_date: '2021-05-21T00:00:00',
            description: 'dfdfdf',
            version: '1.42',
            repository_url: 'https://myrepo.de'
          },
          id: '9',
          links: {
            self: '/rdm/svm-api/v1/device-software-update-actions/9'
          }
        },
        links: {
          self: '/rdm/svm-api/v1/device-software-update-actions/9'
        },
        included: [
          {
            type: 'device_software_update_action_attachment',
            relationships: {
              attachment: {
                links: {
                  self: '/rdm/svm-api/v1/device-software-update-action-attachments/6/relationships/attachment',
                  related: '/rdm/svm-api/v1/device-attachments/51'
                },
                data: {
                  type: 'device_attachment',
                  id: '51'
                }
              },
              action: {
                links: {
                  self: '/rdm/svm-api/v1/device-software-update-action-attachments/6/relationships/action',
                  related: '/rdm/svm-api/v1/device-software-update-actions/9'
                }
              }
            },
            id: '6',
            links: {
              self: '/rdm/svm-api/v1/device-software-update-action-attachments/6'
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
            type: 'device_software_update_action_attachment',
            relationships: {
              attachment: {
                links: {
                  self: '/rdm/svm-api/v1/device-software-update-action-attachments/7/relationships/attachment',
                  related: '/rdm/svm-api/v1/device-attachments/52'
                },
                data: {
                  type: 'device_attachment',
                  id: '52'
                }
              },
              action: {
                links: {
                  self: '/rdm/svm-api/v1/device-software-update-action-attachments/7/relationships/action',
                  related: '/rdm/svm-api/v1/device-software-update-actions/9'
                }
              }
            },
            id: '7',
            links: {
              self: '/rdm/svm-api/v1/device-software-update-action-attachments/7'
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
        const serializer = new DeviceSoftwareUpdateActionAttachmentSerializer()
        expect(serializer.getActionTypeName()).toEqual('device_software_update_action')
      })
      it('should return a correct action attachment type name', () => {
        const serializer = new DeviceSoftwareUpdateActionAttachmentSerializer()
        expect(serializer.getActionAttachmentTypeName()).toEqual('device_software_update_action_attachment')
      })
      it('should return a the plural form of the action attachment type name', () => {
        const serializer = new DeviceSoftwareUpdateActionAttachmentSerializer()
        expect(serializer.getActionAttachmentTypeNamePlural()).toEqual('device_software_update_action_attachments')
      })
      it('should return a correct attachment type name', () => {
        const serializer = new DeviceSoftwareUpdateActionAttachmentSerializer()
        expect(serializer.getAttachmentTypeName()).toEqual('device_attachment')
      })
      it('should return an attachment serializer', () => {
        const serializer = new DeviceSoftwareUpdateActionAttachmentSerializer()
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
          type: 'device_software_update_action_attachment',
          attributes: {},
          relationships: {
            action: {
              data: {
                type: 'device_software_update_action',
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

        const serializer = new DeviceSoftwareUpdateActionAttachmentSerializer()
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
        const serializer = new DeviceSoftwareUpdateActionAttachmentSerializer()

        const attachmentList = serializer.convertJsonApiRelationshipsModelList(response.data.relationships as IJsonApiRelationships, response.included as IJsonApiEntityWithOptionalAttributes[])

        expect(attachmentList).toHaveLength(2)
        expect(attachmentList).toContainEqual(attachment1)
        expect(attachmentList).toContainEqual(attachment2)
      })
    })
  })
  describe('PlatformSoftwareUpdateActionAttachmentSerializer', () => {
    describe('constructing and types', () => {
      it('should return a correct action type name', () => {
        const serializer = new PlatformSoftwareUpdateActionAttachmentSerializer()
        expect(serializer.getActionTypeName()).toEqual('platform_software_update_action')
      })
      it('should return a correct action attachment type name', () => {
        const serializer = new PlatformSoftwareUpdateActionAttachmentSerializer()
        expect(serializer.getActionAttachmentTypeName()).toEqual('platform_software_update_action_attachment')
      })
      it('should return a the plural form of the action attachment type name', () => {
        const serializer = new PlatformSoftwareUpdateActionAttachmentSerializer()
        expect(serializer.getActionAttachmentTypeNamePlural()).toEqual('platform_software_update_action_attachments')
      })
      it('should return a correct attachment type name', () => {
        const serializer = new PlatformSoftwareUpdateActionAttachmentSerializer()
        expect(serializer.getAttachmentTypeName()).toEqual('platform_attachment')
      })
      it('should return an attachment serializer', () => {
        const serializer = new PlatformSoftwareUpdateActionAttachmentSerializer()
        expect(typeof serializer.attachmentSerializer).toBe('object')
      })
    })
  })
})
