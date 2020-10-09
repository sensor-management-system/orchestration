import Contact from '@/models/Contact'
import Device from '@/models/Device'
import DeviceSerializer from '@/serializers/jsonapi/DeviceSerializer'
import { Attachment } from '@/models/Attachment'
import { DeviceProperty } from '@/models/DeviceProperty'
import { MeasuringRange } from '@/models/MeasuringRange'
import { CustomTextField } from '@/models/CustomTextField'

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
  device.createdAt = new Date('2020-08-28T13:49:48.015620+00:00')
  device.updatedAt = new Date('2020-08-30T13:49:48.015620+00:00')

  device.customFields = [
    CustomTextField.createFromObject({
      id: '1',
      key: 'First custom field',
      value: 'First custom value'
    }),
    CustomTextField.createFromObject({
      id: null,
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
      id: null,
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
      failureValue: -999
    }),
    DeviceProperty.createFromObject({
      id: null,
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
      failureValue: null
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
            properties: [],
            device_type_name: 'Logger',
            model: 'CR 1000',
            description: '',
            attachments: [],
            status_uri: null,
            website: '',
            updated_at: '2020-08-28T13:49:48.015620+00:00',
            long_name: 'Campbell CR1000 logger unit',
            created_at: '2020-08-28T13:49:48.015620+00:00',
            inventory_number: '',
            manufacturer_name: 'Campbell Scientific',
            device_type_uri: 'Logger',
            customfields: [],
            short_name: 'Campbell CR1000 logger unit',
            status_name: null,
            dual_use: false,
            persistent_identifier: null,
            manufacturer_uri: null
          },
          relationships: {
            updated_by: {
              links: {
                self: '/rdm/svm-api/v1/devices/46/relationships/updatedUser'
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
                self: '/rdm/svm-api/v1/devices/46/relationships/createdUser'
              }
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
            properties: [],
            device_type_name: 'Logger',
            model: 'CR 200X',
            description: '',
            attachments: [],
            status_uri: null,
            website: 'https://www.campbellsci.de/cr200x',
            updated_at: '2020-08-28T13:49:47.814134+00:00',
            long_name: 'Campbell CR200X logger unit',
            created_at: '2020-08-28T13:49:47.814134+00:00',
            inventory_number: '',
            manufacturer_name: 'Campbell Scientific',
            device_type_uri: 'Logger',
            customfields: [],
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
      expectedDevice1.updatedAt = new Date('2020-08-28T13:49:48.015620+00:00')
      expectedDevice1.longName = 'Campbell CR1000 logger unit'
      expectedDevice1.createdAt = new Date('2020-08-28T13:49:48.015620+00:00')
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
      expectedDevice2.updatedAt = new Date('2020-08-28T13:49:47.814134+00:00')
      expectedDevice2.longName = 'Campbell CR200X logger unit'
      expectedDevice2.createdAt = new Date('2020-08-28T13:49:47.814134+00:00')
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
      const devices = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)

      expect(Array.isArray(devices)).toBeTruthy()
      expect(devices.length).toEqual(2)

      expect(devices[0]).toEqual(expectedDevice1)
      expect(devices[1]).toEqual(expectedDevice2)
    })
  })
  describe('#convertJsonApiObjectToModel', () => {
    it('should convert a json api object to a device model', () => {
      const jsonApiObject: any = {
        data: {
          type: 'device',
          attributes: {
            serial_number: '0000001',
            properties: [],
            device_type_name: null,
            model: 'test model',
            description: 'My first test device',
            attachments: [{
              label: 'test label',
              url: 'http://test.test',
              id: '1'
            }],
            status_uri: null,
            website: null,
            updated_at: '2020-08-28T13:00:46.295058+00:00',
            long_name: 'Device long name',
            created_at: '2020-08-28T13:00:46.295058+00:00',
            inventory_number: '0000001',
            manufacturer_name: null,
            device_type_uri: null,
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
      expectedDevice.attachments = [Attachment.createFromObject({
        label: 'test label',
        url: 'http://test.test',
        id: '1'
      })]
      expectedDevice.statusUri = ''
      expectedDevice.website = ''
      expectedDevice.updatedAt = new Date('2020-08-28T13:00:46.295058+00:00')
      expectedDevice.longName = 'Device long name'
      expectedDevice.createdAt = new Date('2020-08-28T13:00:46.295058+00:00')
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
      const device = serializer.convertJsonApiObjectToModel(jsonApiObject)

      expect(device).toEqual(expectedDevice)
    })
    it('should convert also a device with information for contacts, customFields & properties', () => {
      const jsonApiObject: any = {
        data: {
          type: 'device',
          attributes: {
            serial_number: '0000001',
            properties: [{
              compartment_name: 'Climate',
              unit_uri: '',
              sampling_media_name: 'Other',
              compartment_uri: 'variabletype/Climate',
              property_name: 'Water vapor concentration',
              accuracy: null,
              measuring_range_min: null,
              measuring_range_max: null,
              label: 'water vapor',
              property_uri: 'variablename/Water%20vapor%20concentration',
              id: '39',
              unit_name: '',
              failure_value: null,
              sampling_media_uri: 'medium/Other'
            }, {
              compartment_name: 'a',
              unit_uri: 'b',
              sampling_media_name: 'c',
              compartment_uri: 'd',
              property_name: 'e',
              accuracy: 1,
              measuring_range_min: 2,
              measuring_range_max: 3,
              label: 'f',
              property_uri: 'g',
              id: '40',
              unit_name: 'j',
              failure_value: 4,
              sampling_media_uri: 'k'
            }],
            device_type_name: null,
            model: 'test model',
            description: 'My first test device',
            attachments: [{
              label: 'test label',
              url: 'http://test.test',
              id: '1'
            }],
            status_uri: null,
            website: null,
            updated_at: '2020-08-28T13:00:46.295058+00:00',
            long_name: 'Device long name',
            created_at: '2020-08-28T13:00:46.295058+00:00',
            inventory_number: '0000001',
            manufacturer_name: null,
            device_type_uri: null,
            customfields: [{
              id: '44',
              key: 'a',
              value: 'b'
            }],
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
        included: [{
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
        }],
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
          samplingMediaUri: 'medium/Other'
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
          samplingMediaUri: 'k'
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
      expectedDevice.updatedAt = new Date('2020-08-28T13:00:46.295058+00:00')
      expectedDevice.longName = 'Device long name'
      expectedDevice.createdAt = new Date('2020-08-28T13:00:46.295058+00:00')
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
      const device = serializer.convertJsonApiObjectToModel(jsonApiObject)

      expect(device).toEqual(expectedDevice)
    })
  })
  describe('#convertJsonApiDataToModel', () => {
    it('should convert a json api data to a device model', () => {
      const jsonApiData: any = {
        type: 'device',
        attributes: {
          serial_number: '0000001',
          properties: [],
          device_type_name: null,
          model: 'test model',
          description: 'My first test device',
          attachments: [{
            label: 'test label',
            url: 'http://test.test',
            id: '1'
          }],
          status_uri: null,
          website: null,
          updated_at: '2020-08-28T13:00:46.295058+00:00',
          long_name: 'Device long name',
          created_at: '2020-08-28T13:00:46.295058+00:00',
          inventory_number: '0000001',
          manufacturer_name: null,
          device_type_uri: null,
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
      expectedDevice.updatedAt = new Date('2020-08-28T13:00:46.295058+00:00')
      expectedDevice.longName = 'Device long name'
      expectedDevice.createdAt = new Date('2020-08-28T13:00:46.295058+00:00')
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
      const device = serializer.convertJsonApiDataToModel(jsonApiData, included)

      expect(device).toEqual(expectedDevice)
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
          updated_at: '2020-08-28T13:00:46.295058+00:00',
          long_name: 'Device long name',
          created_at: '2020-08-28T13:00:46.295058+00:00',
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
      expectedDevice.attachments = [Attachment.createFromObject({
        label: 'test label',
        url: 'http://test.test',
        id: '1'
      })]
      expectedDevice.statusUri = ''
      expectedDevice.website = ''
      expectedDevice.updatedAt = new Date('2020-08-28T13:00:46.295058+00:00')
      expectedDevice.longName = 'Device long name'
      expectedDevice.createdAt = new Date('2020-08-28T13:00:46.295058+00:00')
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
      const device = serializer.convertJsonApiDataToModel(jsonApiData, included)

      expect(device).toEqual(expectedDevice)
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
      expect(attributes).toHaveProperty('created_at')
      // expect(attributes.created_at).toEqual('2020-08-28T13:49:48.015620+00:00')
      // I wasn't able to find the exact date time format, so we use ISO date times
      expect(attributes.created_at).toEqual('2020-08-28T13:49:48.015Z')
      expect(attributes).toHaveProperty('updated_at')
      // expect(attributes.updated_at).toEqual('2020-08-30T13:49:48.015620+00:00')
      // again, iso date times
      expect(attributes.updated_at).toEqual('2020-08-30T13:49:48.015Z')

      expect(attributes).toHaveProperty('customfields')
      const customfields = attributes.customfields
      expect(Array.isArray(customfields)).toBeTruthy()
      expect(customfields.length).toEqual(2)
      expect(customfields[0]).toEqual({
        id: '1',
        key: 'First custom field',
        value: 'First custom value'
      })
      expect(customfields[1]).toEqual({
        key: 'Second custom field',
        value: ''
      })

      expect(attributes).toHaveProperty('attachments')
      const attachments = attributes.attachments
      expect(Array.isArray(attachments)).toBeTruthy()
      expect(attachments.length).toEqual(2)
      expect(attachments[0]).toEqual({
        id: '2',
        label: 'GFZ',
        url: 'http://www.gfz-potsdam.de'
      })
      expect(attachments[1]).toEqual({
        label: 'UFZ',
        url: 'http://www.ufz.de'
      })

      expect(attributes).toHaveProperty('properties')
      const properties = attributes.properties
      expect(Array.isArray(properties)).toBeTruthy()
      expect(properties[0]).toEqual({
        id: '3',
        label: 'Prop 1',
        compartment_uri: 'compartment/Comp1',
        compartment_name: 'Comp 1',
        unit_uri: 'unit/Unit1',
        unit_name: 'Unit 1',
        sampling_media_uri: 'medium/Medium1',
        sampling_media_name: 'Medium 1',
        property_uri: 'property/Prop1',
        property_name: 'Property 1',
        measuring_range_min: -7,
        measuring_range_max: 7,
        accuracy: 0.5,
        failure_value: -999
      })
      expect(properties[1]).toEqual({
        label: 'Prop 2',
        compartment_uri: '',
        compartment_name: '',
        unit_uri: '',
        unit_name: '',
        sampling_media_uri: '',
        sampling_media_name: '',
        property_uri: '',
        property_name: '',
        measuring_range_min: null,
        measuring_range_max: null,
        accuracy: null,
        failure_value: null
      })

      expect(jsonApiData).toHaveProperty('relationships')
      expect(typeof jsonApiData.relationships).toEqual('object')
      expect(jsonApiData.relationships).toHaveProperty('contacts')
      expect(typeof jsonApiData.relationships.contacts).toBe('object')
      expect(jsonApiData.relationships.contacts).toHaveProperty('data')
      const contactData = jsonApiData.relationships.contacts.data
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
