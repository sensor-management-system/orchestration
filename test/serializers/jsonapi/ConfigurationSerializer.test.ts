/**
 * @license
 * Web client of the Sensor Management System software developed within
 * the Helmholtz DataHub Initiative by GFZ and UFZ.
 *
 * Copyright (C) 2020
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

import { Configuration } from '@/models/Configuration'
import { Contact } from '@/models/Contact'
import { StationaryLocation, DynamicLocation } from '@/models/Location'

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
            location_type: 'stationary',
            longitude: 13.0,
            latitude: 52.0,
            elevation: 100.0,
            project_uri: 'projects/Tereno-NO',
            project_name: 'Tereno NO',
            label: 'Tereno NO Boeken',
            status: 'draft'
            // TODO: add hierarchy
          },
          relationships: {
            // TODO: add platforms & devices
            // but no contacts, as we expect an empty case here
          },
          id: '1'
        }, {
          type: 'configuration',
          attributes: {
            // no start and no end date
            location_type: 'dynamic',
            // no fields for longitude, latitude & elevation,
            // no fields for project_uri or project_name
            // no field for label
            // TODO: Test other status once we introduced others (and their names)
            status: 'draft'
            // TODO
          },
          relationships: {
            // TODO: add platforms & devices
            // but no contacts, as we expect an empty case here
            // and handle device properties somehow
          },
          id: '2'
        }, {
          type: 'configuration',
          attributes: {},
          relationships: {},
          id: '3'
        }],
        meta: {
          count: 2
        },
        jsonapi: {
          version: '1.0'
        }
      }

      const expectedConfiguration1 = new Configuration()
      expectedConfiguration1.id = '1'
      expectedConfiguration1.location = StationaryLocation.createFromObject({
        longitude: 13.0,
        latitude: 52.0,
        elevation: 100.0
      })
      expectedConfiguration1.startDate = new Date('2020-08-28T13:49:48.015620+00:00')
      expectedConfiguration1.endDate = new Date('2020-08-29T13:49:48.015620+00:00')
      expectedConfiguration1.projectUri = 'projects/Tereno-NO'
      expectedConfiguration1.projectName = 'Tereno NO'
      expectedConfiguration1.label = 'Tereno NO Boeken'
      expectedConfiguration1.status = 'draft'
      // TODO add platforms & devices

      const expectedConfiguration2 = new Configuration()
      expectedConfiguration2.id = '2'
      expectedConfiguration2.location = new DynamicLocation()
      expectedConfiguration2.status = 'draft'
      // TODO add device properties
      // TODO

      const expectedConfiguration3 = new Configuration()
      expectedConfiguration3.id = '3'

      const serializer = new ConfigurationSerializer()
      const configurationsWithMeta = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)
      const configurations = configurationsWithMeta.map((x: IConfigurationWithMeta) => {
        return x.configuration
      })

      expect(Array.isArray(configurations)).toBeTruthy()
      expect(configurations.length).toEqual(3)

      expect(configurations[0]).toEqual(expectedConfiguration1)
      expect(configurations[1]).toEqual(expectedConfiguration2)
      expect(configurations[2]).toEqual(expectedConfiguration3)

      const missingContactIds = configurationsWithMeta.map((x: IConfigurationWithMeta) => {
        return x.missing.contacts.ids
      })

      expect(Array.isArray(missingContactIds)).toBeTruthy()
      expect(missingContactIds.length).toEqual(3)
      expect(missingContactIds[0]).toEqual([])
      expect(missingContactIds[1]).toEqual([])
      expect(missingContactIds[2]).toEqual([])
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
            location_type: 'stationary',
            longitude: 13.0,
            latitude: 52.0,
            elevation: 100.0,
            project_uri: 'projects/Tereno-NO',
            project_name: 'Tereno NO',
            label: 'Tereno NO Boeken',
            status: 'draft'
            // TODO: add hierarchy
          },
          relationships: {
            // TODO: add platforms & devices
            // but no contacts, as we expect an empty case here
          },
          id: '1'
        },
        jsonapi: {
          version: '1.0'
        }
      }
      const expectedConfiguration = new Configuration()
      expectedConfiguration.id = '1'
      expectedConfiguration.location = StationaryLocation.createFromObject({
        longitude: 13.0,
        latitude: 52.0,
        elevation: 100.0
      })
      expectedConfiguration.startDate = new Date('2020-08-28T13:49:48.015620+00:00')
      expectedConfiguration.endDate = new Date('2020-08-29T13:49:48.015620+00:00')
      expectedConfiguration.projectUri = 'projects/Tereno-NO'
      expectedConfiguration.projectName = 'Tereno NO'
      expectedConfiguration.label = 'Tereno NO Boeken'
      expectedConfiguration.status = 'draft'
      // TODO

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
            location_type: 'stationary',
            longitude: 13.0,
            latitude: 52.0,
            elevation: 100.0,
            project_uri: 'projects/Tereno-NO',
            project_name: 'Tereno NO',
            label: 'Tereno NO Boeken',
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
      expectedConfiguration.location = StationaryLocation.createFromObject({
        longitude: 13.0,
        latitude: 52.0,
        elevation: 100.0
      })
      expectedConfiguration.startDate = new Date('2020-08-28T13:49:48.015620+00:00')
      expectedConfiguration.endDate = new Date('2020-08-29T13:49:48.015620+00:00')
      expectedConfiguration.projectUri = 'projects/Tereno-NO'
      expectedConfiguration.projectName = 'Tereno NO'
      expectedConfiguration.label = 'Tereno NO Boeken'
      expectedConfiguration.status = 'draft'
      expectedConfiguration.contacts = [
        Contact.createFromObject({
          id: '1',
          givenName: 'Max',
          familyName: 'Mustermann',
          website: '',
          email: 'test@test.test'
        }),
        Contact.createFromObject({
          id: '2',
          givenName: 'Mux',
          familyName: 'Mastermann',
          website: '',
          email: 'test@tost.test'
        })
      ]
      // TODO platforms & devies

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
          location_type: 'stationary',
          longitude: 13.0,
          latitude: 52.0,
          elevation: 100.0,
          project_uri: 'projects/Tereno-NO',
          project_name: 'Tereno NO',
          label: 'Tereno NO Boeken',
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
      expectedConfiguration.location = StationaryLocation.createFromObject({
        longitude: 13.0,
        latitude: 52.0,
        elevation: 100.0
      })
      expectedConfiguration.startDate = new Date('2020-08-28T13:49:48.015620+00:00')
      expectedConfiguration.endDate = new Date('2020-08-29T13:49:48.015620+00:00')
      expectedConfiguration.projectUri = 'projects/Tereno-NO'
      expectedConfiguration.projectName = 'Tereno NO'
      expectedConfiguration.label = 'Tereno NO Boeken'
      expectedConfiguration.status = 'draft'
      // TODO
      // add platforms & devices

      const included: any[] = []

      const serializer = new ConfigurationSerializer()
      const configurationWithMeta = serializer.convertJsonApiDataToModel(jsonApiData, included)
      const configuration = configurationWithMeta.configuration

      expect(configuration).toEqual(expectedConfiguration)
      expect(configurationWithMeta.missing.contacts.ids).toEqual([])
    })
    it('should convert a json api data to a configuration model without lat&lon', () => {
      const jsonApiData: any = {
        attributes: {
          start_date: '2020-08-28T13:49:48.015620+00:00',
          end_date: '2020-08-29T13:49:48.015620+00:00',
          location_type: 'stationary',
          longitude: null,
          latitude: null,
          elevation: null,
          project_uri: 'projects/Tereno-NO',
          project_name: 'Tereno NO',
          label: 'Tereno NO Boeken',
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
      expectedConfiguration.location = new StationaryLocation()
      expectedConfiguration.startDate = new Date('2020-08-28T13:49:48.015620+00:00')
      expectedConfiguration.endDate = new Date('2020-08-29T13:49:48.015620+00:00')
      expectedConfiguration.projectUri = 'projects/Tereno-NO'
      expectedConfiguration.projectName = 'Tereno NO'
      expectedConfiguration.label = 'Tereno NO Boeken'
      expectedConfiguration.status = 'draft'
      // TODO
      // add platforms & devices

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
      configuration.projectUri = 'projects/tereno-no'
      configuration.projectName = 'TERENO NO'
      configuration.location = StationaryLocation.createFromObject({
        longitude: 12.0,
        latitude: 51.0,
        elevation: 60.0
      })
      configuration.startDate = new Date('2020-08-28T13:49:48.015620+00:00')
      configuration.endDate = new Date('2021-08-28T13:49:48.015620+00:00')
      configuration.contacts = [
        Contact.createFromObject({
          id: '1',
          givenName: 'Max',
          familyName: 'Mustermann',
          website: '',
          email: 'test@test.test'
        }),
        Contact.createFromObject({
          id: '2',
          givenName: 'Mux',
          familyName: 'Mastermann',
          website: '',
          email: 'test@fost.test'
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
      expect(attributes).toHaveProperty('project_uri')
      expect(attributes.project_uri).toEqual('projects/tereno-no')
      expect(attributes).toHaveProperty('project_name')
      expect(attributes.project_name).toEqual('TERENO NO')
      expect(attributes).toHaveProperty('location_type')
      expect(attributes.location_type).toEqual('stationary')
      expect(attributes).toHaveProperty('longitude')
      expect(attributes.longitude).toEqual(12.0)
      expect(attributes).toHaveProperty('latitude')
      expect(attributes.latitude).toEqual(51.0)
      expect(attributes).toHaveProperty('elevation')
      expect(attributes.elevation).toEqual(60.0)
      expect(attributes).toHaveProperty('start_date')
      expect(attributes.start_date).toEqual('2020-08-28T13:49:48.015Z')
      expect(attributes).toHaveProperty('end_date')
      expect(attributes.end_date).toEqual('2021-08-28T13:49:48.015Z')

      expect(jsonApiData).toHaveProperty('relationships')
      expect(typeof jsonApiData.relationships).toEqual('object')
      expect(jsonApiData.relationships).toHaveProperty('contacts')
      expect(typeof jsonApiData.relationships.contacts).toEqual('object')
      expect(jsonApiData.relationships.contacts).toHaveProperty('data')

      const contactData = jsonApiData.relationships.contacts.data
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

      // TODO: platforms & devices
    })
    it('should set an id if given for the configuration', () => {
      const configuration = new Configuration()
      configuration.id = '1'
      const serializer = new ConfigurationSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(configuration)

      expect(jsonApiData).toHaveProperty('id')
      expect(jsonApiData.id).toEqual('1')
    })
    it('should also work with a dynamic location type', () => {
      const configuration = new Configuration()
      expect(configuration.id).toEqual('')
      configuration.location = new DynamicLocation()

      const serializer = new ConfigurationSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(configuration)

      expect(typeof jsonApiData).toEqual('object')

      expect(jsonApiData).not.toHaveProperty('id')
      expect(jsonApiData.type).toEqual('configuration')
      expect(jsonApiData).toHaveProperty('attributes')
      const attributes = jsonApiData.attributes

      expect(attributes).toHaveProperty('location_type')
      expect(attributes.location_type).toEqual('dynamic')
      // TODO: platforms & devices
    })
    it('should also work with an empty stationary location type', () => {
      const configuration = new Configuration()
      expect(configuration.id).toEqual('')
      configuration.location = new StationaryLocation()

      const serializer = new ConfigurationSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(configuration)

      expect(typeof jsonApiData).toEqual('object')

      expect(jsonApiData).not.toHaveProperty('id')
      expect(jsonApiData.type).toEqual('configuration')
      expect(jsonApiData).toHaveProperty('attributes')
      const attributes = jsonApiData.attributes

      expect(attributes).toHaveProperty('location_type')
      expect(attributes.location_type).toEqual('stationary')
      expect(attributes).toHaveProperty('longitude')
      expect(attributes.longitude).toEqual(null)
      expect(attributes).toHaveProperty('latitude')
      expect(attributes.latitude).toEqual(null)
      expect(attributes).toHaveProperty('elevation')
      expect(attributes.elevation).toEqual(null)
    })
  })
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
      email: 'max@mustermann.de'
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
    } catch (error) {
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
      email: 'max@mustermann.de'
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
      email: 'max@mustermann.de'
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
