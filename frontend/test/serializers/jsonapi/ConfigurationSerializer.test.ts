/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020-2024
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

import { Configuration } from '@/models/Configuration'
import { Contact } from '@/models/Contact'

import {
  IJsonApiEntityWithoutDetailsDataDict,
  IJsonApiEntityWithoutDetailsDataDictList
} from '@/serializers/jsonapi/JsonApiTypes'

import {
  ConfigurationSerializer,
  IConfigurationWithMeta,
  configurationWithMetaToConfigurationByThrowingErrorOnMissing,
  configurationWithMetaToConfigurationByAddingDummyObjects
} from '@/serializers/jsonapi/ConfigurationSerializer'

describe('ConfigurationSerializer', () => {
  describe('#convertJsonApiObjectListToModelList', () => {
    it('should convert a json api object with multiple entries to a configuration model list', () => {
      const jsonApiObjectList: any = {
        data: [{
          type: 'configuration',
          attributes: {
            start_date: '2020-08-28T13:49:48.015620+00:00',
            end_date: '2020-08-29T13:49:48.015620+00:00',
            label: 'Tereno NO Boeken',
            description: 'Boeken station',
            project: 'Tereno NO',
            status: 'draft',
            archived: true,
            persistent_identifier: '12345/1234567890',
            keywords: ['key', 'word']
          },
          relationships: {
            created_by: {
              data: {
                id: '123456',
                type: 'user'
              }
            }
            // no contacts, as we expect an empty case here
          },
          id: '1'
        }, {
          type: 'configuration',
          attributes: {
            // no start and no end date
            // no field for label, none for description, nor project
            status: 'draft',
            archived: false,
            persistent_identifier: null
          },
          relationships: {
            // no contacts, as we expect an empty case here
            // and handle device properties somehow
          },
          id: '2'
        }, {
          type: 'configuration',
          attributes: {},
          relationships: {},
          id: '3'
        }, {
          type: 'configuration',
          attributes: {
            // no label, no start nor end
          },
          relationships: {},
          id: '4'
        }],
        included: [
          {
            type: 'device_property',
            id: '100',
            attributes: {
              sampling_media_name: 'Air',
              sampling_media_uri: 'medium/air',
              compartment_name: 'C1',
              compartment_uri: 'compartment/c1',
              property_name: 'Temperature',
              property_uri: 'property/temperature',
              unit_name: 'degree',
              unit_uri: 'unit/degree',
              failure_value: -999,
              measuring_range_min: -273,
              measuring_range_max: 100,
              label: 'air_temperature',
              accuracy: 0.1,
              resolution: 0.05,
              resolution_unit_name: 'TemperatureRes',
              resolution_unit_uri: 'property/res/temperature'
            },
            relationships: {
              device: {
                data: {
                  type: 'device',
                  // just an example device included already for the
                  // mount actions
                  id: '39'
                }
              }
            }
          },
          {
            type: 'device_property',
            id: '101',
            attributes: {
              sampling_media_name: 'Water',
              sampling_media_uri: 'medium/water',
              compartment_name: 'C1',
              compartment_uri: 'compartment/c1',
              property_name: 'Temperature',
              property_uri: 'property/temperature',
              unit_name: 'degree',
              unit_uri: 'unit/degree',
              failure_value: -999,
              measuring_range_min: -10,
              measuring_range_max: 100,
              label: 'water_temperature',
              accuracy: 0.1,
              resolution: 0.05,
              resolution_unit_name: 'TemperatureRes',
              resolution_unit_uri: 'property/res/temperature'
            },
            relationships: {
              device: {
                data: {
                  type: 'device',
                  // just an example device included already for the
                  // mount actions
                  id: '39'
                }
              }
            }
          },
          {
            type: 'contact',
            id: '1',
            attributes: {
              given_name: 'Max',
              family_name: 'Mustermann',
              email: 'max@mustermann.xyz',
              website: ''
            }
          },
          {
            type: 'device',
            id: '39',
            attributes: {
              inventory_number: '',
              short_name: 'Adcon wind vane',
              device_type_uri: '',
              created_at: '2020-08-28T13:49:48.799090+00:00',
              manufacturer_name: 'OTT Hydromet GmbH',
              description: '',
              device_type_name: '',
              updated_at: '2020-08-29T13:49:48.799090+00:00',
              manufacturer_uri: '',
              long_name: 'Adcon wind vane',
              serial_number: '',
              persistent_identifier: null,
              model: 'Wind Vane',
              website: 'www.adcon.com',
              status_uri: '',
              status_name: ''
            },
            relationships: {
              // nothing more to make the test case not too complex
            }
          }],
        meta: {
          count: 2
        },
        jsonapi: {
          version: '1.0'
        }
      }

      // const property1 = DeviceProperty.createFromObject({
      //   id: '100',
      //   samplingMediaName: 'Air',
      //   samplingMediaUri: 'medium/air',
      //   compartmentName: 'C1',
      //   compartmentUri: 'compartment/c1',
      //   propertyName: 'Temperature',
      //   propertyUri: 'property/temperature',
      //   unitName: 'degree',
      //   unitUri: 'unit/degree',
      //   failureValue: -999,
      //   measuringRange: MeasuringRange.createFromObject({
      //     min: -273,
      //     max: 100
      //   }),
      //   label: 'air_temperature',
      //   accuracy: 0.1,
      //   resolution: 0.05,
      //   resolutionUnitName: 'TemperatureRes',
      //   resolutionUnitUri: 'property/res/temperature'
      // })
      // const property2 = DeviceProperty.createFromObject({
      //   id: '101',
      //   samplingMediaName: 'Water',
      //   samplingMediaUri: 'medium/water',
      //   compartmentName: 'C1',
      //   compartmentUri: 'compartment/c1',
      //   propertyName: 'Temperature',
      //   propertyUri: 'property/temperature',
      //   unitName: 'degree',
      //   unitUri: 'unit/degree',
      //   failureValue: -999,
      //   measuringRange: MeasuringRange.createFromObject({
      //     min: -10,
      //     max: 100
      //   }),
      //   label: 'water_temperature',
      //   accuracy: 0.1,
      //   resolution: 0.05,
      //   resolutionUnitName: 'TemperatureRes',
      //   resolutionUnitUri: 'property/res/temperature'
      // })

      const expectedContact = new Contact()
      expectedContact.id = '1'
      expectedContact.givenName = 'Max'
      expectedContact.familyName = 'Mustermann'
      expectedContact.email = 'max@mustermann.xyz'
      expectedContact.website = ''

      const expectedConfiguration1 = new Configuration()
      expectedConfiguration1.id = '1'
      expectedConfiguration1.startDate = DateTime.utc(2020, 8, 28, 13, 49, 48, 15)
      expectedConfiguration1.endDate = DateTime.utc(2020, 8, 29, 13, 49, 48, 15)
      expectedConfiguration1.label = 'Tereno NO Boeken'
      expectedConfiguration1.description = 'Boeken station'
      expectedConfiguration1.project = 'Tereno NO'
      expectedConfiguration1.archived = true
      expectedConfiguration1.status = 'draft'
      expectedConfiguration1.createdByUserId = '123456'
      expectedConfiguration1.persistentIdentifier = '12345/1234567890'
      expectedConfiguration1.keywords = ['key', 'word']

      const expectedConfiguration2 = new Configuration()
      expectedConfiguration2.id = '2'
      expectedConfiguration2.status = 'draft'
      expectedConfiguration2.archived = false

      const expectedConfiguration3 = new Configuration()
      expectedConfiguration3.id = '3'
      expectedConfiguration2.archived = false

      const expectedConfiguration4 = new Configuration()
      expectedConfiguration4.id = '4'
      expectedConfiguration2.archived = false

      const serializer = new ConfigurationSerializer()
      const configurationsWithMeta = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)
      const configurations = configurationsWithMeta.map((x: IConfigurationWithMeta) => {
        return x.configuration
      })

      expect(Array.isArray(configurations)).toBeTruthy()
      expect(configurations.length).toEqual(4)

      expect(configurations[0]).toEqual(expectedConfiguration1)
      expect(configurations[1]).toEqual(expectedConfiguration2)
      expect(configurations[2]).toEqual(expectedConfiguration3)
      expect(configurations[3]).toEqual(expectedConfiguration4)

      const missingContactIds = configurationsWithMeta.map((x: IConfigurationWithMeta) => {
        return x.missing.contacts.ids
      })

      expect(Array.isArray(missingContactIds)).toBeTruthy()
      expect(missingContactIds.length).toEqual(4)
      expect(missingContactIds[0]).toEqual([])
      expect(missingContactIds[1]).toEqual([])
      expect(missingContactIds[2]).toEqual([])
      expect(missingContactIds[3]).toEqual([])
    })
  })
  describe('#convertJsonApiObjectToModel', () => {
    it('should convert a json api object to a configuration model', () => {
      const jsonApiObject: any = {
        data: {
          type: 'configuration',
          attributes: {
            start_date: '2020-08-28T13:49:48.015620+00:00',
            end_date: '2020-08-29T13:49:48.015620+00:00',
            label: 'Tereno NO Boeken',
            description: 'Boeken station',
            project: 'Tereno NO',
            status: 'draft'
          },
          relationships: {
            // no contacts, as we expect an empty case here
          },
          id: '1'
        },
        jsonapi: {
          version: '1.0'
        }
      }
      const expectedConfiguration = new Configuration()
      expectedConfiguration.id = '1'
      expectedConfiguration.startDate = DateTime.utc(2020, 8, 28, 13, 49, 48, 15)
      expectedConfiguration.endDate = DateTime.utc(2020, 8, 29, 13, 49, 48, 15)
      expectedConfiguration.label = 'Tereno NO Boeken'
      expectedConfiguration.description = 'Boeken station'
      expectedConfiguration.project = 'Tereno NO'
      expectedConfiguration.status = 'draft'

      const serializer = new ConfigurationSerializer()
      const configurationWithMeta = serializer.convertJsonApiObjectToModel(jsonApiObject)
      const configuration = configurationWithMeta.configuration

      expect(configuration).toEqual(expectedConfiguration)
      expect(configurationWithMeta.missing.contacts.ids).toEqual([])
    })
    it('should also convert a configuration with information for contacts', () => {
      const jsonApiObject: any = {
        data: {
          type: 'configuration',
          attributes: {
            start_date: '2020-08-28T13:49:48.015620+00:00',
            end_date: '2020-08-29T13:49:48.015620+00:00',
            label: 'Tereno NO Boeken',
            description: 'Boeken station',
            project: 'Tereno NO',
            status: 'draft'
          },
          relationships: {
            contacts: {
              data: [{
                type: 'contact',
                id: '1'
              }, {
                type: 'contact',
                id: '2'
              }]
            }
          },
          id: '1'
        },
        included: [{
          type: 'contact',
          attributes: {
            given_name: 'Max',
            email: 'test@test.test',
            website: null,
            family_name: 'Mustermann'
          },
          id: '1'
        }, {
          type: 'contact',
          attributes: {
            given_name: 'Mux',
            email: 'test@tost.test',
            website: null,
            family_name: 'Mastermann'
          },
          id: '2'
        }],
        jsonapi: {
          version: '1.0'
        }
      }
      const expectedConfiguration = new Configuration()
      expectedConfiguration.id = '1'
      expectedConfiguration.startDate = DateTime.utc(2020, 8, 28, 13, 49, 48, 15)
      expectedConfiguration.endDate = DateTime.utc(2020, 8, 29, 13, 49, 48, 15)
      expectedConfiguration.label = 'Tereno NO Boeken'
      expectedConfiguration.description = 'Boeken station'
      expectedConfiguration.project = 'Tereno NO'
      expectedConfiguration.status = 'draft'
      expectedConfiguration.contacts = [
        Contact.createFromObject({
          id: '1',
          givenName: 'Max',
          familyName: 'Mustermann',
          website: '',
          organization: '',
          email: 'test@test.test',
          orcid: '',
          createdByUserId: null,
          createdAt: null,
          updatedAt: null
        }),
        Contact.createFromObject({
          id: '2',
          givenName: 'Mux',
          familyName: 'Mastermann',
          website: '',
          organization: '',
          orcid: '',
          email: 'test@tost.test',
          createdByUserId: null,
          createdAt: null,
          updatedAt: null
        })
      ]

      const serializer = new ConfigurationSerializer()
      const configurationWithMeta = serializer.convertJsonApiObjectToModel(jsonApiObject)
      const configuration = configurationWithMeta.configuration

      expect(configuration).toEqual(expectedConfiguration)
      expect(configurationWithMeta.missing.contacts.ids).toEqual([])
    })
  })
  describe('#convertJsonApiDataToModel', () => {
    it('should convert a json api data to a configuration model', () => {
      const jsonApiData: any = {
        attributes: {
          start_date: '2020-08-28T13:49:48.015620+00:00',
          end_date: '2020-08-29T13:49:48.015620+00:00',
          label: 'Tereno NO Boeken',
          description: 'Boeken station',
          project: 'Tereno NO',
          status: 'draft'
        },
        relationships: {
          contacts: {
            data: [] // no contacts in this case
          }
        },
        id: '1'
      }

      const expectedConfiguration = new Configuration()
      expectedConfiguration.id = '1'
      expectedConfiguration.startDate = DateTime.utc(2020, 8, 28, 13, 49, 48, 15)
      expectedConfiguration.endDate = DateTime.utc(2020, 8, 29, 13, 49, 48, 15)
      expectedConfiguration.label = 'Tereno NO Boeken'
      expectedConfiguration.description = 'Boeken station'
      expectedConfiguration.project = 'Tereno NO'
      expectedConfiguration.status = 'draft'

      const included: any[] = []

      const serializer = new ConfigurationSerializer()
      const configurationWithMeta = serializer.convertJsonApiDataToModel(jsonApiData, included)
      const configuration = configurationWithMeta.configuration

      expect(configuration).toEqual(expectedConfiguration)
      expect(configurationWithMeta.missing.contacts.ids).toEqual([])
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should convert a model to json data object', () => {
      const configuration = new Configuration()
      expect(configuration.id).toEqual('')
      configuration.label = 'ABC'
      configuration.description = 'some description'
      configuration.project = 'Project'
      configuration.persistentIdentifier = '12345/1234567890'
      configuration.startDate = DateTime.utc(2020, 8, 28, 13, 49, 48, 15)
      configuration.endDate = DateTime.utc(2021, 8, 28, 13, 49, 48, 15)
      configuration.contacts = [
        Contact.createFromObject({
          id: '1',
          givenName: 'Max',
          familyName: 'Mustermann',
          website: '',
          email: 'test@test.test',
          orcid: '',
          organization: '',
          createdByUserId: null,
          createdAt: null,
          updatedAt: null
        }),
        Contact.createFromObject({
          id: '2',
          givenName: 'Mux',
          familyName: 'Mastermann',
          website: '',
          organization: '',
          email: 'test@fost.test',
          orcid: '',
          createdByUserId: null,
          createdAt: null,
          updatedAt: null
        })
      ]
      configuration.siteId = '1'
      configuration.keywords = ['key', 'word']
      const serializer = new ConfigurationSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(configuration)

      expect(typeof jsonApiData).toEqual('object')

      expect(jsonApiData).not.toHaveProperty('id')
      expect(jsonApiData.type).toEqual('configuration')
      expect(jsonApiData).toHaveProperty('attributes')
      const attributes = jsonApiData.attributes

      expect(attributes).toHaveProperty('label')
      expect(attributes.label).toEqual('ABC')
      expect(attributes).toHaveProperty('description')
      expect(attributes.description).toEqual('some description')
      expect(attributes).toHaveProperty('project')
      expect(attributes.project).toEqual('Project')
      expect(attributes).toHaveProperty('start_date')
      expect(attributes.start_date).toEqual('2020-08-28T13:49:48.015Z')
      expect(attributes).toHaveProperty('end_date')
      expect(attributes.end_date).toEqual('2021-08-28T13:49:48.015Z')
      expect(attributes).toHaveProperty('persistent_identifier')
      expect(attributes.persistent_identifier).toEqual('12345/1234567890')
      expect(attributes).toHaveProperty('keywords')
      expect(attributes.keywords).toEqual(['key', 'word'])

      expect(jsonApiData).toHaveProperty('relationships')
      expect(typeof jsonApiData.relationships).toEqual('object')
      expect(jsonApiData.relationships).toHaveProperty('contacts')
      expect(typeof jsonApiData.relationships?.contacts).toEqual('object')
      expect(jsonApiData.relationships?.contacts).toHaveProperty('data')
      expect(jsonApiData.relationships).toHaveProperty('site')
      expect(typeof jsonApiData.relationships?.contacts).toEqual('object')
      expect(jsonApiData.relationships?.contacts).toHaveProperty('data')

      // we test for the inner structure of the result anyway
      // this cast is just to tell typescript that
      // we have an array of data, so that it doesn't show
      // typeerrors here
      const contactObject = jsonApiData.relationships?.contacts as IJsonApiEntityWithoutDetailsDataDictList

      const contactData = contactObject.data
      expect(Array.isArray(contactData)).toBeTruthy()
      expect(contactData.length).toEqual(2)
      expect(contactData[0]).toEqual({
        id: '1',
        type: 'contact'
      })
      expect(contactData[1]).toEqual({
        id: '2',
        type: 'contact'
      })
      const siteObject = jsonApiData.relationships?.site as IJsonApiEntityWithoutDetailsDataDict

      const siteData = siteObject.data
      expect(typeof siteData).toEqual('object')
      expect(siteData).toEqual({
        id: '1',
        type: 'site'
      })
    })
    it('should set an id if given for the configuration', () => {
      const configuration = new Configuration()
      configuration.id = '1'
      const serializer = new ConfigurationSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(configuration)

      expect(jsonApiData).toHaveProperty('id')
      expect(jsonApiData.id).toEqual('1')
    })
    it('should set the persistent identifier to null of not given', () => {
      const configuration = new Configuration()
      configuration.id = '1'
      const serializer = new ConfigurationSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(configuration)

      expect(jsonApiData).toHaveProperty('attributes')
      const attributes = jsonApiData.attributes
      expect(attributes).toHaveProperty('persistent_identifier')
      expect(attributes.persistent_identifier).toBeNull()
    })
    it('should convert to json api model if not site was set', () => {
      const configuration = new Configuration()
      expect(configuration.id).toEqual('')
      configuration.label = 'ABC'
      configuration.startDate = DateTime.utc(2020, 8, 28, 13, 49, 48, 15)
      configuration.endDate = DateTime.utc(2021, 8, 28, 13, 49, 48, 15)
      configuration.contacts = [
        Contact.createFromObject({
          id: '1',
          givenName: 'Max',
          familyName: 'Mustermann',
          website: '',
          email: 'test@test.test',
          organization: '',
          orcid: '',
          createdByUserId: null,
          createdAt: null,
          updatedAt: null
        }),
        Contact.createFromObject({
          id: '2',
          givenName: 'Mux',
          familyName: 'Mastermann',
          website: '',
          email: 'test@fost.test',
          organization: '',
          orcid: '',
          createdByUserId: null,
          createdAt: null,
          updatedAt: null
        })
      ]
      const serializer = new ConfigurationSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(configuration)

      expect(typeof jsonApiData).toEqual('object')

      expect(jsonApiData).not.toHaveProperty('id')
      expect(jsonApiData.type).toEqual('configuration')
      expect(jsonApiData).toHaveProperty('attributes')
      const attributes = jsonApiData.attributes

      expect(attributes).toHaveProperty('label')
      expect(attributes.label).toEqual('ABC')
      expect(attributes).toHaveProperty('start_date')
      expect(attributes.start_date).toEqual('2020-08-28T13:49:48.015Z')
      expect(attributes).toHaveProperty('end_date')
      expect(attributes.end_date).toEqual('2021-08-28T13:49:48.015Z')

      expect(jsonApiData).toHaveProperty('relationships')
      expect(typeof jsonApiData.relationships).toEqual('object')
      expect(jsonApiData.relationships).toHaveProperty('contacts')
      expect(typeof jsonApiData.relationships?.contacts).toEqual('object')
      expect(jsonApiData.relationships?.contacts).toHaveProperty('data')
      expect(jsonApiData.relationships).toHaveProperty('site')
      expect(typeof jsonApiData.relationships?.contacts).toEqual('object')
      expect(jsonApiData.relationships?.contacts).toHaveProperty('data')

      // we test for the inner structure of the result anyway
      // this cast is just to tell typescript that
      // we have an array of data, so that it doesn't show
      // typeerrors here
      const contactObject = jsonApiData.relationships?.contacts as IJsonApiEntityWithoutDetailsDataDictList

      const contactData = contactObject.data
      expect(Array.isArray(contactData)).toBeTruthy()
      expect(contactData.length).toEqual(2)
      expect(contactData[0]).toEqual({
        id: '1',
        type: 'contact'
      })
      expect(contactData[1]).toEqual({
        id: '2',
        type: 'contact'
      })
      const siteObject = jsonApiData.relationships?.site as IJsonApiEntityWithoutDetailsDataDict

      const siteData = siteObject.data
      expect(typeof siteData).toEqual('object')
      expect(siteData).toEqual(null)
    })
  })
  // in earlier versions, the test to serialize the configuration hierarchy
  // was here. As we don't handle a single hierarchy anymore, but the
  // the list of mpunt & unmount actions it is no longer representative.
  // (And the actions themselves are handled as entities of the JSON:API
  // on their own, so there is really no point in checking them for the
  // serializer).
})
describe('configurationWithMetaToConfigurationByThrowingErrorOnMissing', () => {
  it('should work without missing data', () => {
    const configuration = new Configuration()
    const missing = {
      contacts: {
        ids: []
      }
    }

    const result = configurationWithMetaToConfigurationByThrowingErrorOnMissing({
      configuration,
      missing
    })

    expect(result).toEqual(configuration)
    expect(result.contacts).toEqual([])
  })
  it('should also work if there is an contact', () => {
    const configuration = new Configuration()
    const contact = Contact.createFromObject({
      id: '1',
      familyName: 'Mustermann',
      givenName: 'Max',
      website: '',
      email: 'max@mustermann.de',
      organization: '',
      orcid: '',
      createdByUserId: null,
      createdAt: null,
      updatedAt: null
    })
    configuration.contacts.push(contact)

    const missing = {
      contacts: {
        ids: []
      }
    }
    const result = configurationWithMetaToConfigurationByThrowingErrorOnMissing({
      configuration,
      missing
    })

    expect(result).toEqual(configuration)
    expect(result.contacts).toEqual([contact])
  })
  it('should throw an error if there are missing data', () => {
    const configuration = new Configuration()
    const missing = {
      contacts: {
        ids: ['1']
      }
    }

    try {
      configurationWithMetaToConfigurationByThrowingErrorOnMissing({
        configuration,
        missing
      })
      fail('There must be an error')
    } catch (error: any) {
      expect(error.toString()).toMatch(/Contacts are missing/)
    }
  })
})
describe('configurationWithMetaToConfigurationByAddingDummyObjects', () => {
  it('should leave the data as it is if there are no missing data', () => {
    const configuration = new Configuration()
    const missing = {
      contacts: {
        ids: []
      }
    }

    const result = configurationWithMetaToConfigurationByAddingDummyObjects({
      configuration,
      missing
    })

    expect(result).toEqual(configuration)
    expect(result.contacts).toEqual([])
  })
  it('should stay with existing contacts without adding dummy data', () => {
    const configuration = new Configuration()
    const contact = Contact.createFromObject({
      id: '1',
      familyName: 'Mustermann',
      givenName: 'Max',
      website: '',
      email: 'max@mustermann.de',
      organization: '',
      orcid: '',
      createdByUserId: null,
      createdAt: null,
      updatedAt: null
    })
    configuration.contacts.push(contact)
    const missing = {
      contacts: {
        ids: []
      }
    }

    const result = configurationWithMetaToConfigurationByAddingDummyObjects({
      configuration,
      missing
    })

    expect(result).toEqual(configuration)
    expect(result.contacts).toEqual([contact])
  })
  it('should add a dummy contact', () => {
    const configuration = new Configuration()
    const contact = Contact.createFromObject({
      id: '1',
      familyName: 'Mustermann',
      givenName: 'Max',
      website: '',
      email: 'max@mustermann.de',
      organization: '',
      orcid: '',
      createdByUserId: null,
      createdAt: null,
      updatedAt: null
    })
    configuration.contacts.push(contact)
    const missing = {
      contacts: {
        ids: ['2']
      }
    }

    const newExpectedContact = new Contact()
    newExpectedContact.id = '2'

    const result = configurationWithMetaToConfigurationByAddingDummyObjects({
      configuration,
      missing
    })

    expect(result).toEqual(configuration)
    expect(result.contacts).toEqual([contact, newExpectedContact])
  })
})
