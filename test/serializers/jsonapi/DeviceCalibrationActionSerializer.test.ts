/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2023
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
import { Contact } from '@/models/Contact'
import { DeviceCalibrationAction } from '@/models/DeviceCalibrationAction'
import { DeviceProperty } from '@/models/DeviceProperty'

import { DeviceCalibrationActionSerializer } from '@/serializers/jsonapi/DeviceCalibrationActionSerializer'

import {
  IJsonApiEntityEnvelope,
  IJsonApiEntityWithOptionalId
} from '@/serializers/jsonapi/JsonApiTypes'

describe('DeviceCalibrationActionSerializer', () => {
  function getExampleObjectResponse (): IJsonApiEntityEnvelope {
    return {
      data: {
        type: 'device_calibration_action',
        attributes: {
          formula: 'x^2',
          value: 17,
          version: 'fe23f4afc12f234sd',
          current_calibration_date: '2021-07-01T00:00:00',
          next_calibration_date: '2021-08-01T00:00:00',
          description: 'Test',
          created_at: '2021-06-14T14:47:53.554867',
          updated_at: null
        },
        relationships: {
          device: {
            links: {
              self: '/rdm/svm-api/v1/device-calibration-actions/3/relationships/device',
              related: '/rdm/svm-api/v1/devices/204'
            },
            data: {
              type: 'device',
              id: '204'
            }
          },
          contact: {
            links: {
              self: '/rdm/svm-api/v1/device-calibration-actions-actions/3/relationships/contact',
              related: '/rdm/svm-api/v1/contacts/3'
            },
            data: {
              type: 'contact',
              id: '3'
            }
          },
          device_calibration_attachments: {
            links: {
              related: '/rdm/svm-api/v1/device-calibration-actions/3/relationships/device-calibration-action-attachments'
            },
            data: [

            ]
          }
        },
        id: '3',
        links: {
          self: '/rdm/svm-api/v1/device-software-update-actions/3'
        }
      },
      links: {
        self: '/rdm/svm-api/v1/device-software-update-actions/3'
      },
      included: [
        {
          type: 'contact',
          attributes: {
            family_name: 'Brinckmann',
            given_name: 'Nils',
            website: '',
            email: 'nils.brinckmann@gfz-potsdam.de'
          },
          relationships: {
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
            },
            configurations: {
              links: {
                related: '/rdm/svm-api/v1/contacts/14/relationships/configurations'
              },
              data: [

              ]
            },
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
            }
          },
          id: '3',
          links: {
            self: '/rdm/svm-api/v1/contacts/3'
          }
        }
      ],
      jsonapi: {
        version: '1.0'
      }
    }
  }
  describe('#convertJsonApiObjectToModel', () => {
    it('should return a serialized device calibration action', () => {
      const contact = Contact.createFromObject({
        id: '3',
        givenName: 'Nils',
        familyName: 'Brinckmann',
        email: 'nils.brinckmann@gfz-potsdam.de',
        website: '',
        organization: '',
        orcid: '',
        createdByUserId: null,
        createdAt: null,
        updatedAt: null
      })
      const expectedAction = new DeviceCalibrationAction()
      expectedAction.id = '3'
      expectedAction.description = 'Test'
      expectedAction.formula = 'x^2'
      expectedAction.value = 17
      expectedAction.contact = contact
      expectedAction.currentCalibrationDate = DateTime.fromISO('2021-07-01T00:00:00', { zone: 'UTC' })
      expectedAction.nextCalibrationDate = DateTime.fromISO('2021-08-01T00:00:00', { zone: 'UTC' })

      const serializer = new DeviceCalibrationActionSerializer()
      const action = serializer.convertJsonApiObjectToModel(getExampleObjectResponse())

      expect(action).toEqual(expectedAction)
    })
    it('also works with a null next calibration date', () => {
      const contact = Contact.createFromObject({
        id: '3',
        givenName: 'Nils',
        familyName: 'Brinckmann',
        email: 'nils.brinckmann@gfz-potsdam.de',
        website: '',
        organization: '',
        orcid: '',
        createdByUserId: null,
        createdAt: null,
        updatedAt: null
      })
      const expectedAction = new DeviceCalibrationAction()
      expectedAction.id = '3'
      expectedAction.description = 'Test'
      expectedAction.formula = 'x^2'
      expectedAction.value = 17
      expectedAction.contact = contact
      expectedAction.currentCalibrationDate = DateTime.fromISO('2021-07-01T00:00:00', { zone: 'UTC' })
      expectedAction.nextCalibrationDate = null

      const payload = getExampleObjectResponse()
      payload.data.attributes.next_calibration_date = undefined

      const serializer = new DeviceCalibrationActionSerializer()
      const action = serializer.convertJsonApiObjectToModel(payload)

      expect(action).toEqual(expectedAction)
    })
    it('also works with a null value', () => {
      const contact = Contact.createFromObject({
        id: '3',
        givenName: 'Nils',
        familyName: 'Brinckmann',
        email: 'nils.brinckmann@gfz-potsdam.de',
        website: '',
        organization: '',
        orcid: '',
        createdByUserId: null,
        createdAt: null,
        updatedAt: null
      })
      const expectedAction = new DeviceCalibrationAction()
      expectedAction.id = '3'
      expectedAction.description = 'Test'
      expectedAction.formula = 'x^2'
      expectedAction.value = null
      expectedAction.contact = contact
      expectedAction.currentCalibrationDate = DateTime.fromISO('2021-07-01T00:00:00', { zone: 'UTC' })
      expectedAction.nextCalibrationDate = DateTime.fromISO('2021-08-01T00:00:00', { zone: 'UTC' })

      const payload = getExampleObjectResponse()
      payload.data.attributes.value = undefined

      const serializer = new DeviceCalibrationActionSerializer()
      const action = serializer.convertJsonApiObjectToModel(payload)

      expect(action).toEqual(expectedAction)
    })
    it('also works with a zero value', () => {
      const contact = Contact.createFromObject({
        id: '3',
        givenName: 'Nils',
        familyName: 'Brinckmann',
        email: 'nils.brinckmann@gfz-potsdam.de',
        website: '',
        organization: '',
        orcid: '',
        createdByUserId: null,
        createdAt: null,
        updatedAt: null
      })
      const expectedAction = new DeviceCalibrationAction()
      expectedAction.id = '3'
      expectedAction.description = 'Test'
      expectedAction.formula = 'x^2'
      expectedAction.value = 0
      expectedAction.contact = contact
      expectedAction.currentCalibrationDate = DateTime.fromISO('2021-07-01T00:00:00', { zone: 'UTC' })
      expectedAction.nextCalibrationDate = DateTime.fromISO('2021-08-01T00:00:00', { zone: 'UTC' })

      const payload = getExampleObjectResponse()
      payload.data.attributes.value = 0

      const serializer = new DeviceCalibrationActionSerializer()
      const action = serializer.convertJsonApiObjectToModel(payload)

      expect(action).toEqual(expectedAction)
    })
    it('also works with a zero float value', () => {
      const contact = Contact.createFromObject({
        id: '3',
        givenName: 'Nils',
        familyName: 'Brinckmann',
        email: 'nils.brinckmann@gfz-potsdam.de',
        website: '',
        organization: '',
        orcid: '',
        createdByUserId: null,
        createdAt: null,
        updatedAt: null
      })
      const expectedAction = new DeviceCalibrationAction()
      expectedAction.id = '3'
      expectedAction.description = 'Test'
      expectedAction.formula = 'x^2'
      expectedAction.value = 0.0
      expectedAction.contact = contact
      expectedAction.currentCalibrationDate = DateTime.fromISO('2021-07-01T00:00:00', { zone: 'UTC' })
      expectedAction.nextCalibrationDate = DateTime.fromISO('2021-08-01T00:00:00', { zone: 'UTC' })

      const payload = getExampleObjectResponse()
      payload.data.attributes.value = 0.0

      const serializer = new DeviceCalibrationActionSerializer()
      const action = serializer.convertJsonApiObjectToModel(payload)

      expect(action).toEqual(expectedAction)
    })
    it('can also handles associated attachments', () => {
      const contact = Contact.createFromObject({
        id: '3',
        givenName: 'Nils',
        familyName: 'Brinckmann',
        email: 'nils.brinckmann@gfz-potsdam.de',
        website: '',
        organization: '',
        orcid: '',
        createdByUserId: null,
        createdAt: null,
        updatedAt: null
      })
      const attachment1 = Attachment.createFromObject({
        id: '11',
        label: 'UFZ',
        url: 'https://www.ufz.de',
        isUpload: false,
        createdAt: null
      })
      const attachment2 = Attachment.createFromObject({
        id: '22',
        label: 'GFZ',
        url: 'https://www.gfz-potsdam.de',
        isUpload: false,
        createdAt: null
      })
      const expectedAction = new DeviceCalibrationAction()
      expectedAction.id = '3'
      expectedAction.description = 'Test'
      expectedAction.formula = 'x^2'
      expectedAction.value = 17
      expectedAction.contact = contact
      expectedAction.currentCalibrationDate = DateTime.fromISO('2021-07-01T00:00:00', { zone: 'UTC' })
      expectedAction.nextCalibrationDate = DateTime.fromISO('2021-08-01T00:00:00', { zone: 'UTC' })
      expectedAction.attachments = [attachment1, attachment2]

      const payload = getExampleObjectResponse()
      payload.data.relationships = {
        ...payload.data.relationships,
        device_calibration_attachments: {
          data: [
            {
              type: 'device_calibration_attachment',
              id: '1'
            },
            {
              type: 'device_calibration_attachment',
              id: '2'
            }
          ]
        }
      }
      payload.included?.push({
        type: 'device_calibration_attachment',
        id: '1',
        relationships: {
          action: {
            data: {
              type: 'device_calibration_action',
              id: '3'
            }
          },
          attachment: {
            data: {
              type: 'device_attachment',
              id: '11'
            }
          }
        }
      })
      payload.included?.push({
        type: 'device_calibration_attachment',
        id: '2',
        relationships: {
          action: {
            data: {
              type: 'device_calibration_action',
              id: '3'
            }
          },
          attachment: {
            data: {
              type: 'device_attachment',
              id: '22'
            }
          }
        }
      })
      payload.included?.push({
        type: 'device_attachment',
        id: '11',
        attributes: {
          label: 'UFZ',
          url: 'https://www.ufz.de'
        },
        relationships: {
          device: {
            data: {
              type: 'device',
              id: '3'
            }
          }
        }
      })
      payload.included?.push({
        type: 'device_attachment',
        id: '22',
        attributes: {
          label: 'GFZ',
          url: 'https://www.gfz-potsdam.de'
        },
        relationships: {
          device: {
            data: {
              type: 'device',
              id: '3'
            }
          }
        }
      })
      const serializer = new DeviceCalibrationActionSerializer()
      const action = serializer.convertJsonApiObjectToModel(payload)

      expect(action).toEqual(expectedAction)
    })
    it('can also handles associated device properties', () => {
      const contact = Contact.createFromObject({
        id: '3',
        givenName: 'Nils',
        familyName: 'Brinckmann',
        email: 'nils.brinckmann@gfz-potsdam.de',
        website: '',
        organization: '',
        orcid: '',
        createdByUserId: null,
        createdAt: null,
        updatedAt: null
      })
      const measuredQuantity1 = DeviceProperty.createFromObject({
        id: '111',
        label: 'MQ 1',
        compartmentName: 'C1',
        compartmentUri: 'C/1',
        samplingMediaName: 'S1',
        samplingMediaUri: 'S/1',
        propertyName: 'P1',
        propertyUri: 'P/1',
        unitName: 'U1',
        unitUri: 'U/1',
        failureValue: -999,
        accuracy: 0.1,
        measuringRange: {
          min: -1,
          max: 1
        },
        resolution: 0.5,
        resolutionUnitName: 'RU1',
        resolutionUnitUri: 'RU/1'
      })
      const measuredQuantity2 = DeviceProperty.createFromObject({
        id: '222',
        label: 'MQ 2',
        compartmentName: 'C2',
        compartmentUri: 'C/2',
        samplingMediaName: 'S2',
        samplingMediaUri: 'S/2',
        propertyName: 'P2',
        propertyUri: 'P/2',
        unitName: 'U2',
        unitUri: 'U/2',
        failureValue: -998,
        accuracy: 0.5,
        measuringRange: {
          min: -5,
          max: 5
        },
        resolution: 0.05,
        resolutionUnitName: 'RU2',
        resolutionUnitUri: 'RU/2'
      })
      const expectedAction = new DeviceCalibrationAction()
      expectedAction.id = '3'
      expectedAction.description = 'Test'
      expectedAction.formula = 'x^2'
      expectedAction.value = 17
      expectedAction.contact = contact
      expectedAction.currentCalibrationDate = DateTime.fromISO('2021-07-01T00:00:00', { zone: 'UTC' })
      expectedAction.nextCalibrationDate = DateTime.fromISO('2021-08-01T00:00:00', { zone: 'UTC' })
      expectedAction.measuredQuantities = [measuredQuantity1, measuredQuantity2]

      const payload = getExampleObjectResponse()
      payload.data.relationships = {
        ...payload.data.relationships,
        device_property_calibrations: {
          data: [
            {
              type: 'device_property_calibration',
              id: '1'
            },
            {
              type: 'device_property_calibration',
              id: '2'
            }
          ]
        }
      }
      payload.included?.push({
        type: 'device_property_calibration',
        id: '1',
        relationships: {
          calibration_action: {
            data: {
              type: 'device_calibration_action',
              id: '3'
            }
          },
          device_property: {
            data: {
              type: 'device_property',
              id: '111'
            }
          }
        }
      })
      payload.included?.push({
        type: 'device_property_calibration',
        id: '2',
        relationships: {
          calibration_action: {
            data: {
              type: 'device_calibration_action',
              id: '3'
            }
          },
          device_property: {
            data: {
              type: 'device_property',
              id: '222'
            }
          }
        }
      })
      payload.included?.push({
        type: 'device_property',
        id: '111',
        attributes: {
          label: 'MQ 1',
          compartment_name: 'C1',
          compartment_uri: 'C/1',
          sampling_media_name: 'S1',
          sampling_media_uri: 'S/1',
          property_name: 'P1',
          property_uri: 'P/1',
          unit_name: 'U1',
          unit_uri: 'U/1',
          failure_value: -999,
          accuracy: 0.1,
          measuring_range_min: -1,
          measuring_range_max: 1,
          resolution: 0.5,
          resolution_unit_name: 'RU1',
          resolution_unit_uri: 'RU/1'
        },
        relationships: {
          device: {
            data: {
              type: 'device',
              id: '3'
            }
          }
        }
      })
      payload.included?.push({
        type: 'device_property',
        id: '222',
        attributes: {
          label: 'MQ 2',
          compartment_name: 'C2',
          compartment_uri: 'C/2',
          sampling_media_name: 'S2',
          sampling_media_uri: 'S/2',
          property_name: 'P2',
          property_uri: 'P/2',
          unit_name: 'U2',
          unit_uri: 'U/2',
          failure_value: -998,
          accuracy: 0.5,
          measuring_range_min: -5,
          measuring_range_max: 5,
          resolution: 0.05,
          resolution_unit_name: 'RU2',
          resolution_unit_uri: 'RU/2'
        },
        relationships: {
          device: {
            data: {
              type: 'device',
              id: '3'
            }
          }
        }
      })
      const serializer = new DeviceCalibrationActionSerializer()
      const action = serializer.convertJsonApiObjectToModel(payload)

      expect(action).toEqual(expectedAction)
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should return a JSON API representation from a device calibration action model', () => {
      const contact = Contact.createFromObject({
        id: '3',
        givenName: 'Nils',
        familyName: 'Brinckmann',
        email: 'nils.brinckmann@gfz-potsdam.de',
        website: '',
        organization: '',
        orcid: '',
        createdByUserId: null,
        createdAt: null,
        updatedAt: null
      })
      const action = new DeviceCalibrationAction()
      action.id = '3'
      action.description = 'Test'
      action.formula = 'x^2'
      action.value = 17
      action.contact = contact
      action.currentCalibrationDate = DateTime.fromISO('2021-07-01T00:00:00', { zone: 'UTC' })
      action.nextCalibrationDate = DateTime.fromISO('2021-08-01T00:00:00', { zone: 'UTC' })

      const expectedApiModel: IJsonApiEntityWithOptionalId = {
        type: 'device_calibration_action',
        id: '3',
        attributes: {
          description: 'Test',
          formula: 'x^2',
          value: 17,
          current_calibration_date: '2021-07-01T00:00:00.000Z',
          next_calibration_date: '2021-08-01T00:00:00.000Z'
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
              id: '3'
            }
          }
        }
      }

      const serializer = new DeviceCalibrationActionSerializer()
      const apiModel = serializer.convertModelToJsonApiData(action, '204')

      expect(apiModel).toEqual(expectedApiModel)
    })
    it('should also handle a non existing value', () => {
      const contact = Contact.createFromObject({
        id: '3',
        givenName: 'Nils',
        familyName: 'Brinckmann',
        email: 'nils.brinckmann@gfz-potsdam.de',
        website: '',
        organization: '',
        orcid: '',
        createdByUserId: null,
        createdAt: null,
        updatedAt: null
      })
      const action = new DeviceCalibrationAction()
      action.id = '3'
      action.description = 'Test'
      action.formula = 'x^2'
      action.value = null
      action.contact = contact
      action.currentCalibrationDate = DateTime.fromISO('2021-07-01T00:00:00', { zone: 'UTC' })
      action.nextCalibrationDate = DateTime.fromISO('2021-08-01T00:00:00', { zone: 'UTC' })

      const expectedApiModel: IJsonApiEntityWithOptionalId = {
        type: 'device_calibration_action',
        id: '3',
        attributes: {
          description: 'Test',
          formula: 'x^2',
          value: null,
          current_calibration_date: '2021-07-01T00:00:00.000Z',
          next_calibration_date: '2021-08-01T00:00:00.000Z'
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
              id: '3'
            }
          }
        }
      }

      const serializer = new DeviceCalibrationActionSerializer()
      const apiModel = serializer.convertModelToJsonApiData(action, '204')

      expect(apiModel).toEqual(expectedApiModel)
    })
    it('should also handle a 0 value', () => {
      const contact = Contact.createFromObject({
        id: '3',
        givenName: 'Nils',
        familyName: 'Brinckmann',
        email: 'nils.brinckmann@gfz-potsdam.de',
        website: '',
        organization: '',
        orcid: '',
        createdByUserId: null,
        createdAt: null,
        updatedAt: null
      })
      const action = new DeviceCalibrationAction()
      action.id = '3'
      action.description = 'Test'
      action.formula = 'x^2'
      action.value = 0
      action.contact = contact
      action.currentCalibrationDate = DateTime.fromISO('2021-07-01T00:00:00', { zone: 'UTC' })
      action.nextCalibrationDate = DateTime.fromISO('2021-08-01T00:00:00', { zone: 'UTC' })

      const expectedApiModel: IJsonApiEntityWithOptionalId = {
        type: 'device_calibration_action',
        id: '3',
        attributes: {
          description: 'Test',
          formula: 'x^2',
          value: 0,
          current_calibration_date: '2021-07-01T00:00:00.000Z',
          next_calibration_date: '2021-08-01T00:00:00.000Z'
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
              id: '3'
            }
          }
        }
      }

      const serializer = new DeviceCalibrationActionSerializer()
      const apiModel = serializer.convertModelToJsonApiData(action, '204')

      expect(apiModel).toEqual(expectedApiModel)
    })
    it('should also handle the model without the next calibration date', () => {
      const contact = Contact.createFromObject({
        id: '3',
        givenName: 'Nils',
        familyName: 'Brinckmann',
        email: 'nils.brinckmann@gfz-potsdam.de',
        website: '',
        organization: '',
        orcid: '',
        createdByUserId: null,
        createdAt: null,
        updatedAt: null
      })
      const action = new DeviceCalibrationAction()
      action.id = '3'
      action.description = 'Test'
      action.formula = 'x^2'
      action.value = 17
      action.contact = contact
      action.currentCalibrationDate = DateTime.fromISO('2021-07-01T00:00:00', { zone: 'UTC' })
      action.nextCalibrationDate = null

      const expectedApiModel: IJsonApiEntityWithOptionalId = {
        type: 'device_calibration_action',
        id: '3',
        attributes: {
          description: 'Test',
          formula: 'x^2',
          value: 17,
          current_calibration_date: '2021-07-01T00:00:00.000Z',
          next_calibration_date: null
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
              id: '3'
            }
          }
        }
      }

      const serializer = new DeviceCalibrationActionSerializer()
      const apiModel = serializer.convertModelToJsonApiData(action, '204')

      expect(apiModel).toEqual(expectedApiModel)
    })
  })
})
