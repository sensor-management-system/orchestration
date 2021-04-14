/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
 * - Kotyba Alhaj Taha (UFZ, kotyba.alhaj-taha@ufz.de)
 * - Nils Brinckmann (GFZ, nils.brinckmann@gfz-potsdam.de)
 * - Marc Hanisch (GFZ, marc.hanisch@gfz-potsdam.de)
 * - Helmholtz Centre for Environmental Research GmbH - UFZ
 * (UFZ, https://www.ufz.de)
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
import { Contact } from '@/models/Contact'
import { Device } from '@/models/Device'
import {
  DeviceSerializer,
  deviceWithMetaToDeviceByAddingDummyObjects,
  deviceWithMetaToDeviceByThrowingErrorOnMissing,
  IDeviceWithMeta
} from '@/serializers/jsonapi/DeviceSerializer'
import { Attachment } from '@/models/Attachment'
import { DeviceProperty } from '@/models/DeviceProperty'
import { MeasuringRange } from '@/models/MeasuringRange'
import { CustomTextField } from '@/models/CustomTextField'
import { IJsonApiTypeIdDataList } from '@/serializers/jsonapi/JsonApiTypes'

const createTestDevice = () => {
  const device = new Device()
  device.description = 'This is a dummy description'
  device.shortName = 'Dummy short name'
  device.longName = 'Dummy long long long name'
  device.serialNumber = '12345'
  device.inventoryNumber = '6789'
  device.manufacturerUri = 'manufacturer/manu1'
  device.manufacturerName = 'Manu1'
  device.deviceTypeUri = 'deviceType/typeA'
  device.deviceTypeName = 'Type A'
  device.statusUri = 'status/Ok'
  device.statusName = 'Okay'
  device.model = '0815'
  device.persistentIdentifier = 'doi:4354545'
  device.website = 'http://gfz-potsdam.de'
  device.dualUse = true
  device.createdAt = DateTime.utc(2020, 8, 28, 13, 49, 48, 15)
  device.updatedAt = DateTime.utc(2020, 8, 30, 13, 49, 48, 15)

  device.customFields = [
    CustomTextField.createFromObject({
      id: '1',
      key: 'First custom field',
      value: 'First custom value'
    }),
    CustomTextField.createFromObject({
      id: '2',
      key: 'Second custom field',
      value: ''
    })
  ]

  device.attachments = [
    Attachment.createFromObject({
      id: '2',
      label: 'GFZ',
      url: 'http://www.gfz-potsdam.de'
    }),
    Attachment.createFromObject({
      id: '1',
      label: 'UFZ',
      url: 'http://www.ufz.de'
    })
  ]

  device.properties = [
    DeviceProperty.createFromObject({
      id: '3',
      label: 'Prop 1',
      compartmentUri: 'compartment/Comp1',
      compartmentName: 'Comp 1',
      unitUri: 'unit/Unit1',
      unitName: 'Unit 1',
      samplingMediaUri: 'medium/Medium1',
      samplingMediaName: 'Medium 1',
      propertyUri: 'property/Prop1',
      propertyName: 'Property 1',
      measuringRange: MeasuringRange.createFromObject({
        min: -7,
        max: 7
      }),
      accuracy: 0.5,
      failureValue: -999,
      resolution: 0.001,
      resolutionUnitUri: 'http://foo/unit/1',
      resolutionUnitName: 'mm'
    }),
    DeviceProperty.createFromObject({
      id: '4',
      label: 'Prop 2',
      compartmentUri: '',
      compartmentName: '',
      unitUri: '',
      unitName: '',
      samplingMediaUri: '',
      samplingMediaName: '',
      propertyUri: '',
      propertyName: '',
      measuringRange: MeasuringRange.createFromObject({
        min: null,
        max: null
      }),
      accuracy: null,
      failureValue: null,
      resolution: 0.001,
      resolutionUnitUri: 'http://foo/unit/1',
      resolutionUnitName: 'mm'
    })
  ]

  device.contacts = [
    Contact.createFromObject({
      id: '4',
      givenName: 'Max',
      familyName: 'Mustermann',
      email: 'max@mustermann.de',
      website: ''
    }),
    Contact.createFromObject({
      id: '5',
      givenName: 'Mux',
      familyName: 'Mastermunn',
      email: 'mux@mastermunn.de',
      website: ''
    })
  ]
  return device
}

describe('DeviceSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a json api object with multiple entries to a device model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          type: 'device',
          attributes: {
            serial_number: '',
            device_type_name: 'Logger',
            model: 'CR 1000',
            description: '',
            status_uri: null,
            website: '',
            updated_at: '2020-08-29T13:49:48.015620+00:00',
            long_name: 'Campbell CR1000 logger unit',
            created_at: '2020-08-28T13:49:48.015620+00:00',
            inventory_number: '',
            manufacturer_name: 'Campbell Scientific',
            device_type_uri: 'Logger',
            short_name: 'Campbell CR1000 logger unit',
            status_name: null,
            dual_use: false,
            persistent_identifier: null,
            manufacturer_uri: null
          },
          relationships: {
            updated_by: {
              links: {
                self: '/rdm/svm-api/v1/devices/46/relationships/updated-user'
              }
            },
            contacts: {
              links: {
                self: '/rdm/svm-api/v1/devices/46/relationships/contacts',
                related: '/rdm/svm-api/v1/devices/46/contacts'
              }
            },
            events: {
              links: {
                self: '/rdm/svm-api/v1/devices/46/relationships/events',
                related: '/rdm/svm-api/v1/events?device_id=46'
              }
            },
            created_by: {
              links: {
                self: '/rdm/svm-api/v1/devices/46/relationships/created-user'
              }
            },
            customfields: {
              links: {
                related: '/rdm/svm-api/v1/devices/1/relationships/customfields'
              },
              data: []
            },
            device_properties: {
              links: {
                related: '/rdm/svm-api/v1/devices/1/relationships/device-properties'
              },
              data: []
            },
            device_attachments: {
              links: {
                related: '/rdm/svm-api/v1/devices/1/relationships/device-attachments'
              },
              data: []
            }
          },
          id: '46',
          links: {
            self: '/rdm/svm-api/v1/devices/46'
          }
        }, {
          type: 'device',
          attributes: {
            serial_number: '',
            device_type_name: 'Logger',
            model: 'CR 200X',
            description: '',
            status_uri: null,
            website: 'https://www.campbellsci.de/cr200x',
            updated_at: null,
            long_name: 'Campbell CR200X logger unit',
            created_at: null,
            inventory_number: '',
            manufacturer_name: 'Campbell Scientific',
            device_type_uri: 'Logger',
            short_name: 'Campbell CR200X logger unit',
            status_name: null,
            dual_use: false,
            persistent_identifier: null,
            manufacturer_uri: null
          },
          relationships: {
            updated_by: {
              links: {
                self: '/rdm/svm-api/v1/devices/44/relationships/updatedUser'
              }
            },
            contacts: {
              links: {
                self: '/rdm/svm-api/v1/devices/44/relationships/contacts',
                related: '/rdm/svm-api/v1/devices/44/contacts'
              }
            },
            events: {
              links: {
                self: '/rdm/svm-api/v1/devices/44/relationships/events',
                related: '/rdm/svm-api/v1/events?device_id=44'
              }
            },
            created_by: {
              links: {
                self: '/rdm/svm-api/v1/devices/44/relationships/createdUser'
              }
            }
          },
          id: '44',
          links: {
            self: '/rdm/svm-api/v1/devices/44'
          }
        }],
        links: {
          self: 'http://rz-vm64.gfz-potsdam.de:5000/rdm/svm-api/v1/devices?page%5Bsize%5D=2&filter=%5B%7B%22or%22%3A%5B%7B%22name%22%3A%22short_name%22%2C%22op%22%3A%22ilike%22%2C%22val%22%3A%22%25campbell%25%22%7D%2C%7B%22name%22%3A%22long_name%22%2C%22op%22%3A%22ilike%22%2C%22val%22%3A%22%25cam%25%22%7D%5D%7D%5D&sort=short_name',
          first: 'http://rz-vm64.gfz-potsdam.de:5000/rdm/svm-api/v1/devices?page%5Bsize%5D=2&filter=%5B%7B%22or%22%3A%5B%7B%22name%22%3A%22short_name%22%2C%22op%22%3A%22ilike%22%2C%22val%22%3A%22%25campbell%25%22%7D%2C%7B%22name%22%3A%22long_name%22%2C%22op%22%3A%22ilike%22%2C%22val%22%3A%22%25cam%25%22%7D%5D%7D%5D&sort=short_name',
          last: 'http://rz-vm64.gfz-potsdam.de:5000/rdm/svm-api/v1/devices?page%5Bsize%5D=2&filter=%5B%7B%22or%22%3A%5B%7B%22name%22%3A%22short_name%22%2C%22op%22%3A%22ilike%22%2C%22val%22%3A%22%25campbell%25%22%7D%2C%7B%22name%22%3A%22long_name%22%2C%22op%22%3A%22ilike%22%2C%22val%22%3A%22%25cam%25%22%7D%5D%7D%5D&sort=short_name&page%5Bnumber%5D=7',
          next: 'http://rz-vm64.gfz-potsdam.de:5000/rdm/svm-api/v1/devices?page%5Bsize%5D=2&filter=%5B%7B%22or%22%3A%5B%7B%22name%22%3A%22short_name%22%2C%22op%22%3A%22ilike%22%2C%22val%22%3A%22%25campbell%25%22%7D%2C%7B%22name%22%3A%22long_name%22%2C%22op%22%3A%22ilike%22%2C%22val%22%3A%22%25cam%25%22%7D%5D%7D%5D&sort=short_name&page%5Bnumber%5D=2'
        },
        meta: {
          count: 13
        },
        jsonapi: {
          version: '1.0'
        }
      }
      const expectedDevice1 = new Device()

      expectedDevice1.id = '46'
      expectedDevice1.serialNumber = ''
      expectedDevice1.properties = []
      expectedDevice1.deviceTypeName = 'Logger'
      expectedDevice1.model = 'CR 1000'
      expectedDevice1.description = ''
      expectedDevice1.attachments = []
      expectedDevice1.statusUri = ''
      expectedDevice1.website = ''
      expectedDevice1.updatedAt = DateTime.utc(2020, 8, 29, 13, 49, 48, 15)
      expectedDevice1.longName = 'Campbell CR1000 logger unit'
      expectedDevice1.createdAt = DateTime.utc(2020, 8, 28, 13, 49, 48, 15)
      expectedDevice1.inventoryNumber = ''
      expectedDevice1.manufacturerName = 'Campbell Scientific'
      expectedDevice1.deviceTypeUri = 'Logger'
      expectedDevice1.customFields = []
      expectedDevice1.shortName = 'Campbell CR1000 logger unit'
      expectedDevice1.statusName = ''
      expectedDevice1.dualUse = false
      expectedDevice1.persistentIdentifier = ''
      expectedDevice1.manufacturerUri = ''
      expectedDevice1.contacts = []

      const expectedDevice2 = new Device()
      expectedDevice2.id = '44'
      expectedDevice2.serialNumber = ''
      expectedDevice2.properties = []
      expectedDevice2.deviceTypeName = 'Logger'
      expectedDevice2.model = 'CR 200X'
      expectedDevice2.description = ''
      expectedDevice2.attachments = []
      expectedDevice2.statusUri = ''
      expectedDevice2.website = 'https://www.campbellsci.de/cr200x'
      expectedDevice2.updatedAt = null
      expectedDevice2.longName = 'Campbell CR200X logger unit'
      expectedDevice2.createdAt = null
      expectedDevice2.inventoryNumber = ''
      expectedDevice2.manufacturerName = 'Campbell Scientific'
      expectedDevice2.deviceTypeUri = 'Logger'
      expectedDevice2.customFields = []
      expectedDevice2.shortName = 'Campbell CR200X logger unit'
      expectedDevice2.statusName = ''
      expectedDevice2.dualUse = false
      expectedDevice2.persistentIdentifier = ''
      expectedDevice2.manufacturerUri = ''
      expectedDevice2.contacts = []

      const serializer = new DeviceSerializer()
      const devicesWithMeta = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)
      const devices = devicesWithMeta.map((x: IDeviceWithMeta) => x.device)

      expect(Array.isArray(devices)).toBeTruthy()
      expect(devices.length).toEqual(2)

      expect(devices[0]).toEqual(expectedDevice1)
      expect(devices[1]).toEqual(expectedDevice2)

      const missingContactIds = devicesWithMeta.map((x: IDeviceWithMeta) => {
        return x.missing.contacts.ids
      })

      expect(Array.isArray(missingContactIds)).toBeTruthy()
      expect(missingContactIds.length).toEqual(2)

      expect(missingContactIds[0]).toEqual([])
      expect(missingContactIds[1]).toEqual([])
    })
  })
  describe('#convertJsonApiObjectToModel', () => {
    it('should convert a json api object to a device model', () => {
      const jsonApiObject: any = {
        data: {
          type: 'device',
          attributes: {
            serial_number: '0000001',
            device_type_name: null,
            model: 'test model',
            description: 'My first test device',
            status_uri: null,
            website: null,
            updated_at: '2020-08-28T13:00:46.295058+00:00',
            long_name: 'Device long name',
            created_at: '2020-08-28T13:00:46.295058+00:00',
            inventory_number: '0000001',
            manufacturer_name: null,
            device_type_uri: null,
            short_name: 'Device short name',
            status_name: null,
            dual_use: false,
            persistent_identifier: '0000001',
            manufacturer_uri: null
          },
          relationships: {
            updated_by: {
              links: {
                self: '/rdm/svm-api/v1/devices/1/relationships/updatedUser'
              }
            },
            contacts: {
              links: {
                self: '/rdm/svm-api/v1/devices/1/relationships/contacts',
                related: '/rdm/svm-api/v1/devices/1/contacts'
              }
            },
            events: {
              links: {
                self: '/rdm/svm-api/v1/devices/1/relationships/events',
                related: '/rdm/svm-api/v1/events?device_id=1'
              }
            },
            created_by: {
              links: {
                self: '/rdm/svm-api/v1/devices/1/relationships/createdUser',
                related: '/rdm/svm-api/v1/users/1'
              }
            }
          },
          id: '1',
          links: {
            self: '/rdm/svm-api/v1/devices/1'
          }
        },
        links: {
          self: '/rdm/svm-api/v1/devices/1'
        },
        jsonapi: {
          version: '1.0'
        }
      }
      const expectedDevice = new Device()
      expectedDevice.id = '1'
      expectedDevice.serialNumber = '0000001'
      expectedDevice.properties = []
      expectedDevice.deviceTypeName = ''
      expectedDevice.model = 'test model'
      expectedDevice.description = 'My first test device'
      expectedDevice.attachments = []
      expectedDevice.statusUri = ''
      expectedDevice.website = ''
      expectedDevice.updatedAt = DateTime.utc(2020, 8, 28, 13, 0, 46, 295)
      expectedDevice.longName = 'Device long name'
      expectedDevice.createdAt = DateTime.utc(2020, 8, 28, 13, 0, 46, 295)
      expectedDevice.inventoryNumber = '0000001'
      expectedDevice.manufacturerName = ''
      expectedDevice.deviceTypeUri = ''
      expectedDevice.customFields = []
      expectedDevice.shortName = 'Device short name'
      expectedDevice.statusName = ''
      expectedDevice.dualUse = false
      expectedDevice.persistentIdentifier = '0000001'
      expectedDevice.manufacturerUri = ''
      expectedDevice.contacts = []

      const serializer = new DeviceSerializer()
      const deviceWithMeta = serializer.convertJsonApiObjectToModel(jsonApiObject)
      const device = deviceWithMeta.device

      expect(device).toEqual(expectedDevice)
      expect(deviceWithMeta.missing.contacts.ids).toEqual([])
    })
    it('should convert also a device with information for contacts, customFields & properties', () => {
      const jsonApiObject: any = {
        data: {
          type: 'device',
          attributes: {
            serial_number: '0000001',
            device_type_name: null,
            model: 'test model',
            description: 'My first test device',
            status_uri: null,
            website: null,
            updated_at: '2020-08-28T13:00:46.295058+00:00',
            long_name: 'Device long name',
            created_at: '2020-08-28T13:00:46.295058+00:00',
            inventory_number: '0000001',
            manufacturer_name: null,
            device_type_uri: null,
            short_name: 'Device short name',
            status_name: null,
            dual_use: true,
            persistent_identifier: '0000001',
            manufacturer_uri: null
          },
          relationships: {
            updated_by: {
              links: {
                self: '/rdm/svm-api/v1/devices/1/relationships/updatedUser'
              }
            },
            contacts: {
              links: {
                self: '/rdm/svm-api/v1/devices/1/relationships/contacts',
                related: '/rdm/svm-api/v1/devices/1/contacts'
              },
              data: [{
                type: 'contact',
                id: '1'
              }]
            },
            device_attachments: {
              links: {
                self: '/rdm/svm-api/v1/devices/1/relationships/device-attachments',
                related: '/rdm/svm-api/v1/devices/1/device-attachments'
              },
              data: [{
                type: 'device_attachments',
                id: '1'
              }]
            },
            customfields: {
              links: {
                self: '/rdm/svm-api/v1/devices/1/relationships/customfields',
                related: '/rdm/svm-api/v1/devices/1/customfields'
              },
              data: [{
                type: 'customfield',
                id: '44'
              }]
            },
            device_properties: {
              links: {
                self: '/rdm/svm-api/v1/devices/1/relationships/device-properties',
                related: '/rdm/svm-api/v1/devices/1/device-properties'
              },
              data: [
                {
                  type: 'device_property',
                  id: '39'
                },
                {
                  type: 'device_property',
                  id: '40'
                }]
            },
            events: {
              links: {
                self: '/rdm/svm-api/v1/devices/1/relationships/events',
                related: '/rdm/svm-api/v1/events?device_id=1'
              }
            },
            created_by: {
              links: {
                self: '/rdm/svm-api/v1/devices/1/relationships/createdUser',
                related: '/rdm/svm-api/v1/users/1'
              }
            }
          },
          id: '1',
          links: {
            self: '/rdm/svm-api/v1/devices/1'
          }
        },
        links: {
          self: '/rdm/svm-api/v1/devices/1'
        },
        included: [
          {
            type: 'contact',
            relationships: {
              configurations: {
                links: {
                  self: '/rdm/svm-api/v1/contacts/1/relationships/configurations',
                  related: '/rdm/svm-api/v1/configurations?contact_id=1'
                }
              },
              user: {
                links: {
                  self: '/rdm/svm-api/v1/contacts/1/relationships/user',
                  related: '/rdm/svm-api/v1/contacts/1/users'
                },
                data: {
                  type: 'user',
                  id: '[<User 1>]'
                }
              },
              devices: {
                links: {
                  self: '/rdm/svm-api/v1/contacts/1/relationships/devices',
                  related: '/rdm/svm-api/v1/devices?contact_id=1'
                }
              },
              platforms: {
                links: {
                  self: '/rdm/svm-api/v1/contacts/1/relationships/platforms',
                  related: '/rdm/svm-api/v1/contacts/1/platforms'
                }
              }
            },
            attributes: {
              given_name: 'Max',
              email: 'test@test.test',
              website: null,
              family_name: 'Mustermann'
            },
            id: '1',
            links: {
              self: '/rdm/svm-api/v1/contacts/1'
            }
          },
          {
            type: 'customfield',
            relationships: {
              device: {
                links: {
                  self: '/rdm/svm-api/v1/customfields/1/relationships/device',
                  related: '/rdm/svm-api/v1/devices/1'
                },
                data: {
                  type: 'device',
                  id: '1'
                }
              }
            },
            id: '44',
            attributes: {
              key: 'a',
              value: 'b'
            },
            links: {
              self: '/rdm/svm-api/v1/customfields/44'
            }
          },
          {
            type: 'device_attachment',
            attributes: {
              url: 'http://test.test',
              label: 'test label'
            },
            relationships: {
              device: {
                links: {
                  self: '/rdm/svm-api/v1/device-attachments/1/relationships/device',
                  related: '/rdm/svm-api/v1/devices/3'
                },
                data: {
                  type: 'device',
                  id: '1'
                }
              }
            },
            id: '1',
            links: {
              self: '/rdm/svm-api/v1/device-attachments/1'
            }
          },
          {
            type: 'device_property',
            attributes: {
              measuring_range_min: null,
              label: 'water vapor',
              sampling_media_name: 'Other',
              resolution: 0.001,
              property_uri: 'variablename/Water%20vapor%20concentration',
              measuring_range_max: null,
              unit_name: '',
              compartment_uri: 'variabletype/Climate',
              property_name: 'Water vapor concentration',
              resolution_unit_uri: 'http://foo/unit/1',
              sampling_media_uri: 'medium/Other',
              compartment_name: 'Climate',
              accuracy: null,
              resolution_unit_name: 'mm',
              unit_uri: '',
              failure_value: null
            },
            id: '39',
            relationships: {
              device: {
                links: {
                  self: '/rdm/svm-api/v1/device-properties/2/relationships/device',
                  related: '/rdm/svm-api/v1/devices/4'
                },
                data: {
                  type: 'device',
                  id: '1'
                }
              }
            },
            links: {
              self: '/rdm/svm-api/v1/device-properties/2'
            }
          },
          {
            type: 'device_property',
            attributes: {
              measuring_range_min: 2,
              label: 'f',
              sampling_media_name: 'c',
              resolution: 0.001,
              property_uri: 'g',
              measuring_range_max: 3,
              unit_name: 'j',
              compartment_uri: 'd',
              property_name: 'e',
              resolution_unit_uri: 'http://foo/unit/1',
              sampling_media_uri: 'k',
              compartment_name: 'a',
              accuracy: 1,
              resolution_unit_name: 'mm',
              unit_uri: 'b',
              failure_value: 4
            },
            id: '40',
            relationships: {
              device: {
                links: {
                  self: '/rdm/svm-api/v1/device-properties/2/relationships/device',
                  related: '/rdm/svm-api/v1/devices/4'
                },
                data: {
                  type: 'device',
                  id: '1'
                }
              }
            },
            links: {
              self: '/rdm/svm-api/v1/device-properties/2'
            }
          }
        ],
        jsonapi: {
          version: '1.0'
        }
      }

      const expectedDevice = new Device()
      expectedDevice.id = '1'
      expectedDevice.serialNumber = '0000001'
      expectedDevice.properties = [
        DeviceProperty.createFromObject({
          compartmentName: 'Climate',
          unitUri: '',
          samplingMediaName: 'Other',
          compartmentUri: 'variabletype/Climate',
          propertyName: 'Water vapor concentration',
          accuracy: null,
          measuringRange: MeasuringRange.createFromObject({
            min: null,
            max: null
          }),
          label: 'water vapor',
          propertyUri: 'variablename/Water%20vapor%20concentration',
          id: '39',
          unitName: '',
          failureValue: null,
          samplingMediaUri: 'medium/Other',
          resolution: 0.001,
          resolutionUnitUri: 'http://foo/unit/1',
          resolutionUnitName: 'mm'
        }),
        DeviceProperty.createFromObject({
          compartmentName: 'a',
          unitUri: 'b',
          samplingMediaName: 'c',
          compartmentUri: 'd',
          propertyName: 'e',
          accuracy: 1,
          measuringRange: MeasuringRange.createFromObject({
            min: 2,
            max: 3
          }),
          label: 'f',
          propertyUri: 'g',
          id: '40',
          unitName: 'j',
          failureValue: 4,
          samplingMediaUri: 'k',
          resolution: 0.001,
          resolutionUnitUri: 'http://foo/unit/1',
          resolutionUnitName: 'mm'
        })
      ]
      expectedDevice.deviceTypeName = ''
      expectedDevice.model = 'test model'
      expectedDevice.description = 'My first test device'
      expectedDevice.attachments = [Attachment.createFromObject({
        label: 'test label',
        url: 'http://test.test',
        id: '1'
      })]
      expectedDevice.statusUri = ''
      expectedDevice.website = ''
      expectedDevice.updatedAt = DateTime.utc(2020, 8, 28, 13, 0, 46, 295)
      expectedDevice.longName = 'Device long name'
      expectedDevice.createdAt = DateTime.utc(2020, 8, 28, 13, 0, 46, 295)
      expectedDevice.inventoryNumber = '0000001'
      expectedDevice.manufacturerName = ''
      expectedDevice.deviceTypeUri = ''
      expectedDevice.customFields = [
        CustomTextField.createFromObject({
          key: 'a',
          value: 'b',
          id: '44'
        })
      ]
      expectedDevice.shortName = 'Device short name'
      expectedDevice.statusName = ''
      expectedDevice.dualUse = true
      expectedDevice.persistentIdentifier = '0000001'
      expectedDevice.manufacturerUri = ''
      expectedDevice.contacts = [
        Contact.createFromObject({
          id: '1',
          givenName: 'Max',
          email: 'test@test.test',
          website: '',
          familyName: 'Mustermann'
        })
      ]

      const serializer = new DeviceSerializer()
      const deviceWithMeta = serializer.convertJsonApiObjectToModel(jsonApiObject)
      const device = deviceWithMeta.device
      expect(device).toEqual(expectedDevice)
      expect(deviceWithMeta.missing.contacts.ids).toEqual([])
      expect(deviceWithMeta.missing.deviceAttachments.ids).toEqual([])
      expect(deviceWithMeta.missing.customfields.ids).toEqual([])
      expect(deviceWithMeta.missing.properties.ids).toEqual([])
    })
  })
  describe('#convertJsonApiDataToModel', () => {
    it('should convert a json api data to a device model', () => {
      const jsonApiData: any = {
        type: 'device',
        attributes: {
          serial_number: '0000001',
          device_type_name: null,
          model: 'test model',
          description: 'My first test device',
          status_uri: null,
          website: null,
          updated_at: '2020-08-28T13:00:46.295058+00:00',
          long_name: 'Device long name',
          created_at: '2020-08-28T13:00:46.295058+00:00',
          inventory_number: '0000001',
          manufacturer_name: null,
          device_type_uri: null,
          short_name: 'Device short name',
          status_name: null,
          dual_use: false,
          persistent_identifier: '0000001',
          manufacturer_uri: null
        },
        relationships: {
          updated_by: {
            links: {
              self: '/rdm/svm-api/v1/devices/1/relationships/updatedUser'
            }
          },
          contacts: {
            links: {
              self: '/rdm/svm-api/v1/devices/1/relationships/contacts',
              related: '/rdm/svm-api/v1/devices/1/contacts'
            }
          },
          events: {
            links: {
              self: '/rdm/svm-api/v1/devices/1/relationships/events',
              related: '/rdm/svm-api/v1/events?device_id=1'
            }
          },
          created_by: {
            links: {
              self: '/rdm/svm-api/v1/devices/1/relationships/createdUser',
              related: '/rdm/svm-api/v1/users/1'
            }
          }
        },
        id: '1',
        links: {
          self: '/rdm/svm-api/v1/devices/1'
        }
      }

      const expectedDevice = new Device()
      expectedDevice.id = '1'
      expectedDevice.serialNumber = '0000001'
      expectedDevice.properties = []
      expectedDevice.deviceTypeName = ''
      expectedDevice.model = 'test model'
      expectedDevice.description = 'My first test device'
      expectedDevice.attachments = []
      expectedDevice.statusUri = ''
      expectedDevice.website = ''
      expectedDevice.updatedAt = DateTime.utc(2020, 8, 28, 13, 0, 46, 295)
      expectedDevice.longName = 'Device long name'
      expectedDevice.createdAt = DateTime.utc(2020, 8, 28, 13, 0, 46, 295)
      expectedDevice.inventoryNumber = '0000001'
      expectedDevice.manufacturerName = ''
      expectedDevice.deviceTypeUri = ''
      expectedDevice.customFields = []
      expectedDevice.shortName = 'Device short name'
      expectedDevice.statusName = ''
      expectedDevice.dualUse = false
      expectedDevice.persistentIdentifier = '0000001'
      expectedDevice.manufacturerUri = ''
      expectedDevice.contacts = []

      const included: any[] = []

      const serializer = new DeviceSerializer()
      const deviceWeithMeta = serializer.convertJsonApiDataToModel(jsonApiData, included)
      const device = deviceWeithMeta.device

      expect(device).toEqual(expectedDevice)
      expect(deviceWeithMeta.missing.contacts.ids).toEqual([])
    })
    it('should convert also work with different devicetype name and uri values', () => {
      const jsonApiData: any = {
        type: 'device',
        attributes: {
          serial_number: '0000001',
          properties: [],
          device_type_name: 'type name',
          model: 'test model',
          description: 'My first test device',
          attachments: [{
            label: 'test label',
            url: 'http://test.test',
            id: '1'
          }],
          status_uri: null,
          website: null,
          updated_at: '2020-08-29T13:49:48.015',
          long_name: 'Device long name',
          created_at: '2020-08-28T13:49:48.015',
          inventory_number: '0000001',
          manufacturer_name: null,
          device_type_uri: 'type uri',
          customfields: [],
          short_name: 'Device short name',
          status_name: null,
          dual_use: false,
          persistent_identifier: '0000001',
          manufacturer_uri: null
        },
        relationships: {
          updated_by: {
            links: {
              self: '/rdm/svm-api/v1/devices/1/relationships/updatedUser'
            }
          },
          contacts: {
            links: {
              self: '/rdm/svm-api/v1/devices/1/relationships/contacts',
              related: '/rdm/svm-api/v1/devices/1/contacts'
            }
          },
          events: {
            links: {
              self: '/rdm/svm-api/v1/devices/1/relationships/events',
              related: '/rdm/svm-api/v1/events?device_id=1'
            }
          },
          created_by: {
            links: {
              self: '/rdm/svm-api/v1/devices/1/relationships/createdUser',
              related: '/rdm/svm-api/v1/users/1'
            }
          }
        },
        id: '1',
        links: {
          self: '/rdm/svm-api/v1/devices/1'
        }
      }

      const expectedDevice = new Device()
      expectedDevice.id = '1'
      expectedDevice.serialNumber = '0000001'
      expectedDevice.properties = []
      expectedDevice.deviceTypeName = 'type name'
      expectedDevice.model = 'test model'
      expectedDevice.description = 'My first test device'
      expectedDevice.attachments = []
      expectedDevice.updatedAt = DateTime.utc(2020, 8, 29, 13, 49, 48, 15)
      expectedDevice.createdAt = DateTime.utc(2020, 8, 28, 13, 49, 48, 15)
      expectedDevice.statusUri = ''
      expectedDevice.website = ''
      expectedDevice.longName = 'Device long name'
      expectedDevice.inventoryNumber = '0000001'
      expectedDevice.manufacturerName = ''
      expectedDevice.deviceTypeUri = 'type uri'
      expectedDevice.customFields = []
      expectedDevice.shortName = 'Device short name'
      expectedDevice.statusName = ''
      expectedDevice.dualUse = false
      expectedDevice.persistentIdentifier = '0000001'
      expectedDevice.manufacturerUri = ''
      expectedDevice.contacts = []

      const included: any[] = []

      const serializer = new DeviceSerializer()
      const deviceWithMeta = serializer.convertJsonApiDataToModel(jsonApiData, included)
      const device = deviceWithMeta.device

      expect(device).toEqual(expectedDevice)
      expect(deviceWithMeta.missing.contacts.ids).toEqual([])
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should convert a model to json data object with all of the subelements', () => {
      const device = createTestDevice()

      const serializer = new DeviceSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(device)

      expect(typeof jsonApiData).toEqual('object')

      expect(jsonApiData).not.toHaveProperty('id')

      expect(jsonApiData).toHaveProperty('type')
      expect(jsonApiData.type).toEqual('device')

      expect(jsonApiData).toHaveProperty('attributes')
      const attributes = jsonApiData.attributes
      expect(typeof attributes).toBe('object')

      expect(attributes).toHaveProperty('description')
      expect(attributes.description).toEqual('This is a dummy description')
      expect(attributes).toHaveProperty('short_name')
      expect(attributes.short_name).toEqual('Dummy short name')
      expect(attributes).toHaveProperty('long_name')
      expect(attributes.long_name).toEqual('Dummy long long long name')
      expect(attributes).toHaveProperty('serial_number')
      expect(attributes.serial_number).toEqual('12345')
      expect(attributes).toHaveProperty('inventory_number')
      expect(attributes.inventory_number).toEqual('6789')
      expect(attributes).toHaveProperty('manufacturer_uri')
      expect(attributes.manufacturer_uri).toEqual('manufacturer/manu1')
      expect(attributes).toHaveProperty('manufacturer_name')
      expect(attributes.manufacturer_name).toEqual('Manu1')
      expect(attributes).toHaveProperty('device_type_uri')
      expect(attributes.device_type_uri).toEqual('deviceType/typeA')
      expect(attributes).toHaveProperty('device_type_name')
      expect(attributes.device_type_name).toEqual('Type A')
      expect(attributes).toHaveProperty('status_uri')
      expect(attributes.status_uri).toEqual('status/Ok')
      expect(attributes).toHaveProperty('status_name')
      expect(attributes.status_name).toEqual('Okay')
      expect(attributes).toHaveProperty('model')
      expect(attributes.model).toEqual('0815')
      expect(attributes).toHaveProperty('persistent_identifier')
      expect(attributes.persistent_identifier).toEqual('doi:4354545')
      expect(attributes).toHaveProperty('website')
      expect(attributes.website).toEqual('http://gfz-potsdam.de')
      expect(attributes).toHaveProperty('dual_use')
      expect(attributes.dual_use).toEqual(true)
      // expect(attributes).toHaveProperty('created_at')
      // expect(attributes.created_at).toEqual('2020-08-28T13:49:48.015620+00:00')
      // I wasn't able to find the exact date time format, so we use ISO date times
      // expect(attributes.created_at).toEqual('2020-08-28T13:49:48.015Z')
      // expect(attributes).toHaveProperty('updated_at')
      // expect(attributes.updated_at).toEqual('2020-08-30T13:49:48.015620+00:00')
      // again, iso date times
      // expect(attributes.updated_at).toEqual('2020-08-30T13:49:48.015Z')

      expect(jsonApiData.relationships).toHaveProperty('customfields')
      const customFields = jsonApiData.relationships.customfields as IJsonApiTypeIdDataList
      expect(customFields).toHaveProperty('data')
      const customFieldsData = customFields.data
      expect(Array.isArray(customFieldsData)).toBeTruthy()
      expect(customFieldsData.length).toEqual(2)
      expect(customFieldsData[0]).toEqual({
        id: '1',
        type: 'customfield'
      })
      expect(customFieldsData[1]).toEqual({
        id: '2',
        type: 'customfield'
      })

      expect(jsonApiData.relationships).toHaveProperty('device_attachments')
      const attachments = jsonApiData.relationships.device_attachments as IJsonApiTypeIdDataList
      expect(Array.isArray(attachments.data)).toBeTruthy()

      expect(attachments.data.length).toEqual(2)
      expect(attachments.data[0]).toEqual({
        id: '2',
        type: 'device_attachment'

      })
      expect(attachments.data[1]).toEqual({
        id: '1',
        type: 'device_attachment'
      })

      expect(jsonApiData.relationships).toHaveProperty('device_properties')
      const propertyObject = jsonApiData.relationships.device_properties as IJsonApiTypeIdDataList
      expect(propertyObject).toHaveProperty('data')
      const propertyData = propertyObject.data
      expect(propertyData.length).toEqual(2)
      expect(propertyData[0]).toEqual({
        id: '3',
        type: 'device_property'
      })
      expect(propertyData[1]).toEqual({
        id: '4',
        type: 'device_property'
      })

      expect(jsonApiData).toHaveProperty('relationships')
      expect(typeof jsonApiData.relationships).toEqual('object')
      expect(jsonApiData.relationships).toHaveProperty('contacts')
      expect(typeof jsonApiData.relationships.contacts).toBe('object')
      // we test for the inner structure of the result anyway
      // this cast is just to tell typescript that
      // we have an array of data, so that it doesn't show
      // typeerrors here
      const contactObject = jsonApiData.relationships.contacts as IJsonApiTypeIdDataList
      expect(contactObject).toHaveProperty('data')
      const contactData = contactObject.data
      expect(Array.isArray(contactData)).toBeTruthy()
      expect(contactData.length).toEqual(2)
      expect(contactData[0]).toEqual({
        id: '4',
        type: 'contact'
      })
      expect(contactData[1]).toEqual({
        id: '5',
        type: 'contact'
      })
    })
    it('should serialize an empty string as persistent identifier as null', () => {
      const device = createTestDevice()
      device.persistentIdentifier = ''

      const serializer = new DeviceSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(device)

      expect(typeof jsonApiData).toEqual('object')
      expect(jsonApiData).toHaveProperty('attributes')
      const attributes = jsonApiData.attributes
      expect(typeof attributes).toBe('object')
      expect(attributes).toHaveProperty('persistent_identifier')
      expect(attributes.persistent_identifier).toBeNull()
    })
    it('should set an id if given for the device', () => {
      const device = createTestDevice()
      device.id = 'abc'

      const serializer = new DeviceSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(device)

      expect(typeof jsonApiData).toEqual('object')
      expect(jsonApiData).toHaveProperty('id')
      expect(jsonApiData.id).toEqual('abc')
    })
  })
})
describe('deviceWithMetaToDeviceByThrowingErrorOnMissing', () => {
  it('should work without missing data', () => {
    const device = new Device()
    const missing = {
      contacts: {
        ids: []
      }
    }

    const result = deviceWithMetaToDeviceByThrowingErrorOnMissing({
      device,
      missing
    })

    expect(result).toEqual(device)
    expect(result.contacts).toEqual([])
  })
  it('should also work if there is an contact', () => {
    const device = new Device()
    const contact = Contact.createFromObject({
      id: '1',
      familyName: 'Mustermann',
      givenName: 'Max',
      website: '',
      email: 'max@mustermann.de'
    })
    device.contacts.push(contact)

    const missing = {
      contacts: {
        ids: []
      }
    }

    const result = deviceWithMetaToDeviceByThrowingErrorOnMissing({
      device,
      missing
    })

    expect(result).toEqual(device)
    expect(result.contacts).toEqual([contact])
  })
  it('should throw an error if there are missing data', () => {
    const device = new Device()
    const missing = {
      contacts: {
        ids: ['1']
      }
    }

    try {
      deviceWithMetaToDeviceByThrowingErrorOnMissing({
        device,
        missing
      })
      fail('There must be an error')
    } catch (error) {
      expect(error.toString()).toMatch(/Contacts are missing/)
    }
  })
})
describe('deviceWithMetaToDeviceByAddingDummyObjects', () => {
  it('should leave the data as it is if there are no missing data', () => {
    const device = new Device()
    const missing = {
      contacts: {
        ids: []
      }
    }

    const result = deviceWithMetaToDeviceByAddingDummyObjects({
      device,
      missing
    })

    expect(result).toEqual(device)
    expect(result.contacts).toEqual([])
  })
  it('should stay with existing contacts without adding dummy data', () => {
    const device = new Device()
    const contact = Contact.createFromObject({
      id: '1',
      familyName: 'Mustermann',
      givenName: 'Max',
      website: '',
      email: 'max@mustermann.de'
    })
    device.contacts.push(contact)
    const missing = {
      contacts: {
        ids: []
      }
    }

    const result = deviceWithMetaToDeviceByAddingDummyObjects({
      device,
      missing
    })

    expect(result).toEqual(device)
    expect(result.contacts).toEqual([contact])
  })
  it('should add a dummy contact if there are missing data', () => {
    const device = new Device()

    const missing = {
      contacts: {
        ids: ['2']
      }
    }

    const newExpectedContact = new Contact()
    newExpectedContact.id = '2'

    const result = deviceWithMetaToDeviceByAddingDummyObjects({
      device,
      missing
    })

    expect(result.contacts).toEqual([newExpectedContact])
  })
  it('should also add a dummy contact if there are contact data - together with the missing', () => {
    const device = new Device()
    const contact = Contact.createFromObject({
      id: '1',
      familyName: 'Mustermann',
      givenName: 'Max',
      website: '',
      email: 'max@mustermann.de'
    })
    device.contacts.push(contact)

    const missing = {
      contacts: {
        ids: ['2']
      }
    }

    const newExpectedContact = new Contact()
    newExpectedContact.id = '2'

    const result = deviceWithMetaToDeviceByAddingDummyObjects({
      device,
      missing
    })

    expect(result.contacts).toEqual([contact, newExpectedContact])
  })
})
