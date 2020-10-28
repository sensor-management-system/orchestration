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

import { IJsonApiObjectList, IJsonApiObject, IJsonApiDataWithId, IJsonApiDataWithOptionalId, IJsonApiTypeIdAttributes } from '@/serializers/jsonapi/JsonApiTypes'

import { IMissingContactData } from '@/serializers/jsonapi/ContactSerializer'

export interface IConfigurationMissingData {
  contacts: IMissingContactData
}

export interface IConfigurationWithMeta {
  configuration: Configuration
  missing: IConfigurationMissingData
}

export class ConfigurationSerializer {
  convertJsonApiObjectListToModelList (jsonApiObjectList: IJsonApiObjectList): IConfigurationWithMeta[] {
    const included = jsonApiObjectList.included || []
    return jsonApiObjectList.data.map((model: IJsonApiDataWithId) => {
      return this.convertJsonApiDataToModel(model, included)
    })
  }

  convertJsonApiObjectToModel (jsonApiObject: IJsonApiObject): IConfigurationWithMeta {
    const included = jsonApiObject.included || []
    return this.convertJsonApiDataToModel(jsonApiObject.data, included)
  }

  convertJsonApiDataToModel (jsonApiData: IJsonApiDataWithId, included: IJsonApiTypeIdAttributes[]): IConfigurationWithMeta {
    const configuration = new Configuration()
    const missing = {
      contacts: {
        ids: []
      }
    }
    return {
      configuration,
      missing
    }
  }

  convertModelToJsonApiData (configuration: Configuration): IJsonApiDataWithOptionalId {
    const result: IJsonApiDataWithOptionalId = {
      attributes: {},
      relationships: {
        contacts: {
          data: []
        }
      },
      type: 'configuration'
    }
    if (configuration.id) {
      result.id = configuration.id
    }
    return result
  }
}

export const configurationWithMetaToConfigurationByThrowingErrorOnMissing = (configurationWithMeta: IConfigurationWithMeta) : Configuration => {
  const configuration = configurationWithMeta.configuration
  if (configurationWithMeta.missing.contacts.ids.length > 0) {
    throw new Error('Contacts are missing')
  }
  return configuration
}

export const configurationWithMetaToConfigurationByAddingDummyObjects = (configurationWithMeta: IConfigurationWithMeta) : Configuration => {
  const configuration = configurationWithMeta.configuration

  for (const missingContactId of configurationWithMeta.missing.contacts.ids) {
    const contact = new Contact()
    contact.id = missingContactId
    configuration.contacts.push(contact)
  }
  return configuration
}
