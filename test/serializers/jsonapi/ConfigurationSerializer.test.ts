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
            // TODO
          },
          relationships: {
            // TODO
          },
          id: '1'
        }, {
          type: 'configuration',
          attributes: {
            // TODO
          },
          relationships: {
            // TODO
          }
        }],
        meta: {
          count: 2
        },
        jsonapi: {
          version: '1.0'
        }
      }

      const expectedConfiguration1 = new Configuration()
      // TODO

      const expectedConfiguration2 = new Configuration()
      // TODO

      const serializer = new ConfigurationSerializer()
      const configurationsWithMeta = serializer.convertJsonApiObjectListToModelList(jsonApiObjectList)
      const configurations = configurationsWithMeta.map((x: IConfigurationWithMeta) => {
        return x.configuration
      })

      expect(Array.isArray(configurations)).toBeTruthy()
      expect(configurations.length).toEqual(2)

      expect(configurations[0]).toEqual(expectedConfiguration1)
      expect(configurations[1]).toEqual(expectedConfiguration2)

      const missingContactIds = configurationsWithMeta.map((x: IConfigurationWithMeta) => {
        return x.missing.contacts.ids
      })

      expect(Array.isArray(missingContactIds)).toBeTruthy()
      expect(missingContactIds.length).toEqual(2)
      expect(missingContactIds[0]).toEqual([])
      expect(missingContactIds[1]).toEqual([])
    })
  })
  describe('#convertJsonApiObjectToModel', () => {
    it('should convert a json api object to a configuration model', () => {
      const jsonApiObject: any = {
        data: {
          type: 'configuration',
          attributes: {
            // TODO
          },
          relationships: {
            // TODO
          },
          id: '1'
        },
        jsonapi: {
          version: '1.0'
        }
      }
      const expectedConfiguration = new Configuration()
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
            // TODO
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
      // TODO

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
        type: 'configuration',
        attributes: {
          // TODO
        },
        relationships: {
          // TODO
        },
        id: '1'
      }

      const expectedConfiguraiton = new Configuration()
      // TODO

      const included: any[] = []

      const serializer = new ConfigurationSerializer()
      const configurationWithMeta = serializer.convertJsonApiDataToModel(jsonApiData, included)
      const configuration = configurationWithMeta.configuration

      expect(configuration).toEqual(expectedConfiguraiton)
      expect(configurationWithMeta.missing.contacts.ids).toEqual([])
    })
  })
  describe('#convertModelToJsonApiData', () => {
    it('should convert a model to json data object', () => {
      const configuration = new Configuration()
      expect(configuration.id).toEqual('')
      const serializer = new ConfigurationSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(configuration)

      expect(typeof jsonApiData).toEqual('object')

      expect(jsonApiData).not.toHaveProperty('id')
      expect(jsonApiData.type).toEqual('configuration')
      expect(jsonApiData).toHaveProperty('attributes')
      const attributes = jsonApiData.attributes

      //expect(attributes).toHaveProperty('label')
      // TODO

      expect(jsonApiData).toHaveProperty('relationships')
      expect(typeof jsonApiData.relationships).toEqual('object')
      expect(jsonApiData.relationships).toHaveProperty('contacts')
      expect(typeof jsonApiData.relationships.contacts).toEqual('object')
      expect(jsonApiData.relationships.contacts).toHaveProperty('data')
      const contactData = jsonApiData.relationships.contacts.data
      expect(Array.isArray(contactData)).toBeTruthy()
      // TODO
    })
    it('should set an id if given for the configuration', () => {
      const configuration = new Configuration()
      configuration.id = '1'
      const serializer = new ConfigurationSerializer()

      const jsonApiData = serializer.convertModelToJsonApiData(configuration)

      expect(jsonApiData).toHaveProperty('id')
      expect(jsonApiData.id).toEqual('1')
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
